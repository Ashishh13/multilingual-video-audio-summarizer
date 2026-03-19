"""
Streamlit application for the Multilingual Smart Summarization project.

This front‑end ties together the various modules to provide an end‑to‑end
experience: users upload an audio or video file, the system extracts
audio, transcribes speech, cleans the transcript, detects the language,
performs hierarchical summarisation, extracts keywords, generates a
knowledge graph and finally offers downloadable results. The app is
designed to run locally or on Streamlit Cloud without modification.
"""
import os
import sys
import tempfile
import streamlit as st

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules import (
    extract_audio,
    transcribe_audio,
    clean_text,
    detect_language,
    hierarchical_summarize,
    extract_keywords,
    build_keyword_graph,
    save_transcript,
    save_clean_transcript,
    save_chunk_summaries,
    save_final_summary,
    save_keywords,
)
from modules.config import OUTPUT_DIR



def main():
    """Run the Streamlit app."""
    st.set_page_config(page_title="Multilingual Smart Summarization", layout="wide")
    st.title("Multilingual Smart Summarization from Video and Audio")
    st.write(
        "Upload an audio or video file (English or Hindi) and the application "
        "will transcribe it, clean the transcript, detect the language, "
        "generate hierarchical summaries, extract keywords and produce a "
        "keyword co‑occurrence graph."
    )

    # Upload widget
    uploaded_file = st.file_uploader(
        "Upload your media file (mp3, wav, mp4, m4a, flac, avi, mkv)",
        type=["mp3", "wav", "mp4", "m4a", "flac", "avi", "mkv"],
    )

    if uploaded_file is not None:
        # Persist the uploaded file to a temporary location on disk
        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            input_path = tmp.name
        st.success(f"Uploaded file saved: {uploaded_file.name}")

        if st.button("Process file"):
            with st.spinner("Extracting audio from media..."):
                audio_path = extract_audio(input_path)

            with st.spinner("Running speech recognition..."):
                transcript, whisper_lang = transcribe_audio(audio_path)

            st.subheader("Raw Transcript")
            st.text_area("Transcript", transcript, height=200)

            with st.spinner("Cleaning transcript and detecting language..."):
                cleaned = clean_text(transcript)
                detected_lang = detect_language(cleaned) or whisper_lang or "en"

            st.markdown(f"**Detected language:** {detected_lang}")

            with st.spinner("Generating summaries..."):
                final_summary, chunk_summaries = hierarchical_summarize(cleaned, detected_lang)

            st.subheader("Final Summary")
            st.text_area("Summary", final_summary, height=150)

            # Expanders for chunk summaries to avoid cluttering the page
            st.subheader("Chunk Summaries")
            for idx, summary in enumerate(chunk_summaries, 1):
                with st.expander(f"Chunk {idx} Summary"):
                    st.write(summary)

            with st.spinner("Extracting keywords..."):
                keywords = extract_keywords(cleaned, detected_lang)

            st.subheader("Keywords")
            st.write(", ".join(keywords))

            with st.spinner("Generating keyword graph..."):
                graph_path = build_keyword_graph(keywords, cleaned, os.path.join(OUTPUT_DIR, "keyword_graph.png"))

            st.subheader("Keyword Co‑occurrence Graph")
            st.image(graph_path, use_column_width=True)

            # Prepare file names
            base_name = os.path.splitext(uploaded_file.name)[0]
            transcript_file = os.path.join(OUTPUT_DIR, f"{base_name}_transcript.txt")
            clean_file = os.path.join(OUTPUT_DIR, f"{base_name}_cleaned.txt")
            chunk_file = os.path.join(OUTPUT_DIR, f"{base_name}_chunks.txt")
            summary_file = os.path.join(OUTPUT_DIR, f"{base_name}_summary.txt")
            keywords_file = os.path.join(OUTPUT_DIR, f"{base_name}_keywords.txt")

            # Persist outputs
            save_transcript(transcript, transcript_file)
            save_clean_transcript(cleaned, clean_file)
            save_chunk_summaries(chunk_summaries, chunk_file)
            save_final_summary(final_summary, summary_file)
            save_keywords(keywords, keywords_file)

            st.success("Processing complete. Files have been saved to the outputs directory.")

            # Download buttons
            with open(transcript_file, "r", encoding="utf-8") as f:
                st.download_button(
                    "Download Transcript",
                    f.read(),
                    file_name=os.path.basename(transcript_file),
                )
            with open(summary_file, "r", encoding="utf-8") as f:
                st.download_button(
                    "Download Final Summary",
                    f.read(),
                    file_name=os.path.basename(summary_file),
                )
            with open(chunk_file, "r", encoding="utf-8") as f:
                st.download_button(
                    "Download Chunk Summaries",
                    f.read(),
                    file_name=os.path.basename(chunk_file),
                )
            with open(keywords_file, "r", encoding="utf-8") as f:
                st.download_button(
                    "Download Keywords",
                    f.read(),
                    file_name=os.path.basename(keywords_file),
                )
            with open(graph_path, "rb") as f:
                st.download_button(
                    "Download Keyword Graph",
                    f.read(),
                    file_name=os.path.basename(graph_path),
                )


if __name__ == "__main__":
    main()
