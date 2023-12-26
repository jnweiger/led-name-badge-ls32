import sys
import unittest

if __name__ == '__main__':
    sys.path.append("..")
    suite = unittest.TestLoader().discover(".")
    unittest.TextTestRunner().run(suite)

