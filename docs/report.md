# Project Report

## Title

**Multilingual Smart Summarization from Video and Audio with Diagrammatic Representation (English and Hindi)**

## Aim

To design and implement a software system that automatically extracts speech from audio or video media, transcribes and processes the text, summarises long passages hierarchically and visualises key concepts, with support for both English and Hindi languages.

## Objectives

1. Develop an end‑to‑end pipeline that accepts video/audio files and produces concise summaries, keywords and visual diagrams.
2. Integrate state‑of‑the‑art speech recognition (Whisper) and abstractive summarisation models (BART for English and IndicBART for Hindi【687373803873561†L62-L69】).
3. Implement hierarchical summarisation to handle long transcripts without exceeding transformer context windows.
4. Support Hindi summarisation either natively via IndicBART or via translation‑based fallback.
5. Extract salient keywords and visualise their relationships using graph techniques.
6. Provide a user‑friendly interface via Streamlit and a notebook alternative for Google Colab.
7. Document the system thoroughly and provide deployment and troubleshooting guidance.

## Abstract

As audio and video content proliferate across educational and professional domains, the need for tools that can distil this content into concise, actionable knowledge becomes acute. Existing solutions primarily target English and often rely on paid APIs. This project presents a fully open‑source, end‑to‑end application capable of ingesting audio or video files in English or Hindi, extracting the spoken content, performing cleaning and language detection, generating hierarchical summaries, extracting keywords and visualising their co‑occurrence as a knowledge graph. The system leverages OpenAI’s Whisper for robust speech recognition and uses two separate abstractive summarisation models: BART for English and IndicBART for Hindi. When the IndicBART model cannot be loaded, a translate–summarise–translate fallback using MarianMT models is employed. The final deliverable includes a Streamlit web application, a Colab notebook, comprehensive documentation and testing infrastructure.

## Problem Statement

Manual note‑taking and summarisation of audio/video content is laborious and error‑prone, particularly for non‑English media. While automatic speech recognition has made significant progress, converting transcripts into coherent summaries remains challenging due to the length of transcripts and the complexity of multilingual processing. Moreover, summarised content often lacks context and visualisation of key concepts. There is a need for a unified solution that addresses transcription, summarisation, keyword extraction and diagrammatic representation in a user‑friendly manner.

## Methodology

1. **Requirement Analysis:** Detailed user requirements were gathered to support English and Hindi, handle various media formats and provide a graphical representation of key concepts. Open‑source tools and models were selected to avoid licensing issues.

2. **System Design:** A modular architecture was devised to separate audio extraction, transcription, cleaning, language detection, chunking, summarisation, keyword extraction, graph generation and user interface concerns. The design allows individual modules to be replaced or improved independently.

3. **Model Selection:** Whisper was chosen for speech recognition due to its high accuracy across languages. For summarisation, BART (CNN/DailyMail) was selected for English, and IndicBARTSS was selected for Hindi because it supports multiple Indic languages and is lighter than mBART or mT5【687373803873561†L62-L69】. MarianMT translation models were added to provide a fallback summarisation pathway.

4. **Implementation:** Each module was implemented in Python with clear interfaces. Hierarchical summarisation was designed to divide long transcripts into manageable chunks, summarise each chunk and then summarise the combined summaries. YAKE was integrated for keyword extraction and NetworkX for graph generation. A Streamlit app orchestrates the pipeline and presents the results. A Colab notebook replicates the pipeline in a notebook environment.

5. **Testing:** Basic unit tests were written for helper functions. Manual testing with short English and Hindi clips confirmed that the pipeline works end‑to‑end.

6. **Documentation:** Comprehensive documentation and a troubleshooting guide were written to support installation, running, deployment and debugging.

## Results

The final application successfully performs the following:

* Accepts a variety of audio and video formats and extracts audio via `moviepy`/`pydub`.
* Transcribes speech accurately using Whisper and confirms the language via `langdetect`.
* Generates readable summaries even for long transcripts using hierarchical summarisation. IndicBART provides Hindi summaries, while the fallback ensures that Hindi texts can still be summarised via translation.
* Extracts meaningful keywords using YAKE and visualises their relationships through a graph. For example, when processing a Hindi news clip about a government event, keywords such as “सरकार” (government), “আघोषणा” (announcement) and “कार्यक्रम” (programme) were extracted and connected in the diagram.
* Provides a user interface where users can upload files, view progress, read transcripts and summaries, view graphs and download all artefacts.

## Limitations

1. **Computational Demand:** Transformer models are resource intensive. On CPU‑only systems, summarisation can take several minutes for long files.
2. **Model Availability:** IndicBART is not always available on all systems due to memory constraints. The translate–summarise–translate fallback may produce less natural Hindi summaries.
3. **Sentence Segmentation:** A simple regular expression is used to split sentences. This may misidentify sentence boundaries in complex Hindi text.
4. **Keyword Graph:** The co‑occurrence graph is based on sentence‑level co‑occurrence only. It does not capture deeper semantic relationships between topics.
5. **Topic Extraction:** The system extracts keywords but does not perform full topic modelling. Adding topic modelling (e.g. using LDA) could provide richer insights.

## Conclusion

This project demonstrates a complete, deployable pipeline for multimedia summarisation and visualisation in English and Hindi. By combining Whisper for transcription, state‑of‑the‑art summarisation models and lightweight keyword extraction, the system provides a practical tool for quickly understanding recorded content. The modular design and extensive documentation make it a strong candidate for a final‑year project submission and a foundation for future research.

## Future Scope

* **Improved Hindi Summarisation:** Fine‑tune models specifically on Hindi corpora to improve fluency and coherence.
* **Topic Modelling:** Integrate topic modelling algorithms such as LDA or BERTopic to extract thematic structure.
* **Interactive Graphs:** Use interactive libraries like Plotly or VisPy to allow users to explore keyword graphs dynamically.
* **Real‑Time Processing:** Optimise the pipeline for streaming input so that live lectures can be summarised on the fly.
* **Additional Languages:** Extend support to other Indic languages (e.g. Marathi, Tamil) by leveraging the multilingual capabilities of IndicBART and translation models.

## References

* OpenAI Whisper model and paper
* Hugging Face IndicBARTSS model card【687373803873561†L62-L69】
* mT5 m2o Hindi CrossSum model card【879896779544012†L50-L53】
