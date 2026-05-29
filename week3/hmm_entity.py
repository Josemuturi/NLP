"""
week3/hmm_entity.py - Smart Farm HMM Sequence Labeling (Week 3)
================================================================
Demonstrates:
  - Hidden Markov Model (HMM) theory applied to sequence labeling
  - Named Entity Recognition for farming text using the Viterbi algorithm
  - Entity labels: CROP, DISEASE, SYMPTOM, LOCATION, ACTION, O (other)
  - Emission and transition probability matrices seeded from vocabulary knowledge

HMM Notation:
  States (S)       : Entity labels - CROP, DISEASE, SYMPTOM, LOCATION, ACTION, O
  Observations (O) : Words in the farmer's message
  Transitions (A)  : P(state_t | state_{t-1})
  Emissions (B)    : P(word | state)
  Initial (π)      : P(state_0)

Course: BIT4133 Natural Language Processing - Week 3
Project: Smart Farm AI Assistant
"""

import sys
import os
import math
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "week1"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "week2"))

import nltk
nltk.download("punkt",      quiet=True)
nltk.download("punkt_tab",  quiet=True)
from nltk.tokenize import word_tokenize

from knowledge_base import (
    CROP_VOCAB, DISEASE_VOCAB, SYMPTOM_VOCAB,
    LOCATION_VOCAB, ACTION_VOCAB
)


# =============================================================================
# HMM ENTITY LABELS
# =============================================================================

LABELS = ["CROP", "DISEASE", "SYMPTOM", "LOCATION", "ACTION", "O"]

# Label index mapping
LABEL_IDX = {label: i for i, label in enumerate(LABELS)}
IDX_LABEL  = {i: label for i, label in enumerate(LABELS)}

# Number of states
N_STATES = len(LABELS)

# Label -> Color for display
LABEL_COLORS = {
    "CROP":     "\033[92m",   # green
    "DISEASE":  "\033[91m",   # red
    "SYMPTOM":  "\033[93m",   # yellow
    "LOCATION": "\033[94m",   # blue
    "ACTION":   "\033[95m",   # magenta
    "O":        "\033[0m",    # reset (default)
}
RESET = "\033[0m"


# =============================================================================
# HMM PARAMETER INITIALIZATION
# =============================================================================

def _build_emission_probs() -> dict:
    """
    Build emission probability table P(word | label).

    Strategy:
      - Entity states (CROP, DISEASE, etc.): words in their vocabulary get
        a fixed HIGH emission of 0.90; everything else gets 0.001.
      - O state: in-entity words get 0.002 (very low); everything else 0.05.

    This ensures that when a word like 'maize' is seen, the CROP state
    scores far higher than O, driving the Viterbi path away from O.

    Returns:
        dict: label -> {word -> probability}
    """
    VOCAB_MAP = {
        "CROP":     set(CROP_VOCAB),
        "DISEASE":  set(DISEASE_VOCAB),
        "SYMPTOM":  set(SYMPTOM_VOCAB),
        "LOCATION": set(LOCATION_VOCAB),
        "ACTION":   set(ACTION_VOCAB),
    }

    # Collect all in-entity words for use when building O emissions
    all_entity_words = set()
    for vocab in VOCAB_MAP.values():
        all_entity_words.update(w.lower() for w in vocab)

    emission = {}

    for label in LABELS:
        if label == "O":
            # O emits non-entity words freely; emits entity words rarely
            o_default   = 0.05   # background for unknown words
            o_entity    = 0.002  # very low for entity-vocab words
            base = defaultdict(lambda: o_default)
            for word in all_entity_words:
                base[word] = o_entity
            emission[label] = base
        else:
            vocab = VOCAB_MAP[label]
            # Fixed high emission for in-vocab words; tiny for everything else
            IN_PROB    = 0.90
            BACKGROUND = 0.001
            base = defaultdict(lambda: BACKGROUND)
            for word in vocab:
                base[word.lower()] = IN_PROB
            emission[label] = base

    return emission


def _build_transition_probs() -> list:
    """
    Build transition probability matrix A[i][j] = P(label_j | label_i).
    
    These are hand-crafted based on typical entity sequences in farming text.
    E.g., a CROP label is often followed by LOCATION or SYMPTOM.
    
    Returns:
        2D list of shape [N_STATES × N_STATES]
    """
    # A[from_state][to_state]
    # LABELS = ["CROP", "DISEASE", "SYMPTOM", "LOCATION", "ACTION", "O"]
    #           idx 0    idx 1      idx 2       idx 3       idx 4     idx 5

    A = [
        # From CROP -> can go to: DISEASE, SYMPTOM, LOCATION, ACTION, O
        [0.05, 0.15, 0.20, 0.25, 0.10, 0.25],  # from CROP
        # From DISEASE -> can go to: SYMPTOM, LOCATION, ACTION, O
        [0.05, 0.10, 0.20, 0.15, 0.15, 0.35],  # from DISEASE
        # From SYMPTOM -> often goes to: LOCATION, ACTION, O, another SYMPTOM
        [0.05, 0.10, 0.20, 0.25, 0.10, 0.30],  # from SYMPTOM
        # From LOCATION -> often O or ACTION
        [0.05, 0.10, 0.10, 0.10, 0.20, 0.45],  # from LOCATION
        # From ACTION -> often CROP, DISEASE, O
        [0.10, 0.15, 0.10, 0.10, 0.10, 0.45],  # from ACTION
        # From O -> can transition to any entity label or stay O
        [0.10, 0.10, 0.10, 0.10, 0.10, 0.50],  # from O
    ]
    return A


def _build_initial_probs() -> list:
    """
    Build initial state probability vector π[i] = P(label_i at start).
    
    Sentences often start with O words (my, the, I) before entities.
    """
    # [CROP, DISEASE, SYMPTOM, LOCATION, ACTION, O]
    pi = [0.15, 0.05, 0.05, 0.05, 0.15, 0.55]
    return pi


# =============================================================================
# VITERBI ALGORITHM
# =============================================================================

class FarmingHMM:
    """
    Hidden Markov Model for entity sequence labeling in farming text.
    Uses the Viterbi algorithm to find the most likely label sequence.
    """

    def __init__(self):
        self.emission   = _build_emission_probs()
        self.transition = _build_transition_probs()
        self.initial    = _build_initial_probs()

    def _emit_prob(self, label: str, word: str) -> float:
        """Get emission probability P(word | label) with smoothing."""
        return self.emission[label].get(word.lower(),
               self.emission[label][word.lower()])   # uses defaultdict

    def viterbi(self, tokens: list) -> tuple:
        """
        Run the Viterbi algorithm to find the most likely label sequence.

        Args:
            tokens: List of word tokens

        Returns:
            Tuple: (best_labels, viterbi_matrix, backpointer_matrix)
            - best_labels: List of predicted labels, one per token
        """
        T = len(tokens)   # sequence length
        N = N_STATES      # number of states

        if T == 0:
            return [], [], []

        # Viterbi table V[t][s] = max log-prob of reaching state s at time t
        V = [[float("-inf")] * N for _ in range(T)]

        # Backpointer B[t][s] = previous state that led to max probability
        B = [[0] * N for _ in range(T)]

        # -- Initialization (t = 0) ----------------------------------------
        for s in range(N):
            label  = IDX_LABEL[s]
            emit_p = self._emit_prob(label, tokens[0])
            # Use log to avoid underflow
            emit_log = math.log(emit_p) if emit_p > 0 else float("-inf")
            init_log = math.log(self.initial[s]) if self.initial[s] > 0 else float("-inf")
            V[0][s] = init_log + emit_log
            B[0][s] = 0

        # -- Recursion -----------------------------------------------------
        for t in range(1, T):
            for s in range(N):
                label    = IDX_LABEL[s]
                emit_p   = self._emit_prob(label, tokens[t])
                emit_log = math.log(emit_p) if emit_p > 0 else float("-inf")

                # Find best previous state
                best_prev_log = float("-inf")
                best_prev     = 0
                for prev_s in range(N):
                    trans_p   = self.transition[prev_s][s]
                    trans_log = math.log(trans_p) if trans_p > 0 else float("-inf")
                    score     = V[t-1][prev_s] + trans_log
                    if score > best_prev_log:
                        best_prev_log = score
                        best_prev     = prev_s

                V[t][s] = best_prev_log + emit_log
                B[t][s] = best_prev

        # -- Termination ---------------------------------------------------
        best_last_state = max(range(N), key=lambda s: V[T-1][s])

        # -- Backtracking -------------------------------------------------
        best_path = [0] * T
        best_path[T-1] = best_last_state
        for t in range(T-2, -1, -1):
            best_path[t] = B[t+1][best_path[t+1]]

        best_labels = [IDX_LABEL[s] for s in best_path]
        return best_labels, V, B

    def label_sentence(self, text: str) -> list:
        """
        Tokenize and label a farming sentence.

        Returns:
            List of (word, label) tuples
        """
        tokens = word_tokenize(text)
        labels, _, _ = self.viterbi(tokens)
        return list(zip(tokens, labels))

    def extract_entities(self, text: str) -> dict:
        """
        Extract all named entities from a farmer's message.

        Returns:
            dict: entity_type -> list of entity values
        """
        labeled = self.label_sentence(text)
        entities: dict = {label: [] for label in LABELS if label != "O"}

        current_entity = []
        current_label  = "O"

        for word, label in labeled:
            if label == "O":
                if current_label != "O" and current_entity:
                    entities[current_label].append(" ".join(current_entity))
                current_entity = []
                current_label  = "O"
            elif label == current_label:
                current_entity.append(word)
            else:
                if current_label != "O" and current_entity:
                    entities[current_label].append(" ".join(current_entity))
                current_entity = [word]
                current_label  = label

        if current_label != "O" and current_entity:
            entities[current_label].append(" ".join(current_entity))

        # De-duplicate
        for key in entities:
            entities[key] = list(dict.fromkeys(e.lower() for e in entities[key]))

        return entities


# =============================================================================
# DISPLAY HELPERS
# =============================================================================

def print_labeled_sentence(labeled: list):
    """Print tokens with color-coded entity labels."""
    print("\n  Labeled sequence (color-coded):")
    print("  ", end="")
    for word, label in labeled:
        color = LABEL_COLORS.get(label, "")
        if label != "O":
            print(f"{color}[{word}/{label}]{RESET}", end=" ")
        else:
            print(f"{word}", end=" ")
    print()

    print("\n  Token-by-token label table:")
    print(f"  {'TOKEN':<18} {'LABEL':<12} {'MEANING'}")
    print(f"  {'-'*16}   {'-'*10}   {'-'*20}")
    label_meanings = {
        "CROP":     "Crop/plant name",
        "DISEASE":  "Disease/pathogen",
        "SYMPTOM":  "Visual symptom",
        "LOCATION": "Plant part",
        "ACTION":   "Farmer action/verb",
        "O":        "Other/function word",
    }
    for word, label in labeled:
        meaning = label_meanings.get(label, "")
        print(f"  {word:<18} {label:<12} {meaning}")


def print_entities(entities: dict, query: str):
    """Print extracted entities in a structured way."""
    print(f"\n  Extracted Entities from: \"{query}\"")
    print(f"  {'-'*55}")
    has_any = False
    for label in ["CROP", "DISEASE", "SYMPTOM", "LOCATION", "ACTION"]:
        vals = entities.get(label, [])
        if vals:
            has_any = True
            color = LABEL_COLORS.get(label, "")
            print(f"  {color}{label:<12}{RESET}: {', '.join(vals)}")
    if not has_any:
        print("  (No entities detected - try more specific farming terms)")


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print()
    print("=" * 65)
    print("   SMART FARM - Week 3: HMM Sequence Labeling")
    print("   Course: BIT4133 Natural Language Processing")
    print("=" * 65)

    hmm = FarmingHMM()

    # -- HMM Theory summary ------------------------------------------------
    print("\n📐 HMM Architecture:")
    print(f"   States (S)      : {LABELS}")
    print(f"   Observations (O): Words in farmer messages")
    print(f"   Transitions (A) : {N_STATES} × {N_STATES} matrix")
    print(f"   Emissions (B)   : State -> word probability mapping")
    print(f"   Algorithm       : Viterbi (dynamic programming)")
    print(f"   Initial π       : {hmm.initial}")

    # -- Test queries -----------------------------------------------------
    test_queries = [
        "My maize leaves are turning yellow.",
        "The tomato plants have blight and the leaves are wilting.",
        "I need to spray fungicide on my potato crop.",
        "The bean rust spots are spreading on the leaves quickly.",
        "When should I irrigate my rice field during dry weather?",
    ]

    print(f"\n\nProcessing {len(test_queries)} farmer queries through HMM labeler...\n")

    for i, query in enumerate(test_queries, start=1):
        print(f"\n{'='*65}")
        print(f"  Query {i}: {query}")
        print(f"{'='*65}")

        # Label sequence
        labeled = hmm.label_sentence(query)
        print_labeled_sentence(labeled)

        # Extract entities
        entities = hmm.extract_entities(query)
        print_entities(entities, query)
        print()

    # -- Viterbi matrix display for one example ---------------------------
    print("=" * 65)
    print("  VITERBI MATRIX (log-probabilities) for short example")
    print("=" * 65)
    example = "maize leaves wilting"
    tokens  = word_tokenize(example)
    labels, V, B = hmm.viterbi(tokens)

    print(f"\n  Sentence: \"{example}\"")
    print(f"  Tokens  : {tokens}\n")

    header = f"  {'STATE':<12}" + "".join(f"  {t:<10}" for t in tokens)
    print(header)
    print("  " + "-" * (12 + 12 * len(tokens)))
    for s in range(N_STATES):
        row = f"  {LABELS[s]:<12}"
        for t in range(len(tokens)):
            val = V[t][s]
            row += f"  {val:<10.3f}" if val != float("-inf") else f"  {'−∞':<10}"
        print(row)

    print(f"\n  Best label path: {list(zip(tokens, labels))}")
    print()
    print("✅ Week 3 HMM sequence labeling demonstration complete.")
    print()
