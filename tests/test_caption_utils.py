import unittest

from utils.caption_utils import clean_caption, word_count


class TestCaptionUtils(unittest.TestCase):

    def test_clean_caption(self):
        self.assertEqual(
            clean_caption("  A   dog  running  "),
            "A dog running"
        )

    def test_word_count(self):
        self.assertEqual(word_count("A dog running"), 3)

    def test_empty_caption(self):
        self.assertEqual(word_count("   "), 0)


if __name__ == "__main__":
    unittest.main()
