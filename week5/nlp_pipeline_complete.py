"""
week5/nlp_pipeline_complete.py
===========================================================
BIT4133 – Natural Language Processing with Deep Learning
Week 5: CAT 1 Preparation — Complete NLP Pipeline

Integrates ALL concepts from Weeks 1–4:
  - Week 1: Tokenization, Stop Words, Stemming, Lemmatization
  - Week 2: N-gram modeling, POS Tagging
  - Week 3: HMM Sequence Labeling concepts
  - Week 4: Dependency parsing, Semantic similarity

Practical Task 1: Complete NLP processing pipeline using NLTK

Run:  python week5/nlp_pipeline_complete.py

Requirements:
    pip install nltk spacy
    python -m spacy download en_core_web_sm
"""

import sys
import math
from collections import Counter

# ── NLTK imports ──────────────────────────────────────────────────────────────
try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    from nltk import pos_tag
except ImportError:
    print("ERROR: NLTK not installed. Run: pip install nltk")
    sys.exit(1)

# ── Download required NLTK data ───────────────────────────────────────────────
for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet", "averaged_perceptron_tagger",
            "averaged_perceptron_tagger_eng"]:
    try:
        nltk.data.find(f"tokenizers/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

# ── spaCy import (optional — graceful fallback) ───────────────────────────────
try:
    import spacy
    _nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except Exception:
    SPACY_AVAILABLE = False

# ── Tools ─────────────────────────────────────────────────────────────────────
stemmer    = PorterStemmer()
lemmatizer = WordNetLemmatizer()
STOP_WORDS = set(stopwords.words("english"))

DIVIDER   = "=" * 70
SEPARATOR = "-" * 70

# Penn Treebank POS tag explanations (subset)
POS_EXPLAIN = {
    "NN":  "Noun (singular)",       "NNS": "Noun (plural)",
    "NNP": "Proper noun",           "VB":  "Verb (base form)",
    "VBZ": "Verb (3rd person)",     "VBG": "Verb (gerund)",
    "VBD": "Verb (past tense)",     "VBN": "Verb (past participle)",
    "JJ":  "Adjective",             "JJR": "Adjective (comparative)",
    "RB":  "Adverb",                "DT":  "Determiner",
    "IN":  "Preposition",           "CC":  "Conjunction",
    "PRP": "Personal pronoun",      "PRP$":"Possessive pronoun",
    "CD":  "Cardinal number",       ".",   "Period",
    ",":   "Comma",
}


# =============================================================================
# HELPER
# =============================================================================

def _pos_explain(tag: str) -> str:
    return POS_EXPLAIN.get(tag, tag)


def print_step(step_num: int, title: str):
    print(f"\n  ── Step {step_num}: {title} ──")


# =============================================================================
# COMPLETE NLP PIPELINE
# =============================================================================

def run_complete_pipeline(text: str, verbose: bool = True) -> dict:
    """
    Run the complete BIT4133 NLP pipeline on a given text.

    Steps:
        1. Sentence Tokenization
        2. Word Tokenization
        3. Stop Word Removal
        4. Stemming (Porter)
        5. Lemmatization (WordNet)
        6. POS Tagging
        7. N-gram Generation (bigrams)
        8. Semantic Similarity (if spaCy available)

    Returns a dictionary with all intermediate results.
    """
    results = {}

    if verbose:
        print(f"\n{DIVIDER}")
        print(f"  COMPLETE NLP PIPELINE")
        print(f"  Input: \"{text}\"")
        print(DIVIDER)

    # ── Step 1: Sentence tokenization ────────────────────────────────────────
    sentences = sent_tokenize(text)
    results["sentences"] = sentences
    if verbose:
        print_step(1, "Sentence Tokenization")
        for i, s in enumerate(sentences, 1):
            print(f"       Sentence {i}: {s}")

    # ── Step 2: Word tokenization ─────────────────────────────────────────────
    tokens = word_tokenize(text)
    results["tokens"] = tokens
    if verbose:
        print_step(2, "Word Tokenization")
        print(f"       Tokens  : {tokens}")
        print(f"       Count   : {len(tokens)} tokens")

    # ── Step 3: Stop word removal ─────────────────────────────────────────────
    filtered = [w for w in tokens if w.lower() not in STOP_WORDS and w.isalpha()]
    results["filtered"] = filtered
    if verbose:
        print_step(3, "Stop Word Removal")
        removed = [w for w in tokens if w.lower() in STOP_WORDS]
        print(f"       Stop words removed : {removed}")
        print(f"       Filtered tokens    : {filtered}")

    # ── Step 4: Stemming ──────────────────────────────────────────────────────
    stems = [stemmer.stem(w) for w in filtered]
    results["stems"] = stems
    if verbose:
        print_step(4, "Stemming (Porter Stemmer)")
        print(f"       {'Original':<20} {'Stem'}")
        print(f"       {'-'*19} {'-'*19}")
        for orig, stem in zip(filtered, stems):
            print(f"       {orig:<20} {stem}")

    # ── Step 5: Lemmatization ─────────────────────────────────────────────────
    lemmas_n = [lemmatizer.lemmatize(w.lower(), pos="n") for w in filtered]
    lemmas_v = [lemmatizer.lemmatize(w.lower(), pos="v") for w in filtered]
    results["lemmas"] = lemmas_v
    if verbose:
        print_step(5, "Lemmatization (WordNet Lemmatizer)")
        print(f"       {'Original':<20} {'Noun Lemma':<20} {'Verb Lemma'}")
        print(f"       {'-'*19} {'-'*19} {'-'*19}")
        for orig, ln, lv in zip(filtered, lemmas_n, lemmas_v):
            print(f"       {orig:<20} {ln:<20} {lv}")

    # ── Step 6: POS Tagging ───────────────────────────────────────────────────
    pos_tags = pos_tag(filtered)
    results["pos_tags"] = pos_tags
    if verbose:
        print_step(6, "POS Tagging (NLTK Averaged Perceptron)")
        print(f"       {'Word':<20} {'POS Tag':<10} {'Description'}")
        print(f"       {'-'*19} {'-'*9} {'-'*30}")
        for word, tag in pos_tags:
            print(f"       {word:<20} {tag:<10} {_pos_explain(tag)}")

        nouns = [w for w, t in pos_tags if t.startswith("NN")]
        verbs = [w for w, t in pos_tags if t.startswith("VB")]
        adjs  = [w for w, t in pos_tags if t.startswith("JJ")]
        print(f"\n       Nouns      : {nouns}")
        print(f"       Verbs      : {verbs}")
        print(f"       Adjectives : {adjs}")

    # ── Step 7: N-gram Generation ─────────────────────────────────────────────
    words_lower = [w.lower() for w in filtered]
    bigrams  = [(words_lower[i], words_lower[i+1]) for i in range(len(words_lower)-1)]
    trigrams = [(words_lower[i], words_lower[i+1], words_lower[i+2])
                for i in range(len(words_lower)-2)]
    results["bigrams"]  = bigrams
    results["trigrams"] = trigrams
    if verbose:
        print_step(7, "N-gram Generation")
        print(f"       Bigrams  : {bigrams}")
        print(f"       Trigrams : {trigrams if trigrams else 'Not enough tokens for trigrams'}")

    # ── Step 8: Semantic similarity (optional) ────────────────────────────────
    if SPACY_AVAILABLE and verbose:
        print_step(8, "Semantic Similarity (spaCy — Bonus from Week 4)")
        comparison_text = "Natural Language Processing enables computers to understand text."
        doc1 = _nlp(text)
        doc2 = _nlp(comparison_text)
        sim = doc1.similarity(doc2)
        print(f"       Input sentence  : \"{text}\"")
        print(f"       Compare against : \"{comparison_text}\"")
        print(f"       Similarity Score: {sim:.4f}")

    return results


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

def main():
    print(DIVIDER)
    print("  BIT4133 — Week 5: Complete NLP Pipeline")
    print("  CAT 1 Preparation — Integrated All Weeks")
    print(DIVIDER)

    # ── Course example sentence (from Week 5 notes) ───────────────────────────
    course_sentence = "Natural Language Processing helps computers understand language."
    print(f"\n  ► Running course example sentence:")
    run_complete_pipeline(course_sentence)

    # ── Additional sentences to practice ─────────────────────────────────────
    practice_sentences = [
        "The student submitted the assignment before the deadline.",
        "Machine learning models improve with more training data.",
        "The administrator updated the student records in the system.",
    ]

    for sentence in practice_sentences:
        print(f"\n{DIVIDER}")
        print(f"  ► Practice sentence:")
        run_complete_pipeline(sentence)

    # ── Summary table ─────────────────────────────────────────────────────────
    print(f"\n{DIVIDER}")
    print(f"  NLP PIPELINE REVISION SUMMARY")
    print(DIVIDER)
    print("""
  Step 1 — Text Collection     : Gather raw text input from user
  Step 2 — Text Preprocessing  : Clean, normalize, lowercase
  Step 3 — Tokenization        : Split into words/sentences
  Step 4 — Stopword Removal    : Remove low-information words
  Step 5 — POS Tagging         : Assign grammatical roles
  Step 6 — Parsing             : Identify word relationships
  Step 7 — Semantic Analysis   : Measure meaning and similarity
  Step 8 — Result Interpretation: Present solution to user
    """)

    # ── CAT 1 quick-reference ─────────────────────────────────────────────────
    print(f"\n{DIVIDER}")
    print(f"  CAT 1 REVISION CHECKLIST")
    print(DIVIDER)
    cat_topics = [
        ("Tokenization",       "word_tokenize(), sent_tokenize()"),
        ("Stop Word Removal",  "stopwords.words('english')"),
        ("Stemming",           "PorterStemmer().stem(word)"),
        ("Lemmatization",      "WordNetLemmatizer().lemmatize(word, pos='v')"),
        ("POS Tagging",        "nltk.pos_tag(tokens) — Penn Treebank tags"),
        ("N-grams",            "zip(tokens, tokens[1:]) for bigrams"),
        ("HMM Basics",         "States, Observations, Transitions, Emissions, Viterbi"),
        ("Dependency Parsing", "spacy: token.dep_, token.head"),
        ("Semantic Similarity","nlp(s1).similarity(nlp(s2)) — 0.0 to 1.0"),
        ("NLP Pipeline",       "Tokenize → Filter → Stem/Lemma → POS → Parse → Semantics"),
    ]
    for topic, note in cat_topics:
        print(f"  ✔ {topic:<25} {note}")

    print(f"\n{DIVIDER}")
    print("  Week 5 pipeline complete. Ready for CAT 1.")
    print("  Take screenshots of each pipeline step for your logbook.")
    print(DIVIDER)
    print()


if __name__ == "__main__":
    main()
