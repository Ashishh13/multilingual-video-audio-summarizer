"""
Expose key functions and classes from the modules package.

By defining an ``__all__`` list we allow users of this package to
import functions directly from ``modules`` without specifying the
submodule. This file also ensures the directory is recognised as a
Python package.
"""

from .audio_extraction import extract_audio  # noqa: F401
from .speech_recognition import transcribe_audio  # noqa: F401
from .cleaning import clean_text, split_sentences  # noqa: F401
from .lang_detect import detect_language  # noqa: F401
from .chunking import chunk_text  # noqa: F401
from .summarization import summarize_chunk, hierarchical_summarize  # noqa: F401
from .keywords import extract_keywords  # noqa: F401
from .diagram import build_keyword_graph  # noqa: F401
from .file_handler import (  # noqa: F401
    save_transcript,
    save_clean_transcript,
    save_chunk_summaries,
    save_final_summary,
    save_keywords,
)

__all__ = [
    "extract_audio",
    "transcribe_audio",
    "clean_text",
    "split_sentences",
    "detect_language",
    "chunk_text",
    "summarize_chunk",
    "hierarchical_summarize",
    "extract_keywords",
    "build_keyword_graph",
    "save_transcript",
    "save_clean_transcript",
    "save_chunk_summaries",
    "save_final_summary",
    "save_keywords",
]
