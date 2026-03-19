"""
Summarisation module.

This module implements hierarchical summarisation for long transcripts in
both English and Hindi. English summaries are generated using the
BART‑based CNN/DailyMail model, while Hindi summaries leverage the
IndicBART checkpoint, which supports summarising content in multiple
Indic languages and is more efficient than mBART or mT5【687373803873561†L62-L69】.

When Hindi summarisation fails or a model cannot be loaded (for
example, in low‑resource environments), the code falls back to a
translate–summarise–translate pipeline using MarianMT models.
"""

from typing import List, Tuple, Optional

import torch
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    MarianMTModel,
    MarianTokenizer,
)

from .config import (
    ENGLISH_SUMMARY_MODEL,
    HINDI_SUMMARY_MODEL,
    CHUNK_SIZE,
)
from .chunking import chunk_text


# Global caches to avoid reloading models repeatedly
_en_summarizer: Optional[callable] = None
_hi_tokenizer: Optional[AutoTokenizer] = None
_hi_model: Optional[AutoModelForSeq2SeqLM] = None
_marian_hi_en_tokenizer: Optional[MarianTokenizer] = None
_marian_hi_en_model: Optional[MarianMTModel] = None
_marian_en_hi_tokenizer: Optional[MarianTokenizer] = None
_marian_en_hi_model: Optional[MarianMTModel] = None


def _load_en_summarizer():
    """Lazy‑load the English summarisation pipeline."""
    global _en_summarizer
    if _en_summarizer is None:
        device = 0 if torch.cuda.is_available() else -1
        _en_summarizer = pipeline(
            "summarization",
            model=ENGLISH_SUMMARY_MODEL,
            tokenizer=ENGLISH_SUMMARY_MODEL,
            device=device,
        )
    return _en_summarizer


def _load_hi_models():
    """Lazy‑load the Indic summarisation model and tokenizer."""
    global _hi_tokenizer, _hi_model
    if _hi_tokenizer is None or _hi_model is None:
        _hi_tokenizer = AutoTokenizer.from_pretrained(HINDI_SUMMARY_MODEL, use_fast=False)
        _hi_model = AutoModelForSeq2SeqLM.from_pretrained(HINDI_SUMMARY_MODEL)
    return _hi_tokenizer, _hi_model


def _load_translation_models():
    """Lazy‑load MarianMT translation models for hi↔en."""
    global (
        _marian_hi_en_tokenizer,
        _marian_hi_en_model,
        _marian_en_hi_tokenizer,
        _marian_en_hi_model,
    )
    if _marian_hi_en_tokenizer is None:
        _marian_hi_en_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-hi-en")
        _marian_hi_en_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-hi-en")
    if _marian_en_hi_tokenizer is None:
        _marian_en_hi_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-hi")
        _marian_en_hi_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-hi")


def translate(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text between Hindi and English using MarianMT models.

    Parameters
    ----------
    text : str
        Input text to translate.
    source_lang : str
        Source language code ('hi' or 'en').
    target_lang : str
        Target language code ('hi' or 'en').

    Returns
    -------
    str
        The translated text.
    """
    _load_translation_models()
    if source_lang == target_lang:
        return text
    if source_lang == "hi" and target_lang == "en":
        tokenizer = _marian_hi_en_tokenizer
        model = _marian_hi_en_model
    elif source_lang == "en" and target_lang == "hi":
        tokenizer = _marian_en_hi_tokenizer
        model = _marian_en_hi_model
    else:
        raise ValueError(f"Unsupported translation direction: {source_lang}->{target_lang}")
    inputs = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
    translated_ids = model.generate(**inputs)
    translated = tokenizer.batch_decode(translated_ids, skip_special_tokens=True)[0]
    return translated


def _summarize_hindi(text: str) -> str:
    """Summarise a Hindi document using IndicBART.

    This function explicitly formats the input and output languages as
    described in the model card【687373803873561†L92-L100】. It falls back to
    translation‑based summarisation on failure.
    """
    try:
        tokenizer, model = _load_hi_models()
        # Prepare input: original text + language code token
        prepared = text.strip() + " </s> <2hi>"
        inputs = tokenizer(
            prepared,
            add_special_tokens=False,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        )
        input_ids = inputs["input_ids"]
        bos_id = tokenizer._convert_token_to_id_with_added_voc("<s>")
        eos_id = tokenizer._convert_token_to_id_with_added_voc("</s>")
        pad_id = tokenizer._convert_token_to_id_with_added_voc("<pad>")
        hi_id = tokenizer._convert_token_to_id_with_added_voc("<2hi>")
        output_ids = model.generate(
            input_ids=input_ids,
            use_cache=True,
            no_repeat_ngram_size=3,
            num_beams=4,
            length_penalty=0.8,
            max_length=128,
            min_length=20,
            early_stopping=True,
            pad_token_id=pad_id,
            bos_token_id=bos_id,
            eos_token_id=eos_id,
            decoder_start_token_id=hi_id,
        )[0]
        summary = tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        return summary
    except Exception:
        # Fall back to translation pipeline: hi→en→summary→en→hi
        en_text = translate(text, "hi", "en")
        en_summary = _summarize_english(en_text)
        hi_summary = translate(en_summary, "en", "hi")
        return hi_summary


def _summarize_english(text: str) -> str:
    """Summarise an English document using BART."""
    summarizer = _load_en_summarizer()
    # The pipeline returns a list of dicts with key 'summary_text'
    result = summarizer(
        text,
        max_length=130,
        min_length=30,
        do_sample=False,
    )
    return result[0]["summary_text"].strip()


def summarize_chunk(text: str, language: Optional[str]) -> str:
    """Summarise a single chunk of text based on language.

    If ``language`` is 'hi' the Hindi model is attempted first, then
    fallback through the translation pipeline. For all other cases
    (including 'en' and unknown codes) the English summariser is used.
    """
    if not text.strip():
        return ""
    if language == "hi":
        return _summarize_hindi(text)
    # Default to English summarisation for any other language code
    return _summarize_english(text)


def hierarchical_summarize(text: str, language: Optional[str]) -> Tuple[str, List[str]]:
    """Perform hierarchical summarisation on a long transcript.

    The transcript is split into chunks using ``CHUNK_SIZE``. Each chunk
    is summarised individually, then the concatenated summaries are
    summarised again to produce the final summary.

    Parameters
    ----------
    text : str
        The cleaned transcript.
    language : str or None
        Two‑letter code for the language ('en' or 'hi'). If None the
        function assumes English.

    Returns
    -------
    final_summary : str
        Summary of the entire document.
    chunk_summaries : List[str]
        Summaries of each intermediate chunk.
    """
    # If the text is short, avoid chunking overhead
    words = text.split()
    if len(words) <= CHUNK_SIZE:
        summary = summarize_chunk(text, language)
        return summary, [summary]
    # Otherwise perform hierarchical summarisation
    chunks = chunk_text(text, CHUNK_SIZE)
    partials: List[str] = []
    for chunk in chunks:
        part_summary = summarize_chunk(chunk, language)
        partials.append(part_summary)
    combined = " ".join(partials)
    final_summary = summarize_chunk(combined, language)
    return final_summary, partials
