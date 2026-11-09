import unittest

from scripts.evaluate_captions import bleu_score, evaluate


class TestCaptionEvaluation(unittest.TestCase):

    def test_identical_caption(self):
        caption = "a dog runs across the green field"
        self.assertAlmostEqual(bleu_score(caption, caption, 4), 1.0)

    def test_unrelated_caption(self):
        self.assertEqual(
            bleu_score("a dog runs", "the sky shines", 1),
            0.0,
        )

    def test_evaluate(self):
        result = evaluate([
            {
                "reference": "a cat sits on the table",
                "prediction": "a cat sits on the table",
            }
        ])
        self.assertEqual(result["samples"], 1)
        self.assertEqual(result["bleu_1"], 1.0)
        self.assertEqual(result["bleu_4"], 1.0)


if __name__ == "__main__":
    unittest.main()
