from array import array
from unittest import TestCase

from lednamebadge import SimpleTextAndIcons as testee


class Test(TestCase):
    def test_bitmap_png(self):
        creator = testee()
        buf = creator.bitmap("resources/bitpatterns.png")
        self.assertEqual((array('B',
                                [128, 64, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 64, 32, 0, 1, 2, 3,
                                 4, 5, 15, 31, 63, 127, 255]),
                          3), buf)

    def test_bitmap_text(self):
        creator = testee()
        buf = creator.bitmap("/:HEART2:\\")
        self.assertEqual((array('B',
                                [0, 0, 2, 6, 12, 24, 48, 96, 192, 128, 0, 0, 12, 30, 63, 63, 63, 31, 15, 7, 3, 1, 0, 96,
                                 240, 248, 248, 248, 240, 224, 192, 128, 0, 0, 128, 192, 96, 48, 24, 12, 6, 2, 0, 0]),
                          4), buf)

    def test_preload(self):
        creator = testee()
        self.assertFalse(creator.are_preloaded_unused())
        creator.add_preload_img("resources/bitpatterns.png")
        self.assertTrue(creator.are_preloaded_unused())
        buf = creator.bitmap("\x01")
        self.assertFalse(creator.are_preloaded_unused())
        self.assertEqual((array('B',
                                [128, 64, 32, 16, 8, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 64, 32, 0, 1, 2, 3,
                                 4, 5, 15, 31, 63, 127, 255]),
                          3), buf)
