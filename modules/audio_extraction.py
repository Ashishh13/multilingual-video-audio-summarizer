"""
Audio extraction module.

This module extracts or converts audio from supported media files into WAV format.
It uses MoviePy for video files and FFmpeg directly for audio conversion, which
avoids pydub compatibility issues on some Python versions.
"""

import os
import subprocess
from typing import Optional

from moviepy.editor import VideoFileClip


def extract_audio(input_path: str, output_path: Optional[str] = None) -> str:
    """
    Extract or convert audio to WAV format from a video or audio file.

    Parameters
    ----------
    input_path : str
        Path to the source media file.
    output_path : str, optional
        Path for the extracted WAV file.

    Returns
    -------
    str
        Absolute path to the extracted WAV file.
    """
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.wav"

    ext = os.path.splitext(input_path)[1].lower()

    try:
        if ext in [".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm"]:
            clip = VideoFileClip(input_path)
            clip.audio.write_audiofile(output_path, codec="pcm_s16le")
            clip.close()

        elif ext in [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"]:
            command = [
                "ffmpeg",
                "-y",
                "-i",
                input_path,
                output_path
            ]
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                raise ValueError(result.stderr)

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        raise ValueError(f"Failed to extract audio: {e}")

    return os.path.abspath(output_path)
