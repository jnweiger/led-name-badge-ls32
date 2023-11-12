import datetime
import importlib
from array import array
from unittest import TestCase

testee = importlib.import_module("led-badge-11x44")


class Test(TestCase):
    def setUp(self):
        self.test_date = datetime.datetime(2022, 11, 13, 17, 38, 24)

    def test_header_2msgs(self):
        buf = testee.LedNameBadge.header((6, 7), (5, 3), (6, 2), (0, 1), (1, 0), 75, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 16, 254, 1, 70, 34, 34, 34, 34, 34, 34, 34, 0, 6, 0, 7, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0], buf)

    def test_header_8msgs(self):
        buf = testee.LedNameBadge.header((1, 2, 3, 4, 5, 6, 7, 8),
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
        buf = testee.LedNameBadge.header((6,), (4,), (4,), (0,), (0,), 25, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 64, 0, 0, 52, 52, 52, 52, 52, 52, 52, 52, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0], buf)
        buf = testee.LedNameBadge.header((6,), (4,), (4,), (0,), (0,), 26, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 32, 0, 0, 52, 52, 52, 52, 52, 52, 52, 52, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0], buf)
        buf = testee.LedNameBadge.header((6,), (4,), (4,), (0,), (0,), 60, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 16, 0, 0, 52, 52, 52, 52, 52, 52, 52, 52, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0], buf)
        buf = testee.LedNameBadge.header((6,), (4,), (4,), (0,), (0,), 80, self.test_date)
        self.assertEqual([119, 97, 110, 103, 0, 0, 0, 0, 52, 52, 52, 52, 52, 52, 52, 52, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 11, 13, 17, 38, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0], buf)

    def test_header_date(self):
        buf1 = testee.LedNameBadge.header((6,), (4,), (4,), (0,), (0,), 100, self.test_date)
        buf2 = testee.LedNameBadge.header((6,), (4,), (4,), (0,), (0,), 100)
        self.assertEqual(buf1[0:38], buf2[0:38])
        self.assertEqual(buf1[38 + 6:], buf2[38 + 6:])
        self.assertNotEqual(buf1[38:38 + 6], buf2[38:38 + 6])

    def test_bitmap_png(self):
        creator = testee.SimpleTextAndIcons()
        buf = creator.bitmap("resources/bitpatterns.png")
        self.assertEqual((array('B',
                                [128, 64, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 64, 32, 0, 1, 2, 3,
                                 4, 5, 15, 31, 63, 127, 255]),
                          3), buf)

    def test_bitmap_text(self):
        creator = testee.SimpleTextAndIcons()
        buf = creator.bitmap("/:HEART2:\\")
        self.assertEqual((array('B',
                                [0, 0, 2, 6, 12, 24, 48, 96, 192, 128, 0, 0, 12, 30, 63, 63, 63, 31, 15, 7, 3, 1, 0, 96,
                                 240, 248, 248, 248, 240, 224, 192, 128, 0, 0, 128, 192, 96, 48, 24, 12, 6, 2, 0, 0]),
                          4), buf)

    def test_preload(self):
        creator = testee.SimpleTextAndIcons()
        self.assertFalse(creator.are_preloaded_unused())
        creator.add_preload_img("resources/bitpatterns.png")
        self.assertTrue(creator.are_preloaded_unused())
        buf = creator.bitmap("\x01")
        self.assertFalse(creator.are_preloaded_unused())
        self.assertEqual((array('B',
                                [128, 64, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 64, 32, 0, 1, 2, 3,
                                 4, 5, 15, 31, 63, 127, 255]),
                          3), buf)
