"""
Speech recognition module using OpenAI Whisper.

This module wraps the Whisper ASR model to perform multilingual
transcription of audio files. The ``transcribe_audio`` function returns
both the raw transcript and the language predicted by Whisper so that
downstream processes can adapt accordingly.

The Whisper paper and implementation describe how the model supports
automatic language detection and high quality transcription across many
languages, including English and Hindi【687373803873561†L62-L70】.
"""

import os
from typing import Tuple, Optional

import whisper

from .config import WHISPER_MODEL_SIZE


_whisper_model: Optional[whisper.Whisper] = None


def _load_model() -> whisper.Whisper:
    """Load and cache the Whisper model so repeated calls do not reload it."""
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
    return _whisper_model


def transcribe_audio(audio_path: str, language: Optional[str] = None) -> Tuple[str, Optional[str]]:
    """Transcribe an audio file to text using Whisper.

    Parameters
    ----------
    audio_path : str
        Path to a WAV audio file.
    language : str, optional
        Two‑letter language code to hint the model; if None, Whisper
        auto‑detects the language.

    Returns
    -------
    transcript : str
        The transcribed text.
    detected_language : Optional[str]
        Language detected by Whisper (may be None if not returned).
    """
    model = _load_model()
    # Whisper can take a language hint which speeds up transcription; we pass
    # it through if provided, otherwise detection happens automatically.
    result = model.transcribe(audio_path, fp16=False, language=language)
    transcript = result.get("text", "").strip()
    detected_lang = result.get("language")
    return transcript, detected_lang
