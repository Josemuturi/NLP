"""
week2/pos_tagger.py - Smart Farm POS Tagger (Week 2)
=====================================================
Demonstrates:
  - Part-of-Speech (POS) tagging using NLTK's averaged perceptron tagger
  - Extracting nouns (crop names, plant parts) from farmer queries
  - Extracting verbs (farmer actions/problems) from farmer queries
  - Chunking to identify noun phrases (NP)
  - Applying POS analysis to understand the farmer's question

Course: BIT4133 Natural Language Processing - Week 2
Project: Smart Farm AI Assistant
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "week1"))

import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag, RegexpParser

for pkg in ["punkt", "averaged_perceptron_tagger", "maxent_ne_chunker",
            "words", "punkt_tab", "averaged_perceptron_tagger_eng"]:
    nltk.download(pkg, quiet=True)

from knowledge_base import CROP_VOCAB, SYMPTOM_VOCAB, ACTION_VOCAB, LOCATION_VOCAB


# =============================================================================
# POS TAG REFERENCE TABLE
# =============================================================================

POS_DESCRIPTIONS = {
    "CC":  "Coordinating conjunction",
    "CD":  "Cardinal digit",
    "DT":  "Determiner",
    "EX":  "Existential there",
    "FW":  "Foreign word",
    "IN":  "Preposition / subordinating conjunction",
    "JJ":  "Adjective",
    "JJR": "Adjective, comparative",
    "JJS": "Adjective, superlative",
    "LS":  "List item marker",
    "MD":  "Modal verb",
    "NN":  "Noun, singular or mass",
    "NNS": "Noun, plural",
    "NNP": "Proper noun, singular",
    "NNPS":"Proper noun, plural",
    "PDT": "Predeterminer",
    "POS": "Possessive ending",
    "PRP": "Personal pronoun",
    "PRP$":"Possessive pronoun",
    "RB":  "Adverb",
    "RBR": "Adverb, comparative",
    "RBS": "Adverb, superlative",
    "RP":  "Particle",
    "TO":  "to",
    "UH":  "Interjection",
    "VB":  "Verb, base form",
    "VBD": "Verb, past tense",
    "VBG": "Verb, gerund/present participle",
    "VBN": "Verb, past participle",
    "VBP": "Verb, non-3rd person singular present",
    "VBZ": "Verb, 3rd person singular present",
    "WDT": "Wh-determiner",
    "WP":  "Wh-pronoun",
    "WP$": "Possessive wh-pronoun",
    "WRB": "Wh-adverb",
}

# Penn Treebank tag groups
NOUN_TAGS    = {"NN", "NNS", "NNP", "NNPS"}
VERB_TAGS    = {"VB", "VBD", "VBG", "VBN", "VBP", "VBZ"}
ADJ_TAGS     = {"JJ", "JJR", "JJS"}
ADV_TAGS     = {"RB", "RBR", "RBS"}


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def tag_sentence(text: str) -> list:
    """
    POS-tag a sentence.

    Args:
        text: Input sentence string

    Returns:
        List of (word, POS_tag) tuples
    """
    tokens = word_tokenize(text)
    return pos_tag(tokens)


def extract_nouns(tagged: list) -> list:
    """Extract all nouns (NN, NNS, NNP, NNPS) from POS-tagged tokens."""
    return [(word, tag) for word, tag in tagged if tag in NOUN_TAGS]


def extract_verbs(tagged: list) -> list:
    """Extract all verb forms from POS-tagged tokens."""
    return [(word, tag) for word, tag in tagged if tag in VERB_TAGS]


def extract_adjectives(tagged: list) -> list:
    """Extract all adjective forms from POS-tagged tokens."""
    return [(word, tag) for word, tag in tagged if tag in ADJ_TAGS]


def extract_noun_phrases(tagged: list) -> list:
    """
    Extract noun phrases using a simple regex grammar.

    Grammar: NP -> optional DT/JJ* followed by one or more NN*
    """
    grammar = r"""
        NP: {<DT>?<JJ.*>*<NN.*>+}
    """
    parser  = RegexpParser(grammar)
    tree    = parser.parse(tagged)
    phrases = []
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            phrase = " ".join(word for word, tag in subtree.leaves())
            phrases.append(phrase)
    return phrases


def identify_farming_roles(tagged: list) -> dict:
    """
    Classify tokens from a farmer's query into farming roles:
      - crops     : words matching the crop vocabulary
      - symptoms  : words matching the symptom vocabulary
      - actions   : words matching the action vocabulary
      - locations : words matching the location vocabulary (plant parts)
      - other_nouns: remaining nouns

    Args:
        tagged: List of (word, POS_tag) tuples

    Returns:
        dict with role -> list of matching words
    """
    roles = {
        "crops":       [],
        "symptoms":    [],
        "actions":     [],
        "locations":   [],
        "other_nouns": [],
    }

    for word, tag in tagged:
        word_lower = word.lower()

        if word_lower in CROP_VOCAB:
            roles["crops"].append(word_lower)
        elif word_lower in SYMPTOM_VOCAB and tag in ADJ_TAGS | {"RB"}:
            roles["symptoms"].append(word_lower)
        elif word_lower in SYMPTOM_VOCAB:
            roles["symptoms"].append(word_lower)
        elif word_lower in ACTION_VOCAB and tag in VERB_TAGS:
            roles["actions"].append(word_lower)
        elif word_lower in LOCATION_VOCAB and tag in NOUN_TAGS:
            roles["locations"].append(word_lower)
        elif tag in NOUN_TAGS and len(word_lower) > 2:
            roles["other_nouns"].append(word_lower)

    # De-duplicate while preserving order
    for key in roles:
        seen = set()
        roles[key] = [x for x in roles[key] if not (x in seen or seen.add(x))]

    return roles


def analyse_farmer_query(text: str, verbose: bool = True) -> dict:
    """
    Full POS-analysis of a farmer's query.

    Returns a dict with all POS analysis results.
    """
    tagged       = tag_sentence(text)
    nouns        = extract_nouns(tagged)
    verbs        = extract_verbs(tagged)
    adjectives   = extract_adjectives(tagged)
    np_chunks    = extract_noun_phrases(tagged)
    farming_roles = identify_farming_roles(tagged)

    result = {
        "original":      text,
        "tagged":        tagged,
        "nouns":         nouns,
        "verbs":         verbs,
        "adjectives":    adjectives,
        "noun_phrases":  np_chunks,
        "farming_roles": farming_roles,
    }

    if verbose:
        _print_pos_result(result)

    return result


def _print_pos_result(result: dict):
    """Pretty-print the POS tagging analysis."""
    sep = "-" * 65
    print(sep)
    print(f"  QUERY      : {result['original']}")
    print(sep)

    print("\n  Full POS Tags:")
    row_fmt = "    {:<20} {:<10} {}"
    print(row_fmt.format("WORD", "TAG", "DESCRIPTION"))
    print("    " + "-" * 55)
    for word, tag in result["tagged"]:
        desc = POS_DESCRIPTIONS.get(tag, "-")
        print(row_fmt.format(word, tag, desc))

    print(f"\n  Nouns      : {[w for w, _ in result['nouns']]}")
    print(f"  Verbs      : {[w for w, _ in result['verbs']]}")
    print(f"  Adjectives : {[w for w, _ in result['adjectives']]}")
    print(f"  NP Chunks  : {result['noun_phrases']}")

    roles = result["farming_roles"]
    print("\n  Farming Role Classification:")
    print(f"    Crops      : {roles['crops']}")
    print(f"    Symptoms   : {roles['symptoms']}")
    print(f"    Actions    : {roles['actions']}")
    print(f"    Locations  : {roles['locations']}")
    print(f"    Other nouns: {roles['other_nouns']}")
    print()


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print()
    print("=" * 65)
    print("   SMART FARM - Week 2: POS Tagging & Query Analysis")
    print("   Course: BIT4133 Natural Language Processing")
    print("=" * 65)

    queries = [
        "My maize leaves are turning yellow and the plants look stunted.",
        "I need to spray fungicide on my tomato plants because they have blight.",
        "The potato field has brown spots on the leaves and they are spreading fast.",
        "When should I irrigate my wheat crop during the dry season?",
        "My bean plants are dying due to rust infection on the leaves.",
    ]

    print(f"\nAnalysing {len(queries)} farmer queries with POS tagging...\n")

    for i, query in enumerate(queries, start=1):
        print(f"\n[Query {i}]")
        analyse_farmer_query(query, verbose=True)

    # -- Tag distribution summary ------------------------------------------
    print("=" * 65)
    print("  POS TAG DISTRIBUTION across all queries")
    print("=" * 65)
    from collections import Counter
    tag_counter = Counter()
    for q in queries:
        for word, tag in tag_sentence(q):
            tag_counter[tag] += 1

    print()
    print(f"  {'TAG':<8} {'COUNT':<8} {'DESCRIPTION'}")
    print(f"  {'-'*6}   {'-'*5}   {'-'*35}")
    for tag, count in tag_counter.most_common():
        desc = POS_DESCRIPTIONS.get(tag, "-")
        print(f"  {tag:<8} {count:<8} {desc}")

    print()
    print("✅ Week 2 POS tagging demonstration complete.")
    print()
