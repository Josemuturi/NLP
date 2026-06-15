"""
week7/tf_nlp_exercise.py
===========================================================
BIT4133 – Natural Language Processing
Week 7: Neural Language Models and Deep Learning for NLP

TensorFlow NLP Exercise:
1. Accepts user text or uses default demo texts.
2. Tokenizes the text using Keras preprocessing.
3. Displays the vocabulary word indices.
4. Converts the text to sequence arrays.

Run: python week7/tf_nlp_exercise.py
"""

from tensorflow.keras.preprocessing.text import Tokenizer

def run_exercise():
    # Demo text corpus
    texts = [
        "I love NLP",
        "NLP is interesting",
        "Deep learning powers neural language models"
    ]
    
    print("=== Original Text Corpus ===")
    for t in texts:
        print(f" - {t}")

    # 1. Initialize Tokenizer
    tokenizer = Tokenizer(oov_token="<OOV>")
    
    # 2. Fit Tokenizer on text corpus
    tokenizer.fit_on_texts(texts)
    
    # 3. Display Word Indices
    print("\n=== Word Index (Vocabulary Mapping) ===")
    for word, index in tokenizer.word_index.items():
        print(f"  Word: '{word:<12}' -> Index: {index}")

    # 4. Convert text into numeric sequences
    sequences = tokenizer.texts_to_sequences(texts)
    print("\n=== Text Converted to Sequences ===")
    for original, seq in zip(texts, sequences):
        print(f"  Text    : \"{original}\"")
        print(f"  Sequence: {seq}\n")

if __name__ == "__main__":
    run_exercise()
