# Sample Data Instructions

To protect repository size and bandwidth, no media files are bundled in
this project. To test the application you should supply your own small
audio or video clips. Keep in mind the following when preparing
sample data:

* **Format:** Supported file types include MP3, WAV, MP4, M4A, FLAC, AVI and MKV. If your file is not in one of these formats you can convert it using FFmpeg.
* **Length:** For quick demonstrations, choose clips under one minute. Longer recordings will still work but will take more time to process and summarise.
* **Language:** Recordings should be in English or Hindi to fully exercise the multilingual pipeline. The language detector will decide which summarisation model to use.
* **Clarity:** For best results use clear speech without excessive background noise. Whisper will attempt to transcribe noisy audio but accuracy may suffer.

If you do not have a suitable file, you can generate a quick test using
text‑to‑speech or record yourself reading a short paragraph. Place
these files anywhere on your machine when running the app locally,
then upload them through the Streamlit interface.
