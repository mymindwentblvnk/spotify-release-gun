import os
import unittest


def load_tests(loader, standard_tests, pattern):
    this_dir = os.path.dirname(__file__)
    pattern = pattern or 'test_*.py'
    package_tests = loader.discover(start_dir=this_dir,
                                    pattern=pattern,
                                    top_level_dir=this_dir)
    standard_tests.addTests(package_tests)
    return standard_tests


if __name__ == '__main__':
    unittest.main()
