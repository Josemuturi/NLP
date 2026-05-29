"""
week2/ngram_model.py - Smart Farm N-gram Language Model (Week 2)
=================================================================
Demonstrates:
  - Building unigram, bigram, and trigram frequency models from a farming corpus
  - Calculating n-gram probabilities
  - Using n-grams to understand common word sequences in farming language
  - Text prediction using the bigram model

Course: BIT4133 Natural Language Processing - Week 2
Project: Smart Farm AI Assistant
"""

import sys
import os
from collections import defaultdict, Counter
import math

# Allow imports from parent/sibling directories
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "week1"))

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download("punkt",      quiet=True)
nltk.download("stopwords",  quiet=True)
nltk.download("punkt_tab",  quiet=True)

from demo_sentences import FARMING_CORPUS


# =============================================================================
# N-GRAM BUILDER
# =============================================================================

class FarmingNgramModel:
    """
    A simple n-gram language model built on a farming text corpus.

    Supports unigrams (n=1), bigrams (n=2), and trigrams (n=3).
    Uses Maximum Likelihood Estimation (MLE) for probabilities.
    Adds Laplace (add-1) smoothing for unseen n-grams.
    """

    START = "<START>"
    END   = "<END>"

    def __init__(self, corpus: list, n: int = 2, remove_stops: bool = False):
        """
        Args:
            corpus: List of sentence strings
            n: N-gram order (1, 2, or 3)
            remove_stops: If True, remove stop words before building model
        """
        self.n           = n
        self.stop_words  = set(stopwords.words("english")) if remove_stops else set()
        self.ngram_freq  = Counter()
        self.context_freq = Counter()
        self.vocabulary  = set()

        self._build(corpus)

    def _tokenize(self, sentence: str) -> list:
        """Tokenize a sentence and optionally remove stop words."""
        tokens = [t.lower() for t in word_tokenize(sentence)
                  if t.isalpha() and t.lower() not in self.stop_words]
        # Wrap with start/end markers
        padded = ([self.START] * (self.n - 1)) + tokens + [self.END]
        return padded

    def _build(self, corpus: list):
        """Build n-gram frequency counts from corpus."""
        for sentence in corpus:
            tokens = self._tokenize(sentence)
            self.vocabulary.update(tokens)
            for i in range(len(tokens) - self.n + 1):
                ngram   = tuple(tokens[i : i + self.n])
                context = ngram[:-1]
                self.ngram_freq[ngram]   += 1
                self.context_freq[context] += 1

    def probability(self, ngram: tuple) -> float:
        """
        Calculate MLE probability of an n-gram with Laplace smoothing.

        P(w_n | w_1...w_{n-1}) = (count(ngram) + 1) / (count(context) + |V|)
        """
        context = ngram[:-1]
        vocab_size = len(self.vocabulary)
        numerator   = self.ngram_freq[ngram] + 1            # add-1 smoothing
        denominator = self.context_freq[context] + vocab_size
        return numerator / denominator

    def log_probability(self, ngram: tuple) -> float:
        """Return log (base 2) probability of an n-gram."""
        return math.log2(self.probability(ngram))

    def sentence_probability(self, sentence: str) -> float:
        """Calculate total log probability of a sentence under this model."""
        tokens = self._tokenize(sentence)
        log_prob = 0.0
        for i in range(self.n - 1, len(tokens)):
            ngram     = tuple(tokens[i - (self.n - 1) : i + 1])
            log_prob += self.log_probability(ngram)
        return log_prob

    def perplexity(self, test_corpus: list) -> float:
        """
        Calculate perplexity on a test corpus.
        Lower perplexity = better model fit.
        """
        total_log_prob = 0.0
        total_tokens   = 0
        for sentence in test_corpus:
            tokens = self._tokenize(sentence)
            total_tokens += len(tokens)
            total_log_prob += self.sentence_probability(sentence)
        return math.pow(2, -total_log_prob / total_tokens)

    def top_ngrams(self, top_k: int = 10) -> list:
        """Return the top-k most frequent n-grams."""
        return self.ngram_freq.most_common(top_k)

    def predict_next(self, context_words: list, top_k: int = 3) -> list:
        """
        Given a context (list of n-1 words), predict the most likely next word.

        Args:
            context_words: List of preceding words (length = n-1)
            top_k: Number of candidate next words to return

        Returns:
            List of (word, probability) tuples
        """
        context = tuple(w.lower() for w in context_words[-(self.n - 1):])
        candidates = {}
        for ngram, count in self.ngram_freq.items():
            if ngram[:-1] == context:
                prob = self.probability(ngram)
                candidates[ngram[-1]] = prob

        sorted_candidates = sorted(candidates.items(), key=lambda x: -x[1])
        return sorted_candidates[:top_k]

    def get_stats(self) -> dict:
        """Return model statistics."""
        return {
            "n": self.n,
            "vocabulary_size": len(self.vocabulary),
            "unique_ngrams": len(self.ngram_freq),
            "total_ngrams": sum(self.ngram_freq.values()),
            "corpus_size": len(FARMING_CORPUS),
        }


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

def _separator(title: str = "", width: int = 65):
    if title:
        pad = (width - len(title) - 2) // 2
        print(f"\n{'=' * pad} {title} {'=' * pad}")
    else:
        print("-" * width)


if __name__ == "__main__":
    print()
    print("=" * 65)
    print("   SMART FARM - Week 2: N-gram Language Model")
    print("   Course: BIT4133 Natural Language Processing")
    print("=" * 65)

    # -- Build models -----------------------------------------------------
    print("\n📚 Building N-gram models from farming corpus...")
    print(f"   Corpus size: {len(FARMING_CORPUS)} sentences\n")

    unigram_model = FarmingNgramModel(FARMING_CORPUS, n=1)
    bigram_model  = FarmingNgramModel(FARMING_CORPUS, n=2)
    trigram_model = FarmingNgramModel(FARMING_CORPUS, n=3)

    # -- Model statistics -------------------------------------------------
    _separator("MODEL STATISTICS")
    for label, model in [("Unigram", unigram_model),
                          ("Bigram",  bigram_model),
                          ("Trigram", trigram_model)]:
        stats = model.get_stats()
        print(f"\n  {label} Model (n={stats['n']}):")
        print(f"    Vocabulary size : {stats['vocabulary_size']}")
        print(f"    Unique n-grams  : {stats['unique_ngrams']}")
        print(f"    Total n-grams   : {stats['total_ngrams']}")

    # -- Top n-grams -------------------------------------------------------
    _separator("TOP 10 UNIGRAMS (most frequent words)")
    print()
    for rank, (ngram, count) in enumerate(unigram_model.top_ngrams(10), 1):
        word = ngram[0] if isinstance(ngram, tuple) else ngram
        print(f"  {rank:2d}. {word:<20} count={count}")

    _separator("TOP 10 BIGRAMS (most frequent word pairs)")
    print()
    for rank, (ngram, count) in enumerate(bigram_model.top_ngrams(10), 1):
        print(f"  {rank:2d}. {' '.join(ngram):<30} count={count}")

    _separator("TOP 10 TRIGRAMS (most frequent 3-word sequences)")
    print()
    for rank, (ngram, count) in enumerate(trigram_model.top_ngrams(10), 1):
        print(f"  {rank:2d}. {' '.join(ngram):<40} count={count}")

    # -- Next word prediction ---------------------------------------------
    _separator("NEXT WORD PREDICTION (Bigram Model)")
    contexts = [
        ["maize"],
        ["spray"],
        ["the", "soil"],
        ["disease"],
        ["apply"],
    ]
    print()
    for ctx in contexts:
        predictions = bigram_model.predict_next(ctx)
        pred_str = " | ".join(f"{w} ({p:.3f})" for w, p in predictions)
        print(f"  Context: '{' '.join(ctx)}' -> {pred_str}")

    # -- Sentence probability ----------------------------------------------
    _separator("SENTENCE LOG-PROBABILITY SCORING (Bigram)")
    test_sentences = [
        "Maize leaves turn yellow when nitrogen is deficient.",
        "The robot flies over the ocean at midnight.",   # Very unlikely in farming
        "Spray fungicide to control blight on tomatoes.",
    ]
    print()
    for sent in test_sentences:
        lp = bigram_model.sentence_probability(sent)
        print(f"  Sentence: \"{sent}\"")
        print(f"  Log-prob: {lp:.4f}\n")

    # -- Perplexity --------------------------------------------------------
    _separator("MODEL PERPLEXITY (lower = better fit)")
    hold_out = [
        "Farmers should spray their crops to control disease.",
        "Apply fertilizer to improve maize yield in the field.",
    ]
    print()
    for label, model in [("Unigram", unigram_model),
                          ("Bigram",  bigram_model),
                          ("Trigram", trigram_model)]:
        pp = model.perplexity(hold_out)
        print(f"  {label} perplexity: {pp:.2f}")

    print()
    print("✅ Week 2 N-gram model demonstration complete.")
    print()
