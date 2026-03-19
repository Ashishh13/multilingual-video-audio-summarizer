# Module Descriptions

Each Python file in the `modules/` directory fulfils a specific role in the pipeline. Understanding what each module does will help you navigate and extend the code.

| Module | Responsibility |
|---|---|
| **`config.py`** | Stores global configuration constants such as model names, chunk size, number of keywords and figure dimensions. Adjusting these values tunes the behaviour of the entire system. |
| **`utils.py`** | Provides helper functions for checking FFmpeg availability, creating directories and saving text or lists to files. |
| **`audio_extraction.py`** | Extracts or converts audio from media files. Video containers (MP4, MKV, AVI, etc.) are processed via `moviepy`, while audio files (MP3, WAV, FLAC, etc.) are converted to WAV using `pydub`. Unsupported formats raise a clear error. |
| **`speech_recognition.py`** | Wraps OpenAI’s Whisper model to perform transcription. Whisper returns both the transcribed text and a predicted language code. |
| **`cleaning.py`** | Normalises whitespace, removes redundant spacing around punctuation and splits text into sentences for subsequent processing. |
| **`lang_detect.py`** | Uses `langdetect` to determine the primary language of the cleaned transcript. Whisper’s detected language is used as a fallback. |
| **`chunking.py`** | Splits long transcripts into chunks of configurable word length (`CHUNK_SIZE`) to fit within transformer context windows. |
| **`summarization.py`** | Performs both single‑chunk and hierarchical summarisation. English summaries use the BART CNN/DailyMail model; Hindi summaries use IndicBART and fall back to translation‑based summarisation if necessary. |
| **`keywords.py`** | Implements keyword extraction using the YAKE algorithm. The number of keywords returned is configurable. |
| **`diagram.py`** | Generates a co‑occurrence graph of keywords. Nodes represent keywords and edges indicate co‑occurrence within sentences. The graph is drawn using NetworkX and Matplotlib. |
| **`file_handler.py`** | Simplifies saving transcripts, summaries, keyword lists and other artefacts by delegating to `utils.save_text` and `utils.save_list`. |
| **`__init__.py`** | Exposes a clean public API by re‑exporting functions from the modules. Users can import `modules` and access helper functions directly. |

### Front‑End

| Module | Responsibility |
|---|---|
| **`app/app.py`** | A Streamlit application that ties together all modules. It manages file uploads, orchestrates the pipeline, displays intermediate and final results, and provides download buttons for generated artefacts. |

### Jupyter Notebook

| File | Responsibility |
|---|---|
| **`notebooks/colab_pipeline.ipynb`** | A ready‑to‑run Google Colab notebook that replicates the Streamlit pipeline in a cell‑by‑cell manner. It includes dependency installation, sample file handling, pipeline execution and saving outputs to Google Drive. |
