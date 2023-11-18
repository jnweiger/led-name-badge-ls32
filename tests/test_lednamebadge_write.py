import datetime
from unittest import TestCase

from lednamebadge import LedNameBadge as testee


class Test(TestCase):
    def setUp(self):
        self.test_date = datetime.datetime(2022, 11, 13, 17, 38, 24)

    def test_prepare_collection_expand(self):
        self.assertEqual((1, 1, 1, 1, 1, 1, 1, 1), testee._prepare_iterable((1,), 1, 8))
        self.assertEqual((1, 2, 3, 4, 4, 4, 4, 4), testee._prepare_iterable([1, 2, 3, 4], 1, 8))
        self.assertEqual((1, 2, 3, 4, 5, 6, 7, 8), testee._prepare_iterable((1, 2, 3, 4, 5, 6, 7, 8), 1, 8))
        # Weired, but possible:
        self.assertEqual(('A', 'B', 'C', 'D', 'D', 'D', 'D', 'D'), testee._prepare_iterable("ABCD", 'A', 'Z'))
        self.assertEqual((True, False, True, True, True, True, True, True), testee._prepare_iterable((True, False, True), False, True))

    def test_prepare_collection_limit(self):
        self.assertEqual((1, 8, 8, 8, 8, 8, 8, 8), testee._prepare_iterable([-1, 9], 1, 8))
        # Weired, but possible:
        self.assertEqual(('C', 'C', 'C', 'D', 'E', 'F', 'F', 'F'), testee._prepare_iterable("ABCDEFGH", 'C', 'F'))
        self.assertEqual((True, 1, True, True, True, True, True, True), testee._prepare_iterable((True, False, True), 1, 8))
        self.assertEqual((0, False, 0, 0, 0, 0, 0, 0), testee._prepare_iterable((True, False, True), -2, 0))

    def test_prepare_collection_type(self):
        with self.assertRaises(TypeError):
            testee._prepare_iterable(4, 1, 8)
        with self.assertRaises(TypeError):
            testee._prepare_iterable([], 1, 8)

    def test_header_2msgs(self):
        buf = testee.header((6, 7), (5, 3), (6, 2), (0, 1), (1, 0), 75, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 16, 254, 1, 70, 34, 34, 34, 34, 34, 34, 34, 0, 6, 0, 7, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0], buf)

    def test_header_8msgs(self):
        buf = testee.header((1, 2, 3, 4, 5, 6, 7, 8),
                            (1, 2, 3, 4, 5, 6, 7, 8),
                            (1, 2, 3, 4, 5, 6, 7, 8),
                            (0, 1, 0, 1, 0, 1, 0, 1),
                            (1, 0, 1, 0, 1, 0, 1, 0),
                            25,
                            self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 64, 170, 85, 1, 18, 35, 52, 69, 86, 103, 120, 0, 1, 0, 2, 0, 3, 0, 4, 0,
                          5, 0, 6, 0, 7, 0, 8, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0], buf)

    def test_header_brightness(self):
        buf = testee.header((6,), (4,), (4,), (0,), (0,), 25, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 64, 0, 0, 52, 52, 52, 52, 52, 52, 52, 52, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0], buf)
        buf = testee.header((6,), (4,), (4,), (0,), (0,), 26, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 32, 0, 0, 52, 52, 52, 52, 52, 52, 52, 52, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0], buf)
        buf = testee.header((6,), (4,), (4,), (0,), (0,), 60, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 16, 0, 0, 52, 52, 52, 52, 52, 52, 52, 52, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0], buf)
        buf = testee.header((6,), (4,), (4,), (0,), (0,), 80, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 0, 0, 0, 52, 52, 52, 52, 52, 52, 52, 52, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0], buf)

    def test_header_date(self):
        buf1 = testee.header((6,), (4,), (4,), (0,), (0,), 100, self.test_date)
        buf2 = testee.header((6,), (4,), (4,), (0,), (0,), 100)
        self.assertEqual(buf1[0:38], buf2[0:38])
        self.assertEqual(buf1[38 + 6:], buf2[38 + 6:])
        self.assertNotEqual(buf1[38:38 + 6], buf2[38:38 + 6])

    def test_header_type(self):
        with self.assertRaises(TypeError):
            testee.header(("nan",), (4,), (4,), (0,), (0,), 80, self.test_date)
        with self.assertRaises(ValueError):
            testee.header((370,380), (4,), (4,), (0,), (0,), 80, self.test_date)
