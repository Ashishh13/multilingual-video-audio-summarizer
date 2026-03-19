# Viva Questions and Answers

This section lists potential viva questions along with concise answers to help you prepare for your project presentation.

### 1. What motivated you to choose this project?

Recorded lectures, interviews and meetings are often lengthy and difficult to digest quickly. Existing summarisation tools primarily support English and rely on proprietary services. I wanted to build an open‑source pipeline that supports both English and Hindi, summarises long transcripts intelligently and provides visual insights through diagrams.

### 2. Which speech recognition model did you use and why?

I used **OpenAI’s Whisper** model because it provides state‑of‑the‑art transcription across many languages, including English and Hindi. Whisper can automatically detect the language of the audio and returns high quality transcripts without requiring internet access.

### 3. How does hierarchical summarisation work?

Transformer‑based summarisation models have limited context windows. To summarise long transcripts, I first split the transcript into smaller chunks (500 words each). Each chunk is summarised individually. The resulting chunk summaries are concatenated and summarised again to produce the final summary. This two‑stage process is known as hierarchical summarisation.

### 4. Why did you choose BART for English summarisation?

BART, particularly the CNN/DailyMail fine‑tuned model, has been shown to produce high quality abstractive summaries. It is widely adopted and available in the Hugging Face ecosystem. Its performance is reliable for student projects without requiring training.

### 5. How do you handle Hindi summarisation?

For Hindi, I used the **IndicBARTSS** checkpoint, a model fine‑tuned on 11 Indic languages and designed for sentence summarisation【687373803873561†L62-L69】. If this model cannot be loaded due to resource constraints, the system falls back to translating the Hindi text to English using MarianMT, summarising it with BART, and translating the result back to Hindi.

### 6. What algorithm did you use for keyword extraction?

I used the **YAKE (Yet Another Keyword Extractor)** algorithm. YAKE is unsupervised, language independent and does not require training data. It extracts keywords based on statistical co‑occurrence and works well for both English and Hindi.

### 7. How is the keyword graph constructed?

First, the text is split into sentences. For each sentence I check which extracted keywords appear together. If two keywords co‑occur in the same sentence, an edge is drawn between them in a graph. Edge weights reflect the frequency of co‑occurrence across the document. The graph is then rendered with NetworkX using a force‑directed layout.

### 8. What are the main limitations of your system?

The summarisation models are computationally heavy; running them on CPUs can be slow. Hindi summarisation quality depends on the availability of IndicBART; otherwise translation adds noise. Sentence segmentation is simplistic and may not perfectly handle complex punctuation. The keyword graph only captures co‑occurrence, not deeper semantic relationships.

### 9. How would you deploy this application?

Locally, the user can run `streamlit run app/app.py` after installing the requirements. For cloud deployment, Streamlit Community Cloud or Hugging Face Spaces can be used. These platforms allow you to share the app publicly without managing servers. A Colab notebook is also provided for notebook‑based execution.

### 10. How could this project be extended in the future?

Future work could include adding more languages, integrating topic modelling for deeper insights, using interactive graph visualisations (e.g. Plotly), optimising for real‑time summarisation, and fine‑tuning models specifically on domain‑specific corpora for improved accuracy.
