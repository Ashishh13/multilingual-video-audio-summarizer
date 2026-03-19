# System Architecture

The project follows a **modular architecture** that separates media processing, language processing and presentation layers. This modularity not only makes the code easier to understand and test but also allows individual components to be swapped or upgraded without affecting the rest of the system.

## High‑Level Diagram

Below is a high‑level representation of the pipeline. Each box corresponds to a module in the repository.

```
┌────────────────────────────────┐      ┌─────────────────────┐      ┌───────────────────────────┐
│ Uploaded Media     │───▷│ Audio Extraction │───▷│ Speech Recognition     │
└─────────────────────────────┘      └────────────────────┘      └───────────────────────────┘
                                                      │ (Whisper)             │
                                                      └─────────┼──────────┘
                                                                │
                                                                ▼
                                                     ┌───────────────────────┐
                                                     │ Cleaning & Lang Detect  │
                                                     └─────────┼──────────┘
                                                                │
                                                                ▼
                                                     ┌───────────────────────┐
                                                     │ Chunking                │
                                                     └─────────┼──────────┘
                                                                │
                                     ┌─────────────────────────────────────────────────────────────────────────────────┐
                                     │                Hierarchical Summarisation        │
                                     │  (BART for English, IndicBART for Hindi)        │
                                     └──────┼─────────┼─────────┼────────┘
                                               │             │             │
                                               ▼             ▼             ▼
                                        Chunk summaries   Final summary   Keywords
                                               │             │             │
                                               └─────├─────┘             │
                                                      ▼                    ▼
                                         ┌──────────────┐   ┌──────────────┐
                                         │ Graph Generation  │   │ Downloads/Display │
                                         └──────────────┘   └──────────────┘
```

## Components

1. **Audio Extraction (`modules/audio_extraction.py`)** – Uses `moviepy` to extract audio from video files and `pydub` to convert various audio formats to a common WAV format. Unsupported extensions result in a clear error message.

2. **Speech Recognition (`modules/speech_recognition.py`)** – Wraps OpenAI’s Whisper model to transcribe the extracted audio. Whisper automatically detects the language and can process both English and Hindi speech.【687373803873561†L62-L69】

3. **Cleaning (`modules/cleaning.py`)** – Normalises whitespace and punctuation in the transcript and provides a simple sentence splitter used by the diagram module.

4. **Language Detection (`modules/lang_detect.py`)** – Utilises the `langdetect` library to double‑check the language of the cleaned transcript. The detection result decides which summarisation model to employ.

5. **Chunking (`modules/chunking.py`)** – Splits long transcripts into manageable chunks to avoid exceeding transformer context limits. The `CHUNK_SIZE` parameter in `config.py` can be adjusted.

6. **Summarisation (`modules/summarization.py`)** – Implements both single‑chunk and hierarchical summarisation. English summaries are generated with the BART CNN/DailyMail model, while Hindi summaries use the IndicBART checkpoint trained on 11 Indic languages【687373803873561†L62-L69】. If the Hindi model cannot be loaded, the text is translated to English, summarised, and translated back using MarianMT models.

7. **Keyword Extraction (`modules/keywords.py`)** – Applies the YAKE algorithm to extract top keywords from the transcript. YAKE works for multiple languages and does not require training data.

8. **Diagram Generation (`modules/diagram.py`)** – Builds a co‑occurrence graph of keywords based on sentence‑level co‑occurrence. The graph is rendered with NetworkX and Matplotlib.

9. **File Handling (`modules/file_handler.py` & `modules/utils.py`)** – Provides convenient wrappers around saving text files and ensures output directories exist.

10. **Streamlit Front‑End (`app/app.py`)** – Orchestrates the pipeline, displays progress via spinners, shows intermediate and final results, and exposes download buttons for all generated artefacts.

11. **Jupyter/Colab Notebook (`notebooks/colab_pipeline.ipynb`)** – Contains an alternative way to run the pipeline in a notebook environment. This is particularly useful for environments like Google Colab where installing desktop applications is not possible.

## Extensibility

Because each component is isolated, replacing a model (for example, using mT5 instead of BART, or a different keyword extractor) only requires editing a single module. The rest of the system remains unaffected. This design makes the project an excellent starting point for experimentation and future enhancements.
