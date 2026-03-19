"""
Keyword and topic extraction module.

This module provides functions for extracting salient keywords from a
document using the YAKE (Yet Another Keyword Extractor) algorithm. YAKE
is an unsupervised, language‑independent method based on simple term
co‑occurrence statistics. It performs well on both English and Hindi
without requiring any training data or language‑specific resources.
"""

from typing import List

import yake

from .config import MAX_KEYWORDS


def extract_keywords(text: str, language: str, max_keywords: int = MAX_KEYWORDS) -> List[str]:
    """Extract the top N keywords from the given text using YAKE.

    Parameters
    ----------
    text : str
        Input document.
    language : str
        Two letter ISO code ('en' or 'hi') passed to YAKE to improve
        stopword handling.
    max_keywords : int
        Maximum number of keywords to return.

    Returns
    -------
    List[str]
        A list of keywords sorted by importance (most important first).
    """
    # YAKE expects the language code without dialects
    lan = language if language in {"en", "hi"} else "en"
    extractor = yake.KeywordExtractor(lan=lan, n=1, top=max_keywords)
    keywords = extractor.extract_keywords(text)
    # The library returns (keyword, score) pairs; lower scores mean more
    # important keywords. Sort by score ascending and return only keywords.
    sorted_kw = sorted(keywords, key=lambda x: x[1])
    return [kw for kw, score in sorted_kw[:max_keywords]]
