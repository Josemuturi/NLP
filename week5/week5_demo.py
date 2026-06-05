"""
week5/week5_demo.py
==========================================================
BIT4133 - Natural Language Processing
Week 5: Complete NLP Pipeline + Academic Chatbot Demo

Covers:
  Part 1 - Complete NLP Pipeline (all Weeks 1-4 steps chained)
  Part 2 - Student Academic Assistant Chatbot (Mini Project)

No external libraries required - runs instantly.

RUN: python week5/week5_demo.py
"""

import re

SEP  = "=" * 65
SEP2 = "-" * 65
THIN = "." * 65


# ==============================================================
# PART 1: COMPLETE NLP PIPELINE
# ==============================================================

# ── Step data (pre-computed to avoid NLTK dependency) ────────
STOP_WORDS = {
    "i","my","the","a","an","is","are","was","were","be","been",
    "have","has","had","do","does","did","will","would","could",
    "should","may","might","shall","can","to","of","in","on",
    "at","by","for","with","about","as","into","through","during",
    "before","after","above","below","from","up","down","and",
    "or","but","if","then","that","this","it","its","not","no",
}

STEM_RULES = [
    ("ational", "ate"), ("tional", "tion"), ("enci", "ence"),
    ("anci", "ance"), ("ising", "ise"),   ("izing", "ize"),
    ("ising", "is"),   ("izing", "iz"),   ("izing", "iz"),
    ("ing", ""),       ("ness", ""),      ("ment", ""),
    ("tion", "t"),     ("ed", ""),        ("ly", ""),
    ("er", ""),        ("est", ""),       ("ful", ""),
    ("ous", ""),       ("al", ""),        ("ive", ""),
    ("ize", ""),       ("ise", ""),
]

POS_LOOKUP = {
    "maize":   "NN",  "crop":    "NN",  "soil":    "NN",
    "disease": "NN",  "rain":    "NN",  "leaf":    "NN",
    "leaves":  "NNS", "water":   "NN",  "farmer":  "NN",
    "tomato":  "NN",  "plant":   "NN",  "stem":    "NN",
    "yellow":  "JJ",  "dry":     "JJ",  "wet":     "JJ",
    "brown":   "JJ",  "good":    "JJ",  "bad":     "JJ",
    "wilting": "VBG", "turning": "VBG", "spray":   "VB",
    "apply":   "VB",  "harvest": "VB",  "detect":  "VB",
    "should":  "MD",  "need":    "MD",  "when":    "WRB",
    "my":      "PRP$","the":     "DT",  "a":       "DT",
}
POS_TAG_NAMES = {
    "NN":"Noun (singular)","NNS":"Noun (plural)","VB":"Verb (base)",
    "VBG":"Verb (gerund)","JJ":"Adjective","MD":"Modal verb",
    "DT":"Determiner","PRP$":"Possessive pronoun","WRB":"Wh-adverb",
    "IN":"Preposition","CC":"Conjunction","RB":"Adverb",
}


def simple_tokenize(text):
    return re.findall(r"[A-Za-z']+", text)


def simple_stem(word):
    w = word.lower()
    for suffix, replacement in STEM_RULES:
        if len(w) > len(suffix) + 2 and w.endswith(suffix):
            return w[:-len(suffix)] + replacement
    return w


def simple_lemma(word):
    """Very basic lemmatisation rules."""
    w = word.lower()
    irregulars = {
        "leaves":"leaf","are":"be","were":"be","was":"be",
        "turning":"turn","wilting":"wilt","dying":"die",
        "yellowing":"yellow","applies":"apply","sprays":"spray",
    }
    return irregulars.get(w, simple_stem(w))


def pos_tag(word):
    return POS_LOOKUP.get(word.lower(), "IN")


def run_pipeline(sentence: str):
    print(f"\n  Input sentence:")
    print(f"  \"{sentence}\"")
    print()

    # Step 1 – Tokenisation
    tokens = simple_tokenize(sentence)
    print(f"  Step 1 | TOKENISATION")
    print(f"  {'-'*55}")
    print(f"  Tokens ({len(tokens)}): {tokens}")
    print()

    # Step 2 – Lowercase
    tokens_lower = [t.lower() for t in tokens]
    print(f"  Step 2 | LOWERCASE NORMALISATION")
    print(f"  {'-'*55}")
    print(f"  {tokens_lower}")
    print()

    # Step 3 – Stop word removal
    filtered = [t for t in tokens_lower if t not in STOP_WORDS]
    removed  = [t for t in tokens_lower if t in STOP_WORDS]
    print(f"  Step 3 | STOP WORD REMOVAL")
    print(f"  {'-'*55}")
    print(f"  Removed   : {removed}")
    print(f"  Remaining : {filtered}")
    print()

    # Step 4 – Stemming
    stems = [simple_stem(t) for t in filtered]
    print(f"  Step 4 | STEMMING (Porter-style)")
    print(f"  {'-'*55}")
    for orig, stem in zip(filtered, stems):
        arrow = " -> " if orig != stem else " == "
        print(f"    {orig:<16}{arrow}{stem}")
    print()

    # Step 5 – Lemmatisation
    lemmas = [simple_lemma(t) for t in filtered]
    print(f"  Step 5 | LEMMATISATION")
    print(f"  {'-'*55}")
    for orig, lem in zip(filtered, lemmas):
        arrow = " -> " if orig != lem else " == "
        print(f"    {orig:<16}{arrow}{lem}")
    print()

    # Step 6 – POS Tagging
    tagged = [(t, pos_tag(t)) for t in filtered]
    print(f"  Step 6 | POS TAGGING")
    print(f"  {'-'*55}")
    print(f"  {'Token':<18} {'Tag':<8} Meaning")
    print(f"  {'-'*17} {'-'*7} {'-'*25}")
    for word, tag in tagged:
        meaning = POS_TAG_NAMES.get(tag, "Other")
        print(f"  {word:<18} {tag:<8} {meaning}")
    print()

    # Step 7 – N-gram generation
    bigrams  = [(filtered[i], filtered[i+1]) for i in range(len(filtered)-1)]
    trigrams = [(filtered[i], filtered[i+1], filtered[i+2]) for i in range(len(filtered)-2)]
    print(f"  Step 7 | N-GRAM ANALYSIS")
    print(f"  {'-'*55}")
    print(f"  Bigrams  : {bigrams}")
    print(f"  Trigrams : {trigrams if trigrams else '(sentence too short)'}")
    print()

    # Step 8 – Key terms summary
    nouns = [w for w, t in tagged if t in ("NN","NNS")]
    verbs = [w for w, t in tagged if t in ("VB","VBG","MD")]
    adjs  = [w for w, t in tagged if t == "JJ"]
    print(f"  Step 8 | SEMANTIC KEY TERM EXTRACTION")
    print(f"  {'-'*55}")
    print(f"  Nouns (topic)  : {nouns  if nouns  else '(none)'}")
    print(f"  Verbs (action) : {verbs  if verbs  else '(none)'}")
    print(f"  Adjectives     : {adjs   if adjs   else '(none)'}")
    print()
    print(f"  Pipeline complete for this sentence.")


# ==============================================================
# PART 2: ACADEMIC CHATBOT DEMO
# ==============================================================

RESPONSES = {
    "hello":         "Hi there! I am the BIT4133 NLP Academic Assistant. How can I help you?",
    "hi":            "Hello! How can I assist you with BIT4133 NLP today?",
    "cat 1":         "CAT 1 covers Weeks 1-5 topics: tokenization, stemming, n-grams, POS, HMM, dependency parsing, and semantic similarity.",
    "cat1":          "CAT 1 covers Weeks 1-5 topics: tokenization, stemming, n-grams, POS, HMM, dependency parsing, and semantic similarity.",
    "tokenization":  "Tokenization splits text into individual words or sentences. Use nltk.word_tokenize() for words, nltk.sent_tokenize() for sentences.",
    "tokenise":      "Tokenization splits text into individual words or sentences. Use nltk.word_tokenize() for words, nltk.sent_tokenize() for sentences.",
    "stemming":      "Stemming reduces a word to its base form by removing suffixes. Example: 'running' -> 'run'. Use PorterStemmer from NLTK.",
    "lemma":         "Lemmatization returns the dictionary form of a word using grammar rules. More accurate than stemming. Use WordNetLemmatizer from NLTK.",
    "lemmatization": "Lemmatization returns the dictionary form of a word using grammar rules. More accurate than stemming. Use WordNetLemmatizer from NLTK.",
    "pos":           "POS tagging assigns grammatical roles: NN=Noun, VB=Verb, JJ=Adjective, DT=Determiner. Use nltk.pos_tag(tokens).",
    "pos tagging":   "POS tagging assigns grammatical roles: NN=Noun, VB=Verb, JJ=Adjective, DT=Determiner. Use nltk.pos_tag(tokens).",
    "hmm":           "HMM (Hidden Markov Model) is a sequence labeler. In this project it labels each word as CROP, DISEASE, SYMPTOM, LOCATION, ACTION, or O.",
    "hidden markov": "HMM uses transitions P(label|prev_label) and emissions P(word|label). The Viterbi algorithm finds the best label sequence.",
    "viterbi":       "The Viterbi algorithm uses dynamic programming to find the most likely label sequence in O(N^2 * T) time.",
    "ngram":         "N-grams are sequences of N words. Bigrams=2 words, Trigrams=3 words. Used to model language patterns and predict next words.",
    "n-gram":        "N-grams are sequences of N words. Bigrams=2 words, Trigrams=3 words. Used to model language patterns and predict next words.",
    "dependency":    "Dependency parsing shows how words in a sentence relate grammatically. ROOT=main verb, nsubj=subject, dobj=object.",
    "spacy":         "spaCy is an NLP library used in Week 4. It provides fast dependency parsing and word vectors for semantic similarity.",
    "similarity":    "Semantic similarity measures how close two sentences are in meaning. Range: 0.0 (unrelated) to 1.0 (identical). Use doc.similarity() in spaCy.",
    "semantic":      "Semantic analysis is about meaning. Semantic similarity compares word vectors. Week 4 teaches this using spaCy.",
    "assignment":    "For assignments, always include: code snippet, explanation of output, screenshot, and a learning reflection paragraph.",
    "register":      "Unit registration is done through the student portal or registrar's office. Ensure fees are settled before registering.",
    "fees":          "Fee payment queries should be directed to the accounts office. You need a cleared fees balance to access exams.",
    "timetable":     "Check the official university notice board or website for the current exam and class timetable.",
    "goodbye":       "Goodbye! Good luck with your NLP studies. Remember to revise all 5 weeks for CAT 1!",
    "bye":           "Goodbye! Good luck with BIT4133!",
}

DEFAULT = "I don't have a specific answer for that. Try asking about: tokenization, stemming, lemmatization, POS tagging, HMM, n-grams, dependency parsing, or semantic similarity."


def get_response(user_input: str) -> str:
    text = user_input.lower().strip()
    # Exact match
    if text in RESPONSES:
        return RESPONSES[text]
    # Keyword match
    for key, resp in RESPONSES.items():
        if key in text:
            return resp
    return DEFAULT


def run_chatbot_demo():
    print()
    print(SEP)
    print("  STUDENT ACADEMIC ASSISTANT CHATBOT -- DEMO MODE")
    print("  BIT4133 NLP -- Week 5 Mini Project")
    print(SEP)
    print()
    print("  Description:")
    print("  A rule-based chatbot that answers questions about BIT4133")
    print("  NLP concepts, CAT 1 topics, and university admin queries.")
    print()
    print("  Architecture:")
    print("    Input  -> Lowercase normalisation -> Keyword matching")
    print("           -> Response lookup -> Formatted output")
    print()
    print("  Topics supported: tokenization, stemming, lemmatization,")
    print("  POS tagging, HMM, Viterbi, n-grams, dependency parsing,")
    print("  semantic similarity, CAT 1, registration, fees, timetable")
    print()
    print(SEP)
    print("  DEMO SESSION")
    print(SEP)

    conversations = [
        "Hello",
        "What is tokenization?",
        "Explain stemming",
        "What is lemmatization?",
        "Explain POS tagging",
        "What is an HMM?",
        "What is the Viterbi algorithm?",
        "Explain n-grams",
        "What is dependency parsing?",
        "What is semantic similarity?",
        "What topics are in CAT 1?",
        "How do I register for units?",
        "Goodbye",
    ]

    for user_msg in conversations:
        response = get_response(user_msg)
        print()
        print(f"  You : {user_msg}")
        print(f"  Bot : {response}")

    print()
    print(SEP2)
    print("  End of demo session.")
    print()


# ==============================================================
# MAIN
# ==============================================================

def main():
    print()
    print(SEP)
    print("  BIT4133 Natural Language Processing -- Week 5")
    print("  CAT 1 Preparation: Complete Pipeline + Mini Project")
    print(SEP)

    # ── PART 1: NLP Pipeline ──────────────────────────────────
    print()
    print(SEP)
    print("  PART 1: COMPLETE NLP PIPELINE (Weeks 1-4 Integrated)")
    print(SEP)
    print("""
  This pipeline chains all NLP preprocessing steps in order:
    Step 1 : Tokenisation     (Week 1)
    Step 2 : Lowercasing      (Week 1)
    Step 3 : Stop word removal(Week 1)
    Step 4 : Stemming         (Week 1)
    Step 5 : Lemmatisation    (Week 1)
    Step 6 : POS Tagging      (Week 2)
    Step 7 : N-gram analysis  (Week 2)
    Step 8 : Key term extract (Week 4)
    """)

    sentences = [
        "My maize leaves are turning yellow and wilting.",
        "The tomato plants have blight and the leaves are dry.",
        "When should I spray fungicide on my crop?",
    ]

    for i, sent in enumerate(sentences, 1):
        print(SEP)
        print(f"  SENTENCE {i} OF {len(sentences)}")
        print(SEP)
        run_pipeline(sent)

    # ── PART 2: Chatbot ───────────────────────────────────────
    run_chatbot_demo()

    print(SEP)
    print("  Week 5 demo complete.")
    print("  Screenshots to take for your logbook:")
    print("    - NLP Pipeline output for any 1 or 2 sentences (Step 1-8)")
    print("    - Full chatbot demo session showing questions & answers")
    print(SEP)
    print()


if __name__ == "__main__":
    main()
