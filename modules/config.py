"""
Global configuration for the Multilingual Smart Summarization project.

This module centralises common constants so they can be easily tweaked
without touching individual parts of the pipeline. You can adjust model
names, chunk sizes and output paths here. Keeping configuration in one
place makes the code base more maintainable and beginner friendly.
"""

import os

# Base project directory (the parent of the `modules` folder)
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory where all generated files will be stored. You can change this
# to an absolute path if you prefer to keep outputs elsewhere.
OUTPUT_DIR: str = os.path.join(BASE_DIR, "outputs")

# Whisper model size – choose from tiny, base, small, medium, large
# A smaller model will be faster at the cost of slightly lower accuracy.
WHISPER_MODEL_SIZE: str = "small"

# Summarisation models
# English summarisation model (BART-large fine‑tuned on CNN/DailyMail)
ENGLISH_SUMMARY_MODEL: str = "facebook/bart-large-cnn"

# Hindi summarisation model (IndicBART checkpoint fine‑tuned on multiple
# Indic languages). According to the model card, this checkpoint supports
# Assamese, Bengali, Gujarati, Hindi, Marathi, Odiya, Punjabi, Kannada,
# Malayalam, Tamil and Telugu languages and is less expensive to decode
# than mBART or mT5【687373803873561†L62-L69】.
HINDI_SUMMARY_MODEL: str = "ai4bharat/MultiIndicSentenceSummarizationSS"

# Chunk size for hierarchical summarisation (in approximate word count).
# Long transcripts are split into chunks of this many words before
# summarisation to avoid exceeding model context lengths.
CHUNK_SIZE: int = 500

# Maximum number of keywords to extract from the transcript
MAX_KEYWORDS: int = 10

# Figure settings for diagrams
FIGURE_WIDTH: int = 10
FIGURE_HEIGHT: int = 8

# Ensure output directory exists on import
os.makedirs(OUTPUT_DIR, exist_ok=True)
