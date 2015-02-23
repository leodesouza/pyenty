from unittest.suite import TestSuite
import unittest


suite = TestSuite()


def load_tests(loader, tests, pattern):
    for all_test_suite in unittest.defaultTestLoader.discover('tests', pattern='*_test.py'):
        for test_suite in all_test_suite:
            suite.addTest(test_suite)

    return suite


if __name__ == "__main__":
    unittest.main()
