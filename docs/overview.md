# Project Overview

## Introduction

**Multilingual Smart Summarization from Video and Audio with Diagrammatic Representation** is a final‑year student project that demonstrates how modern natural language processing can be combined with multimedia handling to extract knowledge from spoken content. The application ingests an audio or video file, transcribes the speech, cleans and analyses the resulting text, summarises the material hierarchically, extracts keywords, and finally visualises relationships between those keywords as a graph. The pipeline supports both **English and Hindi**, making it suitable for users in multilingual settings.

## Motivation

Students and professionals often need to understand lengthy lectures, interviews or news reports quickly. Manual transcription and summarisation are time‑consuming and prone to errors. Automatic summarisation systems exist for English, but resources for Indic languages like Hindi remain scarce. This project bridges that gap by combining open‑source models to support both languages. The Hindi summarisation model is based on the **IndicBARTSS checkpoint**, which was fine‑tuned on 11 Indic languages and is more efficient than mBART or mT5 models【687373803873561†L62-L69】. For English, the well‑known BART CNN/DailyMail model is used. When the Hindi model cannot be loaded, the pipeline falls back to translating Hindi to English, summarising, then translating back to Hindi.

## Features

* **Media agnostic** – accepts video (MP4, MKV, AVI, MOV, FLV, WebM) and audio (MP3, WAV, FLAC, M4A, AAC, OGG) files.
* **Robust audio extraction** – leverages `moviepy` and `pydub` to extract or convert audio to WAV format.
* **Multilingual speech recognition** – uses OpenAI’s Whisper model to transcribe speech and detect the spoken language automatically.
* **Language detection redundancy** – applies the `langdetect` library on the cleaned transcript to confirm the primary language.
* **Hierarchical summarisation** – splits long transcripts into manageable chunks and summarises them individually before producing a final summary. English summarisation is powered by BART, while Hindi summarisation uses IndicBART or a translate–summarise–translate fallback.
* **Keyword extraction** – employs the YAKE algorithm to extract salient keywords from the transcript in a language‑independent manner.
* **Diagrammatic representation** – builds a keyword co‑occurrence graph using NetworkX and Matplotlib to visualise relationships between concepts.
* **Streamlit interface** – provides an intuitive web interface with file upload, progress indicators, expandable summaries, keyword display, interactive graph and download buttons.
* **Colab compatibility** – includes a Jupyter notebook that can be run in Google Colab, complete with installation steps and Drive integration for saving outputs.
* **Modular design** – separates concerns into well‑documented Python modules for ease of understanding and future extension.

## Target Users

The application targets students, educators and researchers who need quick insights from recorded lectures, podcasts or interviews. It also demonstrates to examiners how state‑of‑the‑art machine learning can be applied to practical problems while maintaining code readability and robustness.
