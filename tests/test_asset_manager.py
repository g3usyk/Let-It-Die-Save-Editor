# -*- coding: utf-8 -*-
"""
Unit tests for core.asset_manager (Hybrid CDN & Local Cache).
"""

import os
import io
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from core.asset_manager import AssetManager


class TestAssetManager(unittest.TestCase):

    def setUp(self):
        self.temp_cache = tempfile.mkdtemp(prefix="test_cache_")
        self.manager = AssetManager(cache_dir=self.temp_cache)

    def tearDown(self):
        if os.path.exists(self.temp_cache):
            shutil.rmtree(self.temp_cache, ignore_errors=True)

    def test_normalize_rel_path(self):
        self.assertEqual(self.manager.normalize_rel_path("cards\\item.png"), "cards/item.png")
        self.assertEqual(self.manager.normalize_rel_path("/icons/all_official/gear.png"), "icons/all_official/gear.png")
        self.assertEqual(self.manager.normalize_rel_path(""), "")
        self.assertEqual(self.manager.normalize_rel_path(None), "")

    def test_get_cdn_url(self):
        url = self.manager.get_cdn_url("all_official/pt_arm_wp001_001.png")
        self.assertTrue(url.startswith("https://cdn.jsdelivr.net/gh/g3usyk/Let-It-Die-Save-Editor@main/icons/"))
        self.assertTrue(url.endswith("all_official/pt_arm_wp001_001.png"))

        url_fallback = self.manager.get_cdn_url("all_official/pt_arm_wp001_001.png", use_fallback=True)
        self.assertTrue(url_fallback.startswith("https://raw.githubusercontent.com/g3usyk/Let-It-Die-Save-Editor/main/icons/"))

    def test_get_local_path_existing_and_missing(self):
        # dm.png is in the repository's icons/ directory
        local = self.manager.get_local_path("dm.png")
        self.assertIsNotNone(local)
        self.assertTrue(os.path.exists(local))

        # Missing asset should return None
        missing = self.manager.get_local_path("non_existent_image_12345.png")
        self.assertIsNone(missing)

    def test_cache_stats_and_clear(self):
        # Initially empty cache
        stats = self.manager.get_cache_stats()
        self.assertEqual(stats["count"], 0)
        self.assertEqual(stats["size_mb"], 0.0)

        # Create dummy cached file
        dummy_file = os.path.join(self.temp_cache, "test.png")
        with open(dummy_file, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 1024)

        stats_after = self.manager.get_cache_stats()
        self.assertEqual(stats_after["count"], 1)

        # Clear cache
        self.manager.clear_cache()
        stats_cleared = self.manager.get_cache_stats()
        self.assertEqual(stats_cleared["count"], 0)

    def test_request_asset_already_local(self):
        called = []
        result = self.manager.request_asset("dm.png", on_downloaded=lambda p: called.append(p))
        self.assertIsNotNone(result)
        self.assertEqual(len(called), 1)
        self.assertTrue(os.path.exists(called[0]))

    @patch("urllib.request.urlopen")
    def test_download_worker_successful_cache(self, mock_urlopen):
        dummy_png_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read = MagicMock(side_effect=[dummy_png_bytes, b""])
        mock_urlopen.return_value.__enter__.return_value = mock_response

        target_rel = "mock_sub/mock_icon.png"
        self.assertIsNone(self.manager.get_local_path(target_rel))

        # Run worker directly
        self.manager._download_worker(target_rel)

        # Should now exist in cache
        cached_path = self.manager.get_local_path(target_rel)
        self.assertIsNotNone(cached_path)
        self.assertTrue(os.path.exists(cached_path))
        with open(cached_path, "rb") as f:
            content = f.read()
        self.assertEqual(content, dummy_png_bytes)

    @patch("urllib.request.urlopen", side_effect=Exception("Network unreachable"))
    def test_download_worker_network_error_graceful(self, mock_urlopen):
        target_rel = "fail_sub/fail_icon.png"
        # Should not raise exception
        self.manager._download_worker(target_rel)
        self.assertIsNone(self.manager.get_local_path(target_rel))


if __name__ == "__main__":
    unittest.main()
