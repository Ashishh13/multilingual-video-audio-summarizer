"""
Audio extraction module.

This module provides functions to extract or convert audio from a variety
of input formats. Videos are handled via ``moviepy``, while audio files
are converted to the desired format using ``pydub``. The functions here
return the path to the generated audio file so downstream modules can
operate on it without caring about the original container.
"""

import os
import shutil
import subprocess
from typing import Optional

from moviepy.editor import VideoFileClip
from pydub import AudioSegment

from .utils import ensure_dir


def extract_audio(input_path: str, output_path: Optional[str] = None) -> str:
    """Extract or convert audio to WAV format from a video or audio file.

    Parameters
    ----------
    input_path: str
        Path to the source media file (video or audio).
    output_path: str, optional
        Path where the resulting WAV file should be written. If omitted,
        the file will be saved next to the input with a ``.wav`` suffix.

    Returns
    -------
    str
        The absolute path to the extracted WAV file.

    Raises
    ------
    ValueError
        If the file format is unsupported or extraction fails.
    """
    ensure_dir(os.path.dirname(os.path.abspath(input_path)))
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.wav"

    ext = os.path.splitext(input_path)[1].lower()
    try:
        if ext in [".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm"]:
            # Use moviepy to extract audio from video
            clip = VideoFileClip(input_path)
            clip.audio.write_audiofile(output_path, codec="pcm_s16le")
            clip.reader.close()
            clip.audio.reader.close()
        elif ext in [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"]:
            # Use pydub to convert various audio types to wav
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format="wav")
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        raise ValueError(f"Failed to extract audio: {e}")

    return os.path.abspath(output_path)
