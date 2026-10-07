import json
from pathlib import Path

HIGH_SCORE_PATH = Path(__file__).resolve().parent.parent / "high_scores.json"


def _valid_scores(scores):
    if not isinstance(scores, list):
        return []
    return sorted(
        (score for score in scores if isinstance(score, int) and not isinstance(score, bool) and score >= 0),
        reverse=True,
    )[:5]


def load_high_scores(path=HIGH_SCORE_PATH):
    try:
        with path.open(encoding="utf-8") as score_file:
            return _valid_scores(json.load(score_file))
    except (OSError, json.JSONDecodeError):
        return []


def save_high_scores(scores, path=HIGH_SCORE_PATH):
    try:
        with path.open("w", encoding="utf-8") as score_file:
            json.dump(_valid_scores(scores), score_file)
        return True
    except OSError:
        return False