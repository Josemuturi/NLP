"""
week3/hmm_demo.py
==========================================================
BIT4133 - Natural Language Processing
Week 3: Hidden Markov Model (HMM) - Standalone Demo

PURPOSE OF HMM IN THIS PROJECT:
  The HMM is used as a SEQUENCE LABELER (Named Entity Recogniser).
  It reads a farmer's sentence word by word and assigns each word
  an entity label:
    CROP     -> the plant being discussed (maize, tomato, rice)
    DISEASE  -> the disease affecting the crop (blight, rust)
    SYMPTOM  -> what the farmer can see (yellow, wilting, spots)
    LOCATION -> part of the plant (leaves, roots, stem)
    ACTION   -> what to do (spray, irrigate, fertilize)
    O        -> other/unimportant words (my, the, are, I)

  WHY HMM AND NOT JUST KEYWORD MATCHING?
  HMM considers CONTEXT - it looks at what label came BEFORE
  to decide the most likely label NOW. This is called a
  TRANSITION PROBABILITY. So "rust" after "bean" is more likely
  DISEASE than SYMPTOM, even though rust can mean both.

RUN: python week3/hmm_demo.py
No external libraries needed beyond Python standard library.
"""

import math


# ==============================================================
# 1. HMM PARAMETERS
# ==============================================================

# Entity labels (hidden states)
LABELS  = ["CROP", "DISEASE", "SYMPTOM", "LOCATION", "ACTION", "O"]
N       = len(LABELS)
IDX     = {l: i for i, l in enumerate(LABELS)}

# --- Simple vocabulary per label ----------------------------
VOCAB = {
    "CROP":     {"maize","tomato","potato","rice","bean","wheat","cassava","sorghum"},
    "DISEASE":  {"blight","rust","mosaic","wilt","mildew","rot","streak","smut"},
    "SYMPTOM":  {"yellow","yellowing","wilting","spots","brown","stunted","drooping","pale"},
    "LOCATION": {"leaves","leaf","roots","stem","stalk","fruit","flowers","soil"},
    "ACTION":   {"spray","irrigate","fertilize","water","prune","harvest","apply","remove"},
    "O":        set(),  # O handles everything else
}

# --- Emission probabilities P(word | label) ------------------
def emit_prob(label: str, word: str) -> float:
    w = word.lower().strip(".,?!")
    if label == "O":
        # O emits non-entity words with prob 0.10, entity words very rarely
        for lbl, vocab in VOCAB.items():
            if lbl != "O" and w in vocab:
                return 0.002
        return 0.10
    else:
        return 0.85 if w in VOCAB[label] else 0.002

# --- Transition matrix P(label_j | label_i) -----------------
#     rows = from, cols = to
#     LABELS = [CROP, DISEASE, SYMPTOM, LOCATION, ACTION, O]
A = [
    [0.05, 0.15, 0.20, 0.25, 0.10, 0.25],  # from CROP
    [0.05, 0.08, 0.22, 0.15, 0.15, 0.35],  # from DISEASE
    [0.05, 0.08, 0.18, 0.28, 0.10, 0.31],  # from SYMPTOM
    [0.05, 0.08, 0.10, 0.10, 0.22, 0.45],  # from LOCATION
    [0.12, 0.12, 0.08, 0.08, 0.10, 0.50],  # from ACTION
    [0.12, 0.10, 0.10, 0.10, 0.10, 0.48],  # from O
]

# --- Initial probabilities P(label at position 0) ------------
PI = [0.12, 0.04, 0.05, 0.04, 0.12, 0.63]


# ==============================================================
# 2. VITERBI ALGORITHM
# ==============================================================

def viterbi(tokens: list):
    """
    Find the most likely sequence of labels for a list of tokens.
    Uses dynamic programming (log probabilities to avoid underflow).

    Returns: (best_labels, V_matrix, backpointers)
    """
    T = len(tokens)

    # V[t][s] = best log-probability of reaching state s at time t
    V = [[float("-inf")] * N for _ in range(T)]
    B = [[0]              * N for _ in range(T)]  # backpointers

    # -- Initialisation (t=0) --
    for s in range(N):
        p = PI[s] * emit_prob(LABELS[s], tokens[0])
        V[0][s] = math.log(p) if p > 0 else float("-inf")

    # -- Recursion (t=1..T-1) --
    for t in range(1, T):
        for s in range(N):
            ep = emit_prob(LABELS[s], tokens[t])
            el = math.log(ep) if ep > 0 else float("-inf")

            best_score, best_prev = float("-inf"), 0
            for prev_s in range(N):
                tp = A[prev_s][s]
                tl = math.log(tp) if tp > 0 else float("-inf")
                score = V[t-1][prev_s] + tl
                if score > best_score:
                    best_score, best_prev = score, prev_s

            V[t][s] = best_score + el
            B[t][s] = best_prev

    # -- Backtracking --
    path = [0] * T
    path[T-1] = max(range(N), key=lambda s: V[T-1][s])
    for t in range(T-2, -1, -1):
        path[t] = B[t+1][path[t+1]]

    best_labels = [LABELS[s] for s in path]
    return best_labels, V, B


# ==============================================================
# 3. DISPLAY HELPERS
# ==============================================================

SEP  = "=" * 65
SEP2 = "-" * 65

LABEL_MEANINGS = {
    "CROP":     "Crop or plant name",
    "DISEASE":  "Disease or pathogen",
    "SYMPTOM":  "Visible symptom",
    "LOCATION": "Part of the plant",
    "ACTION":   "Farmer action / remedy",
    "O":        "Other (function word)",
}


def show_label_table(tokens, labels):
    print(f"\n  {'TOKEN':<16}  {'ASSIGNED LABEL':<14}  MEANING")
    print(f"  {'-'*15}  {'-'*13}  {'-'*24}")
    for word, label in zip(tokens, labels):
        meaning = LABEL_MEANINGS.get(label, "")
        marker  = " <-- ENTITY" if label != "O" else ""
        print(f"  {word:<16}  {label:<14}  {meaning}{marker}")


def show_viterbi_matrix(tokens, V):
    print(f"\n  Viterbi Log-Probability Matrix")
    print(f"  (columns = tokens, rows = states)")
    print()
    # Header
    header = f"  {'STATE':<10}" + "".join(f"  {tok:<12}" for tok in tokens)
    print(header)
    print("  " + "-" * (10 + 14 * len(tokens)))
    for s in range(N):
        row = f"  {LABELS[s]:<10}"
        for t in range(len(tokens)):
            val = V[t][s]
            if val == float("-inf"):
                row += f"  {'−inf':<12}"
            else:
                row += f"  {val:<12.4f}"
        print(row)


def show_entities(tokens, labels, query):
    entities = {l: [] for l in LABELS if l != "O"}
    cur_words, cur_label = [], "O"
    for word, label in zip(tokens, labels):
        if label == "O":
            if cur_label != "O" and cur_words:
                entities[cur_label].append(" ".join(cur_words))
            cur_words, cur_label = [], "O"
        elif label == cur_label:
            cur_words.append(word)
        else:
            if cur_label != "O" and cur_words:
                entities[cur_label].append(" ".join(cur_words))
            cur_words, cur_label = [word], label
    if cur_label != "O" and cur_words:
        entities[cur_label].append(" ".join(cur_words))

    print(f"\n  Extracted Entities:")
    found = False
    for lbl in ["CROP", "DISEASE", "SYMPTOM", "LOCATION", "ACTION"]:
        vals = [e.lower() for e in entities[lbl] if e]
        if vals:
            found = True
            print(f"    {lbl:<12} -> {', '.join(vals)}")
    if not found:
        print("    (No specific farming entities detected)")


# ==============================================================
# 4. MAIN DEMONSTRATION
# ==============================================================

def main():
    print()
    print(SEP)
    print("  BIT4133 Natural Language Processing - Week 3")
    print("  Hidden Markov Model (HMM) - Sequence Labeling")
    print(SEP)

    # ── WHAT IS HMM? ──────────────────────────────────────────
    print("""
  WHAT IS A HIDDEN MARKOV MODEL (HMM)?
  -------------------------------------
  An HMM is a probabilistic model that assigns labels to sequences.
  In this project it acts as a Named Entity Recogniser (NER):
  it reads each word in a farmer's query and labels it.

  HMM COMPONENTS:
    States (S)       : The entity labels we want to find
                       [CROP, DISEASE, SYMPTOM, LOCATION, ACTION, O]

    Observations (O) : The actual words in the sentence
                       e.g. ["My", "maize", "leaves", "are", "yellow"]

    Transitions (A)  : P(next label | current label)
                       e.g. after CROP -> likely LOCATION (0.25)

    Emissions (B)    : P(word | label)
                       e.g. P("maize" | CROP) = 0.85

    Initial (pi)     : P(label at word 0)
                       Most sentences start with O (0.63)

    Algorithm        : Viterbi - finds the globally best label
                       sequence using dynamic programming O(N^2 T)
    """)

    # ── HMM PARAMETERS ────────────────────────────────────────
    print(SEP)
    print("  HMM PARAMETERS")
    print(SEP)
    print(f"\n  States (N={N})    : {LABELS}")
    print(f"\n  Initial probabilities (pi):")
    for i, lbl in enumerate(LABELS):
        print(f"    P(start={lbl:<10}) = {PI[i]}")
    print(f"\n  Transition matrix A  [sample row for CROP]:")
    print(f"    From CROP ->  ", end="")
    for i, lbl in enumerate(LABELS):
        print(f"{lbl}:{A[0][i]}  ", end="")
    print()

    # ── PROCESS QUERIES ───────────────────────────────────────
    queries = [
        "My maize leaves are turning yellow.",
        "The tomato plants have blight and the leaves are wilting.",
        "I need to spray fungicide on my potato crop.",
        "The bean rust is spreading on the leaves quickly.",
        "When should I irrigate my rice field?",
    ]

    for i, query in enumerate(queries, 1):
        # Simple tokenisation (avoid nltk dependency for speed)
        tokens = query.replace(".", " ").replace(",", " ").replace("?", " ").split()

        print()
        print(SEP)
        print(f"  Query {i}: \"{query}\"")
        print(SEP)
        print(f"  Tokens: {tokens}")

        labels, V, _ = viterbi(tokens)

        show_label_table(tokens, labels)
        show_entities(tokens, labels, query)

    # ── VITERBI MATRIX DETAIL ─────────────────────────────────
    print()
    print(SEP)
    print("  VITERBI MATRIX DETAIL - Short Example")
    print(SEP)
    example = "maize leaves wilting"
    tokens  = example.split()
    labels, V, _ = viterbi(tokens)

    print(f"\n  Input sentence : \"{example}\"")
    print(f"  Tokens         : {tokens}")

    show_viterbi_matrix(tokens, V)

    print(f"\n  Best label path: {list(zip(tokens, labels))}")
    print(f"\n  INTERPRETATION:")
    print(f"    'maize'   -> CROP     (word found in CROP vocabulary)")
    print(f"    'leaves'  -> LOCATION (plant part, follows CROP in sequence)")
    print(f"    'wilting' -> SYMPTOM  (symptom word, follows LOCATION)")
    print(f"\n  The Viterbi algorithm found the globally optimal path by")
    print(f"  considering BOTH emission and transition probabilities together.")

    print()
    print(SEP)
    print("  Week 3 HMM demo complete.")
    print("  Take a screenshot of this output for your logbook (Section 3.5).")
    print(SEP)
    print()


if __name__ == "__main__":
    main()
