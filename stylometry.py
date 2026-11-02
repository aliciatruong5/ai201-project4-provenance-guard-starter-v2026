"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies: standard deviation of sentence lengths in
    words, divided by their mean (the coefficient of variation), so a long text
    and a short one are comparable.

    Scale: 0.0 means every sentence is the same length. Real prose runs roughly
    0.3 to 0.9. HIGHER means more human-looking.

    A one-sentence text has no spread, and `stdev` raises on fewer than two
    values. It returns 0.0 here; `style_signal` checks the sentence count
    itself and treats that case as "can't tell" instead of "looks like AI".
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean


def type_token_ratio(text: str, window: int = 50) -> float:
    """
    Unique words over total words, between 0 and 1. HIGHER means more varied
    vocabulary, which reads as more human.

    A plain ratio falls as text gets longer, because common words repeat, which
    would make a long human text look machine-like on length alone. So this is
    measured over a sliding window of `window` words and averaged. Text shorter
    than the window falls back to the plain ratio.
    """
    ws = words(text)
    if not ws:
        return 0.0
    if len(ws) <= window:
        return len(set(ws)) / len(ws)
    ratios = [
        len(set(ws[i:i + window])) / window
        for i in range(len(ws) - window + 1)
    ]
    return sum(ratios) / len(ratios)


# Marks that vary between writers. Full stops are left out on purpose: nearly
# every sentence has one, so they say nothing about the writer.
_VARIED_MARKS = set(",;:()!?\u2014\u2013-\"")


def punctuation_density(text: str) -> float:
    """
    Commas, semicolons, colons, brackets, dashes, quotes and ! ? per word.
    HIGHER means more punctuation, which reads as more human here.

    Typical prose runs roughly 0.05 to 0.35. Returns 0.0 for text with no words.
    """
    n_words = len(words(text))
    if n_words == 0:
        return 0.0
    marks = sum(1 for ch in text if ch in _VARIED_MARKS)
    return marks / n_words


# ── Combining them ───────────────────────────────────────────────────────────

def _clamp(x: float) -> float:
    return min(max(x, 0.0), 1.0)


# How much each measure counts. Sentence rhythm is the strongest of the three;
# punctuation is the weakest, since plenty of people write with little of it.
_WEIGHTS = {"spread": 0.5, "ttr": 0.3, "punct": 0.2}

# Each measure maps onto "how AI-like", 0 (human-looking) to 1 (AI-looking):
#   spread:  CV 0.0 -> 1.0, CV 0.7 or more -> 0.0
#   ttr:     0.95 -> 0.0, 0.60 or less -> 1.0
#   punct:   0.0 per word -> 1.0, 0.30 or more -> 0.0
# These cut-offs are first guesses from reading typical values, not fitted
# numbers. Milestone 4's calibration inputs are where they get checked.
_SPREAD_FULL = 0.7
_TTR_HUMAN, _TTR_AI = 0.95, 0.60
_PUNCT_FULL = 0.30


def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. **Higher means more likely AI.**

    Each of the three measures is flipped where needed (all three read
    "higher = more human" on their own) and put on a 0-1 scale, then they are
    averaged with the weights above. With fewer than two sentences there is no
    rhythm to measure, so that measure is left out and the other two are
    re-weighted. With no words at all the answer is 0.5, meaning "can't tell".
    """
    if not words(text):
        return 0.5

    parts = {
        "ttr": _clamp((_TTR_HUMAN - type_token_ratio(text)) / (_TTR_HUMAN - _TTR_AI)),
        "punct": _clamp(1.0 - punctuation_density(text) / _PUNCT_FULL),
    }
    if len(sentences(text)) >= 2:
        parts["spread"] = _clamp(1.0 - sentence_length_spread(text) / _SPREAD_FULL)

    total_weight = sum(_WEIGHTS[k] for k in parts)
    score = sum(_WEIGHTS[k] * v for k, v in parts.items()) / total_weight
    return round(_clamp(score), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
