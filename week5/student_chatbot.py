"""
week5/student_chatbot.py
===========================================================
BIT4133 – Natural Language Processing with Deep Learning
Week 5: CAT 1 Preparation — Student Academic Assistant Chatbot

Mini Project: Rule-based chatbot for student academic queries.

Features:
  - Greeting responses
  - CAT 1 schedule information
  - Unit registration guidance
  - NLP topic help
  - Graceful exit

Run:  python week5/student_chatbot.py

No external libraries required (pure Python).
"""

import sys
import time
import random

# =============================================================================
# CHATBOT KNOWLEDGE BASE
# =============================================================================

# Response patterns: (list of trigger keywords, list of possible responses)
RESPONSE_PATTERNS = [

    # ── Greetings ──────────────────────────────────────────────────────────
    (
        ["hello", "hi", "hey", "good morning", "good afternoon",
         "good evening", "howdy", "greetings"],
        [
            "Hello! I am the Student Academic Assistant for BIT4133. How can I help you today?",
            "Hi there! Welcome to the BIT4133 NLP Academic Assistant. What can I do for you?",
            "Good day! I am ready to assist you with NLP course queries. Ask away!",
        ]
    ),

    # ── CAT / Assessment schedule ──────────────────────────────────────────
    (
        ["cat", "cat1", "cat 1", "continuous assessment", "test", "exam",
         "assessment", "evaluation", "schedule", "when", "date"],
        [
            "CAT 1 is scheduled to take place next week. It will cover Weeks 1–5 topics.",
            "The CAT 1 assessment covers: Tokenization, POS Tagging, N-grams, HMM basics, "
            "Parsing, Semantic Similarity, and the NLP preprocessing pipeline.",
            "CAT 1 is coming up next week! Revise Weeks 1–4 concepts thoroughly. "
            "Focus on tokenization, stemming, POS tagging, and dependency parsing.",
        ]
    ),

    # ── Unit registration ──────────────────────────────────────────────────
    (
        ["register", "registration", "unit", "course", "enroll", "add unit",
         "drop", "withdraw", "units"],
        [
            "For unit registration, please visit the student portal at your institution's website "
            "and log in with your student credentials. Registration closes at the end of Week 2.",
            "Unit registration is done through the academic registrar's office or the student portal. "
            "Ensure you have settled your fees before registering.",
            "To register for BIT4133, go to the student portal → Academic → Unit Registration. "
            "Contact the registrar if you face any issues.",
        ]
    ),

    # ── NLP topics help ────────────────────────────────────────────────────
    (
        ["tokenization", "tokenize", "token"],
        [
            "Tokenization is the process of splitting text into individual words or sentences. "
            "In Python: use nltk.word_tokenize() for words and nltk.sent_tokenize() for sentences.",
        ]
    ),
    (
        ["stemming", "stem"],
        [
            "Stemming reduces words to their root form. Example: 'running' → 'run'. "
            "Use nltk.stem.PorterStemmer() in Python.",
        ]
    ),
    (
        ["lemmatization", "lemmatize", "lemma"],
        [
            "Lemmatization returns the dictionary base form of a word. "
            "Example: 'better' → 'good'. Use nltk.stem.WordNetLemmatizer() in Python.",
        ]
    ),
    (
        ["pos", "pos tag", "part of speech", "tagging"],
        [
            "POS Tagging assigns grammatical roles to words. Example: 'runs' → VBZ (Verb). "
            "Use nltk.pos_tag(tokens) in Python. Common tags: NN (noun), VB (verb), JJ (adjective).",
        ]
    ),
    (
        ["ngram", "n-gram", "bigram", "trigram", "unigram"],
        [
            "N-grams are sequences of N words. Bigrams = 2 words, Trigrams = 3 words. "
            "They are used in language models to predict the next word.",
        ]
    ),
    (
        ["hmm", "hidden markov", "viterbi", "sequence labeling"],
        [
            "HMM (Hidden Markov Model) is a probabilistic model for sequence labeling. "
            "States are hidden (labels), observations are visible (words). "
            "The Viterbi algorithm finds the most likely label sequence.",
        ]
    ),
    (
        ["dependency", "parsing", "parse", "syntax"],
        [
            "Dependency parsing identifies grammatical relationships between words. "
            "In spaCy: use nlp(text) then access token.dep_ and token.head. "
            "Key roles: nsubj (subject), ROOT (main verb), dobj (direct object).",
        ]
    ),
    (
        ["semantic", "similarity", "meaning", "spacy"],
        [
            "Semantic similarity measures how close in meaning two sentences are. "
            "In spaCy: nlp(sentence1).similarity(nlp(sentence2)) returns a score from 0.0 to 1.0.",
        ]
    ),

    # ── Assignment / homework ──────────────────────────────────────────────
    (
        ["assignment", "homework", "task", "practical", "submit", "submission",
         "deadline", "due"],
        [
            "Assignments are submitted through the student portal. Ensure you submit before the deadline. "
            "Week 4 assignment requires: dependency structure screenshots and semantic similarity analysis.",
            "For practical tasks, include: your Python source code, terminal output screenshots, "
            "and a short explanation of what you observed.",
            "Your logbook should document all practical tasks with: code snippets, screenshots, "
            "learning outcomes, and GitHub commit records.",
        ]
    ),

    # ── Online course / CAT 2 ──────────────────────────────────────────────
    (
        ["online course", "cat 2", "certificate", "mooc", "hugging face",
         "deeplearning", "coursera", "free course"],
        [
            "For CAT 2, you must complete ONE free online NLP/AI course. "
            "Recommended: Hugging Face NLP Course (free), DeepLearning.AI NLP Specialization, "
            "or Google AI Learning Resources. Submit your certificate + reflection report.",
            "Start your online course early — they take time to complete. "
            "Focus on courses covering Transformers, LLMs, or NLP pipelines for maximum relevance to BIT4133.",
        ]
    ),

    # ── Python / libraries ─────────────────────────────────────────────────
    (
        ["python", "install", "library", "nltk", "spacy", "import", "error",
         "pip", "package"],
        [
            "To install required libraries, run:\n"
            "  pip install nltk spacy\n"
            "  python -m spacy download en_core_web_sm\n"
            "For NLTK data: import nltk; nltk.download('all')",
            "If you get an import error, ensure your virtual environment is activated "
            "and the library is installed with pip install <library-name>.",
        ]
    ),

    # ── Lecturer / help ────────────────────────────────────────────────────
    (
        ["lecturer", "teacher", "professor", "instructor", "help", "explain",
         "understand", "confused"],
        [
            "Please review the course notes for Weeks 1–5 on the student portal. "
            "You can also visit the lecturer during office hours or post your question "
            "in the class discussion group.",
            "If you need further assistance, consult your Week 1–5 practical notes "
            "or revisit the code examples in your logbook.",
        ]
    ),

    # ── Goodbye ────────────────────────────────────────────────────────────
    (
        ["bye", "goodbye", "exit", "quit", "see you", "later", "done", "close"],
        [
            "Goodbye! Good luck with your CAT 1 preparation. Study hard!",
            "Farewell! Remember to practice your NLP code daily. See you!",
            "Bye! You are doing great — keep building those NLP skills!",
        ]
    ),
]

EXIT_KEYWORDS = {"bye", "goodbye", "exit", "quit", "done", "close"}


# =============================================================================
# RESPONSE ENGINE
# =============================================================================

def find_response(user_input: str) -> str:
    """
    Match user input against patterns and return a response.
    Returns a default message if no pattern matches.
    """
    text = user_input.lower().strip()

    for triggers, responses in RESPONSE_PATTERNS:
        if any(kw in text for kw in triggers):
            return random.choice(responses)

    # Default / fallback response
    return (
        "I do not understand that query yet. Try asking about:\n"
        "  • CAT 1 schedule       • Unit registration\n"
        "  • Tokenization         • Stemming / Lemmatization\n"
        "  • POS Tagging          • N-grams\n"
        "  • HMM / Viterbi        • Dependency parsing\n"
        "  • Semantic similarity  • Online courses (CAT 2)\n"
        "  • Python/NLTK help     • Assignment submission"
    )


def is_exit(user_input: str) -> bool:
    """Check if the user wants to exit."""
    words = set(user_input.lower().split())
    return bool(words & EXIT_KEYWORDS)


# =============================================================================
# CHATBOT INTERACTION LOOP
# =============================================================================

def run_chatbot():
    """Run the interactive chatbot loop."""
    print("\n" + "=" * 60)
    print("  Welcome to the Student Academic Assistant Chatbot")
    print("  BIT4133 — Natural Language Processing")
    print("=" * 60)
    print("""
  I can help you with:
    ► CAT 1 schedule and revision topics
    ► Unit registration guidance
    ► NLP concept explanations (tokenization, POS, HMM, etc.)
    ► Assignment and submission information
    ► Online course recommendations (CAT 2)
    ► Python and library installation help

  Type 'bye' or 'exit' to quit.
""")
    print("-" * 60)

    while True:
        try:
            user_input = input("  You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Bot: Session interrupted. Goodbye!")
            break

        if not user_input:
            print("  Bot: Please type a question or topic you need help with.")
            continue

        response = find_response(user_input)

        # Simulate typing delay for a more natural feel
        time.sleep(0.3)

        # Format bot response (indent all lines)
        formatted = "\n".join(f"         {line}" if i > 0 else f"  Bot: {line}"
                              for i, line in enumerate(response.split("\n")))
        print(formatted)
        print()

        if is_exit(user_input):
            break

    print("-" * 60)
    print("  Chatbot session ended. Good luck with BIT4133!")
    print("=" * 60)
    print()


# =============================================================================
# DEMO MODE (non-interactive for screenshots)
# =============================================================================

def run_demo():
    """Run a preset demonstration of the chatbot (for logbook screenshots)."""
    demo_queries = [
        "Hello",
        "When is CAT 1?",
        "How do I register for units?",
        "Explain tokenization",
        "What is POS tagging?",
        "Tell me about HMM",
        "How do I install spaCy?",
        "I need help with my assignment",
        "What online course should I take for CAT 2?",
        "Goodbye",
    ]

    print("\n" + "=" * 60)
    print("  DEMO MODE — Student Academic Assistant Chatbot")
    print("  BIT4133 NLP — Week 5 Mini Project")
    print("=" * 60)

    for query in demo_queries:
        print(f"\n  You: {query}")
        time.sleep(0.2)
        response = find_response(query)
        formatted = "\n".join(f"         {line}" if i > 0 else f"  Bot: {line}"
                              for i, line in enumerate(response.split("\n")))
        print(formatted)

        if is_exit(query):
            break

    print("\n" + "=" * 60)
    print("  Demo complete. Take screenshots for your logbook.")
    print("=" * 60)
    print()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_chatbot()
