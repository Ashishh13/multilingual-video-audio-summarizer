"""
Language detection module.

Although Whisper returns a language prediction, we still perform a second
check using ``langdetect`` to confirm the detected language of the text.
This redundancy helps us handle edge cases where Whisper might mislabel
short clips. The library returns ISO-639 two letter codes, which are
passed into downstream modules.
"""

from typing import Optional

from langdetect import detect, DetectorFactory

# Ensure consistent results between runs
DetectorFactory.seed = 0


def detect_language(text: str) -> Optional[str]:
    """Detect the primary language of the provided text.

    Parameters
    ----------
    text : str
        Input text to analyse.

    Returns
    -------
    str or None
        Two letter language code (e.g. 'en', 'hi') or None if detection
        fails.
    """
    try:
        lang = detect(text)
        return lang
    except Exception:
        return None
