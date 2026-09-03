# -*- coding: utf-8 -*-
"""
LET IT DIE Save Editor - Automated Test Suite Runner.
Executes all unit and integration tests across save_io, modifiers, core, and i18n.
"""
import unittest
import sys
import os
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def run():
    print("=" * 70)
    print("  LET IT DIE SAVE EDITOR - AUTOMATED TEST SUITE")
    print("=" * 70)
    
    start_time = time.time()
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.join(PROJECT_ROOT, "tests"), pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    elapsed = time.time() - start_time
    print("-" * 70)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Successes:      {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:       {len(result.failures)}")
    print(f"Errors:         {len(result.errors)}")
    print(f"Execution Time: {elapsed:.3f}s")
    print("=" * 70)
    
    if result.wasSuccessful():
        print(">>> ALL TESTS PASSED! CODEBASE IS 100% HEALTHY! <<<")
        return 0
    else:
        print(">>> TEST SUITE FAILED! PLEASE REVIEW ERRORS ABOVE. <<<")
        return 1

if __name__ == "__main__":
    sys.exit(run())
