"""
Text chunking module.

Summarisation models like BART and IndicBART have fixed context windows
that limit the number of tokens they can process in a single pass. To
handle transcripts longer than a few hundred words we divide the text
into smaller chunks. Each chunk is summarised individually and the
partial summaries are then combined for a final summary (hierarchical
summarisation).
"""

from typing import List


def chunk_text(text: str, max_words: int) -> List[str]:
    """Split text into chunks of approximately ``max_words`` words.

    Parameters
    ----------
    text : str
        The input document to split.
    max_words : int
        Maximum number of words per chunk.

    Returns
    -------
    List[str]
        A list of text chunks.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk_words = words[i : i + max_words]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
    return chunks
