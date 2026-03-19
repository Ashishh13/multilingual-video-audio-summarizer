"""
Basic sanity tests for the modules.

These tests can be run locally with ``pytest -q``. They verify that
helper functions behave as expected on small inputs without loading
heavy models. To keep CI fast and requirements modest, we avoid
invoking Whisper or the summarisation models here.
"""
import os

from modules.cleaning import clean_text
from modules.chunking import chunk_text
from modules.keywords import extract_keywords
from modules.diagram import build_keyword_graph


def test_clean_text_normalises_whitespace():
    raw = "Hello\n\nworld!  This   is    a test."
    cleaned = clean_text(raw)
    assert cleaned == "Hello world! This is a test."


def test_chunk_text_splits_correctly():
    text = " ".join(["word"] * 1050)
    chunks = chunk_text(text, max_words=500)
    assert len(chunks) == 3
    assert all(len(chunk.split()) <= 500 for chunk in chunks)


def test_keyword_extraction_returns_list():
    text = "This is a test document. This document contains important information about tests."
    keywords = extract_keywords(text, language="en", max_keywords=5)
    assert isinstance(keywords, list)
    assert len(keywords) <= 5


def test_graph_creation(tmp_path):
    keywords = ["test", "document"]
    text = "This is a test document. Another test document here."
    out_path = os.path.join(tmp_path, "graph.png")
    result_path = build_keyword_graph(keywords, text, out_path)
    assert os.path.exists(result_path)
