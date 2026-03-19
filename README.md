# Multilingual Smart Summarization from Video and Audio

## 📙 Overview

This project delivers an end‑to‑end pipeline for extracting, transcribing, summarising and analysing speech from audio or video files. It supports **English** and **Hindi** content, generates hierarchical summaries, extracts keywords using YAKE and visualises relationships between those keywords via a co‑occurrence graph. The entire pipeline is wrapped in a Streamlit application and accompanied by a Google Colab notebook.

Motivated by the lack of open‑source tools for summarising non‑English speech, the project uses OpenAI’s Whisper for transcription and the IndicBART checkpoint for Hindi summarisation. IndicBART was trained on multiple Indic languages and is lighter than mBART and mT5 models【687373803873561†L62-L69】. The fallback path translates Hindi to English, summarises it with BART and translates back to Hindi if required.

## ✨ Features

- **Media agnostic:** Accepts MP3, WAV, MP4, M4A, FLAC, AVI, MKV, MOV, FLV and WebM files.
- **Multilingual:** Supports English and Hindi transcripts; uses language detection to choose the appropriate summarisation model.
- **Hierarchical summarisation:** Splits long transcripts into chunks and summarises them recursively to respect model context limits.
- **Keyword extraction:** Uses YAKE to find salient terms in the transcript.
- **Graph visualisation:** Builds a keyword co‑occurrence graph with NetworkX and Matplotlib.
- **Streamlit UI:** Upload a file, view progress, read summaries and download the outputs.
- **Colab notebook:** Run the pipeline in Google Colab, complete with Drive integration.
- **Modular code:** Each stage of the pipeline is encapsulated in its own module, making the repository easy to read and extend.

## 📁 Folder Structure

```
multilingual-video-audio-summarizer/
│  README.md            – project overview and instructions
│  requirements.txt      – Python dependencies
│  LICENSE               – MIT license
│  .gitignore            – files and directories to ignore
├─ app/
│   └─ app.py           – Streamlit application entry point
├─ modules/
│   ├─ __init__.py      – exposes key functions
│   ├─ audio_extraction.py – extract/convert audio to WAV
│   ├─ speech_recognition.py – transcribe audio using Whisper
│   ├─ cleaning.py       – normalise and split transcript
│   ├─ lang_detect.py    – detect language via langdetect
│   ├─ chunking.py       – split long texts into chunks
│   ├─ summarization.py  – hierarchical summarisation logic
│   ├─ keywords.py       – keyword extraction via YAKE
│   ├─ diagram.py        – keyword co‑occurrence graph generation
│   ├─ file_handler.py   – helper functions to save outputs
│   ├─ config.py        – global settings
│   └─ utils.py          – general utility functions
├─ docs/
│   ├─ overview.md      – high‑level project description
│   ├─ system_architecture.md – architecture diagram & explanation
│   ├─ workflow.md      – step‑by‑step pipeline description
│   ├─ module_descriptions.md – breakdown of each module
│   ├─ troubleshooting.md – common issues and fixes
│   ├─ report.md        – final project report
│   └─ viva_questions.md – potential viva questions and answers
├─ notebooks/
│   └─ colab_pipeline.ipynb – Colab demonstration of the pipeline
├─ sample_data/
│   └─ README.md        – guidance on preparing sample files
├─ outputs/
│   └─ (generated files) – transcripts, summaries, keywords and graphs
└─ tests/
    └─ test_basic.py    – simple tests for helper functions
```

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multilingual-video-audio-summarizer.git
   cd multilingual-video-audio-summarizer
   ```

2. **Create a Python virtual environment (optional but recommended)**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\\Scripts\\activate`
   ```

3. **Install Python dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Install FFmpeg** (if not already installed)

   - **Ubuntu/Debian:** `sudo apt-get update && sudo apt-get install ffmpeg`
   - **macOS (Homebrew):** `brew install ffmpeg`
   - **Windows:** Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html), extract it and add the `bin` directory to your system `PATH`.

## 🏃‍♂️ Running the Streamlit App

After installation, start the Streamlit application:

```bash
streamlit run app/app.py
```

1. A web browser will open automatically.
2. Upload an audio or video file using the file uploader.
3. Click **Process file** to run the pipeline.
4. View the transcript, summary, keywords and keyword graph.
5. Download the results using the provided buttons.

## 📝 Running in Google Colab

1. Open `notebooks/colab_pipeline.ipynb` in Google Colab.
2. Follow the cell instructions to install dependencies, mount Google Drive and run the pipeline on a sample file stored in your Drive.
3. Outputs will be saved back to your Drive.

## ✅ Running Tests

Basic sanity checks are provided in `tests/test_basic.py`. To run them:

```bash
pytest -q
```

These tests verify that helper functions behave as expected. They do not load heavy models and therefore run quickly.

## 🛠️ Deployment

The app can be deployed on the **Streamlit Community Cloud** or **Hugging Face Spaces**. Ensure that the environment installs the required packages and has FFmpeg available. On Streamlit Cloud you can specify dependencies in `requirements.txt` and use the provided `app/app.py` as the entry point. For Spaces, create a `space.yml` file pointing to the Streamlit script.

## 📍 Usage Notes

* **Performance:** Summarisation models are resource intensive. Running on a GPU is recommended for long files.
* **File Size:** Large video files can take a long time to upload and process. For demonstrations, use shorter clips (<1 minute).
* **Hindi Summarisation:** The IndicBART model is loaded on demand. If it cannot be loaded due to memory constraints, the pipeline automatically translates the Hindi text to English, summarises it with BART and translates back to Hindi.

## 📑 References

* IndicBART summarisation model card【687373803873561†L62-L69】
* CrossSum mT5 Hindi summarisation description【879896779544012†L50-L53】

---

Made with ❤️ by Ashish Singh
