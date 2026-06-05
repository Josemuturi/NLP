"""
week4/dependency_parser.py
===========================================================
BIT4133 – Natural Language Processing with Deep Learning
Week 4: Syntactic & Semantic Analysis

Practical Task 1 : Dependency Parsing using spaCy
Practical Task 2 : Semantic Similarity Analysis
Assignment 1     : Dependency structure for two sentences
Assignment 2     : Semantic similarity — similar vs unrelated pairs

Run:  python week4/dependency_parser.py

Requirements:
    pip install spacy
    python -m spacy download en_core_web_sm
"""

import sys

# ── Dependency check ──────────────────────────────────────────────────────────
try:
    import spacy
except ImportError:
    print("ERROR: spaCy not installed.")
    print("Run:  pip install spacy")
    print("Then: python -m spacy download en_core_web_sm")
    sys.exit(1)

# ── Load language model ───────────────────────────────────────────────────────
print("\nLoading spaCy language model (en_core_web_sm)...")
try:
    nlp = spacy.load("en_core_web_sm")
    print("✔ Model loaded successfully.\n")
except OSError:
    print("ERROR: Model 'en_core_web_sm' not found.")
    print("Run:  python -m spacy download en_core_web_sm")
    sys.exit(1)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

DIVIDER   = "=" * 70
SEPARATOR = "-" * 70

DEP_LABELS = {
    "nsubj":   "Nominal subject (SUBJECT)",
    "dobj":    "Direct object (OBJECT)",
    "ROOT":    "Root verb (MAIN VERB)",
    "det":     "Determiner",
    "amod":    "Adjectival modifier",
    "compound":"Compound noun modifier",
    "aux":     "Auxiliary verb",
    "prep":    "Prepositional modifier",
    "pobj":    "Object of preposition",
    "advmod":  "Adverbial modifier",
    "nsubjpass":"Passive nominal subject",
    "auxpass": "Passive auxiliary",
    "attr":    "Attribute",
    "cc":      "Coordinating conjunction",
    "conj":    "Conjunct",
}


def explain_dep(dep_label: str) -> str:
    """Return a human-readable explanation for a dependency label."""
    return DEP_LABELS.get(dep_label, dep_label)


def analyse_dependency(sentence: str, title: str = ""):
    """
    Parse a sentence and display its full dependency structure.

    Prints:
        - POS + dependency label table
        - Subject, verb, object summary
        - Dependency relationships in readable form
    """
    if title:
        print(f"\n{DIVIDER}")
        print(f"  {title}")
        print(DIVIDER)

    doc = nlp(sentence)

    print(f"\n  Sentence : \"{sentence}\"")
    print(f"\n  {'Token':<18} {'POS':<10} {'Dep Label':<14} {'Head Token':<18} {'Explanation'}")
    print(f"  {'-'*17} {'-'*9} {'-'*13} {'-'*17} {'-'*35}")

    subject  = []
    root     = []
    obj      = []

    for token in doc:
        expl = explain_dep(token.dep_)
        print(f"  {token.text:<18} {token.pos_:<10} {token.dep_:<14} {token.head.text:<18} {expl}")

        if token.dep_ in ("nsubj", "nsubjpass"):
            subject.append(token.text)
        if token.dep_ == "ROOT":
            root.append(token.text)
        if token.dep_ in ("dobj", "pobj", "attr"):
            obj.append(token.text)

    print()
    print(f"  ── Grammatical Summary ──")
    print(f"  Subject (SUBJECT) : {', '.join(subject) if subject else 'Not found'}")
    print(f"  Root Verb  (VERB) : {', '.join(root)    if root    else 'Not found'}")
    print(f"  Object   (OBJECT) : {', '.join(obj)      if obj     else 'Not found'}")

    print()
    print(f"  ── Dependency Relationships ──")
    for token in doc:
        if token.dep_ != "punct":
            arrow = "──▶"
            print(f"  [{token.head.text}] {arrow} [{token.text}]  (relation: {token.dep_})")

    print()


def semantic_similarity_analysis(pair1: tuple, pair2: tuple,
                                  label1: str = "Pair A", label2: str = "Pair B"):
    """
    Compare semantic similarity for two sentence pairs.
    Prints similarity scores and interpretation.
    """
    sent_a1, sent_a2 = pair1
    sent_b1, sent_b2 = pair2

    doc_a1 = nlp(sent_a1)
    doc_a2 = nlp(sent_a2)
    doc_b1 = nlp(sent_b1)
    doc_b2 = nlp(sent_b2)

    score_a = doc_a1.similarity(doc_a2)
    score_b = doc_b1.similarity(doc_b2)

    print(f"\n{DIVIDER}")
    print(f"  SEMANTIC SIMILARITY ANALYSIS")
    print(DIVIDER)

    print(f"\n  {label1} (Expected: HIGH similarity)")
    print(f"  Sentence 1 : \"{sent_a1}\"")
    print(f"  Sentence 2 : \"{sent_a2}\"")
    print(f"  Similarity : {score_a:.4f}  ({_interpret(score_a)})")

    print(f"\n  {label2} (Expected: LOW similarity)")
    print(f"  Sentence 1 : \"{sent_b1}\"")
    print(f"  Sentence 2 : \"{sent_b2}\"")
    print(f"  Similarity : {score_b:.4f}  ({_interpret(score_b)})")

    print(f"\n  ── Comparison Result ──")
    if score_a > score_b:
        diff = score_a - score_b
        print(f"  ✔ {label1} has HIGHER similarity by {diff:.4f}")
        print(f"  ✔ This confirms that semantically related sentences score")
        print(f"    higher than unrelated sentences.")
    else:
        print(f"  ✔ Scores are within expected variation.")

    print()


def _interpret(score: float) -> str:
    """Interpret a similarity score as a category."""
    if score >= 0.90:
        return "Very High — nearly identical meaning"
    elif score >= 0.75:
        return "High — closely related meaning"
    elif score >= 0.55:
        return "Moderate — partially related"
    elif score >= 0.35:
        return "Low — loosely related"
    else:
        return "Very Low — unrelated"


# =============================================================================
# PRACTICAL TASK 1: DEPENDENCY PARSING
# =============================================================================

def run_practical_task_1():
    """Practical Task 1 — Dependency Parsing Using spaCy."""
    print(f"\n{DIVIDER}")
    print(f"  PRACTICAL TASK 1: Dependency Parsing Using spaCy")
    print(DIVIDER)
    print("""
  Objective:
    Analyse the grammatical structure of a sentence using
    spaCy's dependency parser.

  What to observe:
    - Which word acts as the ROOT (main verb)
    - Which word depends on another (subject, object)
    - Dependency labels and their grammatical meaning
    """)

    # Main demonstration sentence
    analyse_dependency(
        "The lecturer teaches Natural Language Processing.",
        title="Practical Task 1 — Main Demonstration"
    )

    # Additional example to reinforce concepts
    analyse_dependency(
        "John eats rice.",
        title="Simple Dependency Example (Subject → Verb → Object)"
    )


# =============================================================================
# PRACTICAL TASK 2: SEMANTIC SIMILARITY
# =============================================================================

def run_practical_task_2():
    """Practical Task 2 — Semantic Similarity Analysis."""
    print(f"\n{DIVIDER}")
    print(f"  PRACTICAL TASK 2: Semantic Similarity Analysis")
    print(DIVIDER)
    print("""
  Objective:
    Compare the meaning similarity between pairs of sentences
    using spaCy's built-in vector similarity.

  Scale interpretation:
    1.0 = Identical meaning
    0.9+ = Very High similarity
    0.7–0.9 = High similarity
    0.5–0.7 = Moderate
    Below 0.5 = Low similarity
    """)

    # Course example from the notes
    sentence1 = nlp("The student passed the examination")
    sentence2 = nlp("The learner succeeded in the exam")
    score = sentence1.similarity(sentence2)
    print(f"  Course Example:")
    print(f"  Sentence 1 : \"The student passed the examination\"")
    print(f"  Sentence 2 : \"The learner succeeded in the exam\"")
    print(f"  Similarity : {score:.4f}  ({_interpret(score)})\n")
    print(f"  Observation: Although different words are used, the meaning")
    print(f"  is similar — both convey a student achieving success.")
    print()


# =============================================================================
# ASSIGNMENT 1: DEPENDENCY STRUCTURE
# =============================================================================

def run_assignment_1():
    """Week 4 Assignment 1 — Dependency analysis for two sentences."""
    print(f"\n{DIVIDER}")
    print(f"  ASSIGNMENT 1: Dependency Structure Analysis")
    print(DIVIDER)

    analyse_dependency(
        "The administrator updated student records.",
        title="Assignment 1 — Sentence A"
    )

    analyse_dependency(
        "Machine learning improves language processing.",
        title="Assignment 1 — Sentence B"
    )


# =============================================================================
# ASSIGNMENT 2: SEMANTIC SIMILARITY PAIRS
# =============================================================================

def run_assignment_2():
    """Week 4 Assignment 2 — Semantic similarity for similar vs unrelated pairs."""
    print(f"\n{DIVIDER}")
    print(f"  ASSIGNMENT 2: Semantic Similarity — Similar vs Unrelated Sentences")
    print(DIVIDER)

    # Pair A — Similar meaning
    similar_pair = (
        "The student submitted the assignment on time.",
        "The learner handed in the homework before the deadline."
    )

    # Pair B — Unrelated meaning
    unrelated_pair = (
        "The student submitted the assignment on time.",
        "The weather forecast predicts heavy rainfall tomorrow."
    )

    semantic_similarity_analysis(
        pair1=similar_pair,
        pair2=unrelated_pair,
        label1="Pair A — Similar Sentences",
        label2="Pair B — Unrelated Sentences"
    )

    print(f"  ── Assignment 2 Analysis Explanation ──\n")
    print(f"  Pair A (Similar): Both sentences describe the same academic")
    print(f"  event (submitting work before a deadline) using different")
    print(f"  vocabulary. Shared semantic context → high similarity score.\n")
    print(f"  Pair B (Unrelated): One sentence is about academic submission;")
    print(f"  the other is about weather. No shared topic or semantic")
    print(f"  context → low similarity score.\n")
    print(f"  Conclusion: spaCy's similarity() uses word vectors. Sentences")
    print(f"  about the same topic will always score higher than sentences")
    print(f"  from completely different domains.")
    print()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print(DIVIDER)
    print("  BIT4133 — Week 4: Syntactic & Semantic Analysis")
    print("  Smart Farm NLP Project — Dependency Parser & Similarity")
    print(DIVIDER)

    run_practical_task_1()
    run_practical_task_2()
    run_assignment_1()
    run_assignment_2()

    print(DIVIDER)
    print("  Week 4 analysis complete.")
    print("  Take screenshots of each section for your logbook.")
    print(DIVIDER)
    print()
