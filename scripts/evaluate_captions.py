"""Evaluate generated image captions using BLEU-1 and BLEU-4."""

import argparse
import json
from collections import Counter
from pathlib import Path


def tokenize(text):
    return text.lower().strip().split()


def bleu_score(reference, prediction, n=1):
    """Calculate a simple sentence-level BLEU score."""
    import math

    ref = tokenize(reference)
    pred = tokenize(prediction)

    if not ref or len(pred) < n:
        return 0.0

    precisions = []

    for k in range(1, n + 1):
        reference_ngrams = Counter(
            tuple(ref[i:i+k])
            for i in range(len(ref)-k+1)
        )
        predicted_ngrams = Counter(
            tuple(pred[i:i+k])
            for i in range(len(pred)-k+1)
        )

        total = sum(predicted_ngrams.values())
        matches = sum(
            min(count, reference_ngrams[gram])
            for gram, count in predicted_ngrams.items()
        )

        if total == 0 or matches == 0:
            return 0.0

        precisions.append(matches / total)

    brevity = min(1.0, math.exp(1 - len(ref) / len(pred)))
    return brevity * math.exp(
        sum(math.log(p) for p in precisions) / n
    )


def evaluate(records):
    if not records:
        raise ValueError("At least one caption pair is required")

    return {
        "samples": len(records),
        "bleu_1": round(sum(
            bleu_score(r["reference"], r["prediction"], 1)
            for r in records
        ) / len(records), 4),
        "bleu_4": round(sum(
            bleu_score(r["reference"], r["prediction"], 4)
            for r in records
        ) / len(records), 4),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON file with caption pairs")
    args = parser.parse_args()

    records = json.loads(Path(args.input).read_text())
    print(json.dumps(evaluate(records), indent=2))
