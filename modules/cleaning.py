"""
Text cleaning and preprocessing.

After transcription, transcripts often contain extra whitespace, line
breaks and filler tokens that can degrade summarisation quality. This
module provides functions to normalise the text prior to further
processing. Cleaning is deliberately conservative – we avoid
language‑specific removals so the same code can work for English and
Hindi.
"""

import re
from typing import List


def clean_text(text: str) -> str:
    """Normalize whitespace and remove stray characters.

    Parameters
    ----------
    text : str
        Raw transcript from Whisper.

    Returns
    -------
    str
        Cleaned and normalised text ready for tokenisation.
    """
    # Replace newlines with spaces
    cleaned = re.sub(r"\s+", " ", text)
    # Remove extraneous spaces around punctuation
    cleaned = re.sub(r"\s+([,.!?])", r"\1", cleaned)
    return cleaned.strip()


def split_sentences(text: str) -> List[str]:
    """Rudimentary sentence segmentation based on punctuation.

    Splits the text on Hindi and English sentence delimiters. This is
    intentionally simple to avoid heavy dependencies; it may misplace
    some boundaries but is sufficient for building co‑occurrence graphs.

    Parameters
    ----------
    text : str

    Returns
    -------
    List[str]
        A list of sentences.
    """
    # Use full stops, question marks and exclamation marks for segmentation
    sentences = re.split(r"(?<=[\.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]
