# -*- coding: utf-8 -*-
"""
week1/nlp_pipeline.py - Smart Farm NLP Pipeline (Week 1)
==========================================================
Demonstrates:
  - Tokenization (word & sentence) using NLTK
  - Stop words removal
  - Stemming using PorterStemmer
  - Lemmatization using WordNetLemmatizer

This module is also imported by later modules to provide the base pipeline.

Course: BIT4133 Natural Language Processing - Week 1
Project: Smart Farm AI Assistant
"""

import sys
import os
import string

# Allow imports from the parent directory (knowledge_base.py)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.stem import WordNetLemmatizer

# -- Download required NLTK data (silent if already present) -----------------
for pkg in ["punkt", "stopwords", "wordnet", "averaged_perceptron_tagger",
            "omw-1.4", "punkt_tab"]:
    nltk.download(pkg, quiet=True)

# -- Initialize NLP tools ----------------------------------------------------
porter_stemmer   = PorterStemmer()
snowball_stemmer = SnowballStemmer("english")
lemmatizer       = WordNetLemmatizer()
STOP_WORDS       = set(stopwords.words("english"))


# =============================================================================
# CORE PIPELINE FUNCTIONS
# =============================================================================

def sentence_tokenize(text: str) -> list:
    """Split a paragraph into individual sentences."""
    return sent_tokenize(text)


def word_tokenize_text(text: str) -> list:
    """Tokenize text into individual words (includes punctuation)."""
    return word_tokenize(text)


def remove_stopwords(tokens: list) -> list:
    """
    Remove English stop words AND punctuation from a token list.
    Returns only meaningful content tokens.
    """
    filtered = [
        token for token in tokens
        if token.lower() not in STOP_WORDS
        and token not in string.punctuation
        and token.strip()
    ]
    return filtered


def stem_tokens(tokens: list, stemmer: str = "porter") -> list:
    """
    Apply stemming to reduce words to their root form.

    Args:
        tokens: List of word tokens
        stemmer: 'porter' (default) or 'snowball'

    Returns:
        List of stemmed tokens
    """
    if stemmer == "snowball":
        return [snowball_stemmer.stem(t) for t in tokens]
    return [porter_stemmer.stem(t) for t in tokens]


def lemmatize_tokens(tokens: list) -> list:
    """
    Apply lemmatization using WordNet to get dictionary base forms.
    Tries verb form first, then falls back to noun form.
    """
    lemmas = []
    for token in tokens:
        # Try as verb first (catches 'turning' -> 'turn', 'dying' -> 'die')
        lemma_v = lemmatizer.lemmatize(token.lower(), pos="v")
        if lemma_v != token.lower():
            lemmas.append(lemma_v)
        else:
            # Fall back to noun form
            lemmas.append(lemmatizer.lemmatize(token.lower(), pos="n"))
    return lemmas


def run_full_pipeline(text: str, verbose: bool = True) -> dict:
    """
    Run the complete Week 1 NLP pipeline on a given text string.

    Steps:
      1. Sentence tokenization
      2. Word tokenization
      3. Stop word removal
      4. Stemming (Porter)
      5. Lemmatization

    Args:
        text: Input farming sentence or paragraph
        verbose: If True, print formatted output

    Returns:
        dict with keys: sentences, tokens, filtered, stems, lemmas
    """
    sentences = sentence_tokenize(text)
    tokens    = word_tokenize_text(text)
    filtered  = remove_stopwords(tokens)
    stems     = stem_tokens(filtered)
    lemmas    = lemmatize_tokens(filtered)

    result = {
        "original":  text,
        "sentences": sentences,
        "tokens":    tokens,
        "filtered":  filtered,
        "stems":     stems,
        "lemmas":    lemmas,
    }

    if verbose:
        _print_pipeline_result(result)

    return result


def _print_pipeline_result(result: dict):
    """Pretty-print the NLP pipeline output."""
    sep = "-" * 65
    print(sep)
    print(f"  INPUT    : {result['original']}")
    print(sep)
    print(f"  Sentences: {result['sentences']}")
    print(f"  Tokens   : {result['tokens']}")
    print(f"  Filtered : {result['filtered']}")
    print(f"  Stems    : {result['stems']}")
    print(f"  Lemmas   : {result['lemmas']}")
    print()


# =============================================================================
# MAIN - Run the pipeline on 5 farming example sentences
# =============================================================================

if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print()
    print("=" * 65)
    print("   SMART FARM - Week 1: NLP Pipeline Demonstration")
    print("   Course: BIT4133 Natural Language Processing")
    print("=" * 65)
    print()

    # Import demo sentences from the companion module
    from demo_sentences import FARMING_SENTENCES

    print(f"Processing {len(FARMING_SENTENCES)} farming sentences through the NLP pipeline...\n")

    for i, sentence in enumerate(FARMING_SENTENCES, start=1):
        print(f"[Sentence {i}]")
        run_full_pipeline(sentence, verbose=True)

    # -- Stemming Comparison ----------------------------------------------
    print("=" * 65)
    print("  STEMMING COMPARISON: Porter vs Snowball Stemmer")
    print("=" * 65)

    sample_words = ["diseased", "yellowing", "fertilizing", "spraying",
                    "irrigated", "harvesting", "leaves", "infection"]
    print(f"\n  {'Word':<15} {'Porter':<15} {'Snowball':<15}")
    print(f"  {'-'*13}   {'-'*13}   {'-'*13}")
    for word in sample_words:
        porter   = porter_stemmer.stem(word)
        snowball = snowball_stemmer.stem(word)
        print(f"  {word:<15} {porter:<15} {snowball:<15}")

    # -- Lemmatization vs Stemming -----------------------------------------
    print()
    print("=" * 65)
    print("  LEMMATIZATION vs STEMMING")
    print("=" * 65)
    compare_words = ["leaves", "running", "better", "corns", "spraying", "dying"]
    print(f"\n  {'Word':<15} {'Stem':<15} {'Lemma (n)':<15} {'Lemma (v)':<15}")
    print(f"  {'-'*13}   {'-'*13}   {'-'*13}   {'-'*13}")
    for word in compare_words:
        stem    = porter_stemmer.stem(word)
        lemma_n = lemmatizer.lemmatize(word, pos="n")
        lemma_v = lemmatizer.lemmatize(word, pos="v")
        print(f"  {word:<15} {stem:<15} {lemma_n:<15} {lemma_v:<15}")

    print()
    print("✅ Week 1 pipeline demonstration complete.")
    print()
