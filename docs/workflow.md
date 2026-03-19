# Workflow

The application follows a clear, linear workflow from input to output. Each step is encapsulated in a dedicated module, allowing individual parts of the pipeline to be swapped or improved independently.

## 1. Media Validation and Audio Extraction

1. The user selects an audio or video file via the Streamlit front‑end.
2. The file is saved to a temporary location.
3. The **Audio Extraction** module examines the file extension and uses `moviepy` to extract the audio track from a video or `pydub` to convert audio files to WAV. Unsupported formats raise a `ValueError`.

## 2. Speech Recognition

1. The extracted WAV file is passed to **Whisper** for transcription. Whisper automatically detects the language of the audio and returns the transcript along with a predicted language code.
2. The raw transcript may contain line breaks and inconsistent spacing.

## 3. Cleaning and Language Detection

1. The **Cleaning** module normalises whitespace and removes stray characters to produce a clean transcript.
2. The cleaned text is fed into **langdetect** for a second opinion on the language. If the detection fails, the language reported by Whisper is used as a fallback.

## 4. Chunking and Summarisation

1. If the transcript exceeds the configured `CHUNK_SIZE` (500 words by default) it is split into chunks using the **Chunking** module. Short transcripts bypass this step.
2. Each chunk is summarised individually by the **Summarisation** module. English chunks are summarised by the BART CNN/DailyMail model. Hindi chunks are summarised by IndicBART; if the model cannot be loaded, the chunk is translated to English, summarised, then translated back to Hindi.
3. The chunk summaries are concatenated and summarised again to produce a **final summary**. This hierarchical approach ensures that the model’s context window is respected while maintaining coherence.

## 5. Keyword Extraction and Graph Generation

1. The cleaned transcript is passed to the **Keyword Extraction** module which uses YAKE to compute the top N keywords (default 10).
2. The **Diagram** module constructs a co‑occurrence graph where nodes represent keywords and edges indicate that two keywords appear in the same sentence. Edge weights reflect how often the co‑occurrence occurs.
3. The graph is rendered using NetworkX’s spring layout and saved as a PNG. When there are no edges (e.g. only one keyword), the diagram shows isolated nodes.

## 6. Saving and Displaying Results

* The Streamlit front‑end displays the raw transcript, final summary, chunk summaries, keywords and the graph. Each result section is clearly labelled.
* All generated artefacts are saved to the `outputs/` directory with meaningful names based on the original filename.
* Download buttons allow users to retrieve the transcript, cleaned transcript, chunk summaries, final summary, keyword list and graph image directly from the browser.

## 7. Running in Colab

For users who prefer a notebook environment, the project includes a Colab‑compatible notebook (`notebooks/colab_pipeline.ipynb`). The notebook guides you through installing dependencies, mounting Google Drive, running the pipeline on a sample file and saving outputs back to Drive.
