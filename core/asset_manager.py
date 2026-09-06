# -*- coding: utf-8 -*-
"""
Asset Manager Module for LET IT DIE Save Editor.
Handles hybrid remote/local asset resolution:
- Serves images instantly from local disk (icons/ or cache/icons/).
- Asynchronously downloads missing assets from jsDelivr CDN without blocking GUI.
- Atomically writes to local cache to ensure integrity.
- Provides batch downloading for complete offline experience.
"""

import os
import sys
import json
import time
import shutil
import urllib.request
import threading
from concurrent.futures import ThreadPoolExecutor

if getattr(sys, "frozen", False):
    BUNDLE_ROOT = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(sys.executable)))
    EXE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BUNDLE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    EXE_DIR = BUNDLE_ROOT

PROJECT_ROOT = BUNDLE_ROOT

# Standard directories
ICONS_LOCAL_DIR = os.path.join(BUNDLE_ROOT, "icons")
if not os.path.isdir(ICONS_LOCAL_DIR):
    ICONS_LOCAL_DIR = os.path.join(EXE_DIR, "icons")

# Determine writable cache directory (self-contained next to exe if possible, %LOCALAPPDATA% fallback)
_local_cache_candidate = os.path.join(EXE_DIR, "cache", "icons")
try:
    os.makedirs(_local_cache_candidate, exist_ok=True)
    CACHE_DIR = _local_cache_candidate
except Exception:
    app_data = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
    CACHE_DIR = os.path.join(app_data, "LetItDieSaveEditor", "cache", "icons")
    os.makedirs(CACHE_DIR, exist_ok=True)

DEFAULT_CDN_BASE = "https://cdn.jsdelivr.net/gh/g3usyk/Let-It-Die-Save-Editor@main/icons/"
FALLBACK_RAW_BASE = "https://raw.githubusercontent.com/g3usyk/Let-It-Die-Save-Editor/main/icons/"


class AssetManager:
    """Manages downloading, local disk caching, and thread-safe asset resolution."""

    def __init__(self, cdn_base=DEFAULT_CDN_BASE, cache_dir=CACHE_DIR, max_workers=4):
        self.cdn_base = cdn_base.rstrip("/") + "/"
        self.fallback_base = FALLBACK_RAW_BASE.rstrip("/") + "/"
        self.cache_dir = cache_dir
        self.local_icons_dir = ICONS_LOCAL_DIR
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="AssetWorker")
        self._lock = threading.Lock()
        self._pending = set()
        self._callbacks = {}
        self._is_batch_downloading = False
        self._cancel_batch = False

        self.manifest = {}
        for m_root in [BUNDLE_ROOT, EXE_DIR, PROJECT_ROOT]:
            m_path = os.path.join(m_root, "asset_manifest.json")
            if os.path.isfile(m_path):
                try:
                    with open(m_path, "r", encoding="utf-8") as f:
                        self.manifest = json.load(f)
                    break
                except Exception:
                    pass

    def normalize_rel_path(self, rel_path):
        """Converts Windows backslashes and strips leading slashes."""
        if not rel_path:
            return ""
        norm = str(rel_path).replace("\\", "/").strip().lstrip("/")
        return norm

    def resolve_asset_path(self, rel_path):
        """Resolves a bare filename or relative path to its canonical repository path."""
        norm = self.normalize_rel_path(rel_path)
        if not norm:
            return ""
        if "/" in norm:
            return norm
        lower = norm.lower()
        if hasattr(self, "manifest") and self.manifest:
            if lower in self.manifest:
                return self.manifest[lower]
            stem = os.path.splitext(lower)[0]
            if stem in self.manifest:
                return self.manifest[stem]
        return norm

    def get_local_path(self, rel_path):
        """
        Checks if the asset exists locally in:
        1. Local icons/ directory
        2. Local persistent cache_dir
        Returns the absolute filepath if found, otherwise None.
        """
        canonical = self.resolve_asset_path(rel_path)
        if not canonical:
            return None

        # 1. Check primary icons directory
        primary = os.path.join(self.local_icons_dir, canonical.replace("/", os.sep))
        if os.path.isfile(primary):
            return primary

        # 2. Check local persistent cache
        cached = os.path.join(self.cache_dir, canonical.replace("/", os.sep))
        if os.path.isfile(cached):
            return cached

        # 3. Direct filename check inside icons subdirectories
        base_name = os.path.basename(canonical)
        for sub in ["", "cards", "sets", "all_official", "armor", "weapons", "materials", "decals", "shrooms", "gear", "thumbs"]:
            p1 = os.path.join(self.local_icons_dir, sub, base_name)
            if os.path.isfile(p1):
                return p1
            p2 = os.path.join(self.cache_dir, sub, base_name)
            if os.path.isfile(p2):
                return p2

        return None

    def get_cdn_url(self, rel_path, use_fallback=False):
        """Builds full CDN URL for a given relative path."""
        canonical = self.resolve_asset_path(rel_path)
        base = self.fallback_base if use_fallback else self.cdn_base
        return base + canonical

    def request_asset(self, rel_path, on_downloaded=None):
        """
        Requests an asset asynchronously:
        If it's already on disk, returns its path immediately.
        If missing, queues background download and calls on_downloaded(path) when ready.
        """
        canonical = self.resolve_asset_path(rel_path)
        existing = self.get_local_path(canonical)
        if existing:
            if on_downloaded:
                try:
                    on_downloaded(existing)
                except Exception:
                    pass
            return existing

        if not canonical:
            return None

        with self._lock:
            if on_downloaded:
                self._callbacks.setdefault(canonical, []).append(on_downloaded)
            if canonical in self._pending:
                return None
            self._pending.add(canonical)

        self.executor.submit(self._download_worker, canonical)
        return None

    def _download_worker(self, norm_rel_path):
        """Worker thread to download a single file from CDN and cache it atomically."""
        dest_path = os.path.join(self.cache_dir, norm_rel_path.replace("/", os.sep))
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        temp_path = dest_path + f".tmp_{threading.get_ident()}_{int(time.time()*1000)}"

        success = False
        urls = [self.get_cdn_url(norm_rel_path, use_fallback=False), self.get_cdn_url(norm_rel_path, use_fallback=True)]
        
        for url in urls:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "LetItDieSaveEditor/4.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    if resp.status == 200:
                        with open(temp_path, "wb") as f:
                            shutil.copyfileobj(resp, f)
                        os.replace(temp_path, dest_path)
                        success = True
                        break
            except Exception:
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass

        with self._lock:
            self._pending.discard(norm_rel_path)
            cbs = self._callbacks.pop(norm_rel_path, [])

        if success:
            for cb in cbs:
                try:
                    cb(dest_path)
                except Exception:
                    pass

    def get_cache_stats(self):
        """Calculates total number of cached files and total size in MB."""
        file_count = 0
        total_bytes = 0
        if os.path.isdir(self.cache_dir):
            for root, _, files in os.walk(self.cache_dir):
                for f in files:
                    if not f.endswith(".tmp"):
                        fp = os.path.join(root, f)
                        try:
                            total_bytes += os.path.getsize(fp)
                            file_count += 1
                        except OSError:
                            pass
        return {
            "count": file_count,
            "size_mb": round(total_bytes / (1024 * 1024), 2),
            "cache_dir": self.cache_dir,
        }

    def clear_cache(self):
        """Removes all files in the cache directory."""
        if os.path.isdir(self.cache_dir):
            for root, dirs, files in os.walk(self.cache_dir, topdown=False):
                for f in files:
                    try:
                        os.remove(os.path.join(root, f))
                    except OSError:
                        pass
                for d in dirs:
                    try:
                        os.rmdir(os.path.join(root, d))
                    except OSError:
                        pass
        return True

    def download_all_assets_async(self, all_rel_paths=None, progress_callback=None, completion_callback=None):
        """
        Batch downloader for offline preparation.
        all_rel_paths: list of relative asset paths to ensure in cache (if None, downloads entire manifest).
        progress_callback: fn(current, total, current_file)
        completion_callback: fn(downloaded_count, error_count)
        """
        if self._is_batch_downloading:
            return False

        if not all_rel_paths and getattr(self, "manifest", None):
            all_rel_paths = list(set(self.manifest.values()))
        elif not all_rel_paths:
            all_rel_paths = []

        self._is_batch_downloading = True
        self._cancel_batch = False

        def batch_worker():
            missing = []
            for p in all_rel_paths:
                if not self.get_local_path(p):
                    missing.append(self.normalize_rel_path(p))

            total = len(missing)
            downloaded = 0
            errors = 0

            for i, rel_p in enumerate(missing):
                if self._cancel_batch:
                    break
                dest = os.path.join(self.cache_dir, rel_p.replace("/", os.sep))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                tmp = dest + f".tmp_{time.time()}"
                url = self.get_cdn_url(rel_p)
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "LetItDieSaveEditor/4.0"})
                    with urllib.request.urlopen(req, timeout=6) as resp:
                        if resp.status == 200:
                            with open(tmp, "wb") as f:
                                shutil.copyfileobj(resp, f)
                            os.replace(tmp, dest)
                            downloaded += 1
                except Exception:
                    if os.path.exists(tmp):
                        try:
                            os.remove(tmp)
                        except OSError:
                            pass
                    errors += 1

                if progress_callback:
                    try:
                        progress_callback(i + 1, total, rel_p)
                    except Exception:
                        pass

            self._is_batch_downloading = False
            if completion_callback:
                try:
                    completion_callback(downloaded, errors)
                except Exception:
                    pass

        t = threading.Thread(target=batch_worker, daemon=True)
        t.start()
        return True

    def cancel_batch_download(self):
        """Signals the batch worker to stop gracefully."""
        self._cancel_batch = True
