# Troubleshooting

Running a machine‑learning pipeline that involves audio extraction, speech recognition and summarisation can occasionally lead to issues. This section lists common problems and how to resolve them.

## FFmpeg Not Found

**Symptoms:** Audio extraction fails with an error such as `moviepy.audio.io.audio_reader.AudioFileClip: No such file or directory` or `OSError: ffmpeg not found`.

**Solution:** FFmpeg is required by `moviepy` and `pydub` to read and write media files. Install it using one of the following methods:

* **Windows:** Download the FFmpeg build from [ffmpeg.org](https://ffmpeg.org/download.html), extract it and add the `bin` directory to your `PATH` environment variable.
* **Linux (Debian/Ubuntu):** `sudo apt‑get update && sudo apt‑get install ffmpeg`
* **macOS (Homebrew):** `brew install ffmpeg`

After installation restart your terminal or IDE so the new path is recognised.

## Unsupported File Type

**Symptoms:** The application raises `ValueError: Unsupported file type` when you upload a file.

**Solution:** Ensure your media file has one of the supported extensions: MP3, WAV, MP4, M4A, FLAC, AVI, MKV, MOV, FLV or WebM. If your file uses another container (e.g. `.wmv` or `.aac`), convert it to a supported format using FFmpeg: `ffmpeg -i input.wmv output.mp4`.

## Empty Transcript

**Symptoms:** Whisper returns an empty transcript or only whitespace.

**Solution:** Check that the audio contains audible speech and is not silent or corrupted. Also ensure the volume is sufficiently loud and there is minimal background noise. If Whisper still fails, try the `medium` or `large` Whisper models by changing `WHISPER_MODEL_SIZE` in `modules/config.py`.

## Slow Summarisation

**Symptoms:** The summarisation step takes a very long time or runs out of memory.

**Solution:** Transformer models such as BART and IndicBART are computationally intensive. Running them on a CPU will be slow for long transcripts. Consider the following:

* Use shorter input files or increase the `CHUNK_SIZE` to reduce the number of summarisation calls.
* Run the application on a machine with a GPU. The code automatically selects GPU (`device=0`) if available.
* Use a smaller Whisper model to reduce transcription time. The default is `small`; try `base` or `tiny` for faster performance.
* When summarising Hindi content, if the IndicBART model is too large for your environment, allow the translate‑summarise‑translate fallback to handle the summarisation.

## Model Loading Errors

**Symptoms:** Errors such as `OSError: Can't load model` or `OutOfMemoryError` appear when loading summarisation or translation models.

**Solution:**

* Ensure you have a stable internet connection during the first run so that Hugging Face models can be downloaded.
* Try clearing the Hugging Face cache at `~/.cache/huggingface` if corrupted.
* If memory is limited, consider using smaller models or running the pipeline in Google Colab with a free GPU.

## Streamlit App Not Launching

**Symptoms:** Running `streamlit run app/app.py` results in an error.

**Solution:** Make sure you have installed all dependencies using `pip install -r requirements.txt`. If the error persists, upgrade Streamlit (`pip install --upgrade streamlit`) and clear the Streamlit cache using `streamlit cache clear`.

## No Keywords Extracted

**Symptoms:** The keyword extraction step returns an empty list.

**Solution:** YAKE may struggle with extremely short or repetitive transcripts. Increase the length of the input or adjust the `MAX_KEYWORDS` parameter in `config.py`. Alternatively, try the fallback summarisation pipeline; translation into English may allow YAKE to extract English keywords successfully.
