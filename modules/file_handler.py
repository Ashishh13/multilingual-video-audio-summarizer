"""
File management helpers.

These functions wrap common file operations, such as saving
transcripts, summaries and keyword lists, into human friendly API calls.
Internally they defer to ``utils`` for path creation and write
operations. Keeping them in a separate module makes the app code
simpler to read and modify.
"""
from typing import List

from .utils import save_text, save_list


def save_transcript(text: str, path: str) -> None:
    """Save the raw transcript to a file."""
    save_text(text, path)


def save_clean_transcript(text: str, path: str) -> None:
    """Save the cleaned transcript to a file."""
    save_text(text, path)


def save_chunk_summaries(chunks: List[str], path: str) -> None:
    """Save intermediate chunk summaries to a file."""
    save_list(chunks, path)


def save_final_summary(summary: str, path: str) -> None:
    """Save the final summary to a file."""
    save_text(summary, path)


def save_keywords(keywords: List[str], path: str) -> None:
    """Save extracted keywords to a file."""
    save_list(keywords, path)
