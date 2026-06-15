"""
week6/train_word2vec.py
===========================================================
BIT4133 – Natural Language Processing
Week 6: Word Embeddings and Distributed Representations

Trains a custom Word2Vec model (both CBOW and Skip-Gram) on a farming corpus,
displays word vectors, computes similarities, and performs analogy tasks.

Run: python week6/train_word2vec.py
"""

import os
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import word_tokenize

# Download tokenizer data if not present
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

# 1. Define a farming-focused corpus
corpus = [
    "The farmer crops maize and wheat in the fertile soil.",
    "Maize leaves turn yellow when there is nitrogen deficiency in the soil.",
    "The farmer applies urea fertilizer to correct nutrient deficiency in crops.",
    "Apply chemical pesticides or organic neem oil to control insect pests.",
    "Yellow leaves can be caused by maize streak virus or water logging.",
    "Irrigation supplies water to crops in dry sandy soil during drought.",
    "Insects like aphids and stem borers damage maize stalks and leaves.",
    "Weeds compete with crops for nutrients in the soil.",
    "A healthy crop has green leaves and strong roots.",
    "Crop rotation improves soil health and reduces pest infestations.",
    "Organic farming avoids chemical fertilizers and uses compost.",
    "The farmer sprays pesticide on infected crops to control diseases.",
    "Drip irrigation is efficient for watering plants in clay soil.",
    "Nitrogen deficiency is a common nutrient problem for maize crops.",
    "Dry soil lacks water and requires immediate irrigation.",
    "Good quality seeds produce healthy crops and higher yields.",
    "Farming requires fertile soil, clean water, and proper nutrients.",
    "The crop is infected with a fungal disease causing spot symptoms.",
    "A student learns farming techniques and crop science at school.",
    "The teacher explains soil composition and nutrient absorption to students."
]

# 2. Preprocess sentences (tokenization, lowercasing, filtering non-alpha)
tokenized_sentences = []
for sentence in corpus:
    tokens = word_tokenize(sentence.lower())
    filtered_tokens = [t for t in tokens if t.isalpha()]
    tokenized_sentences.append(filtered_tokens)

print("=== Preprocessed Corpus Preview ===")
for i, sent in enumerate(tokenized_sentences[:3], 1):
    print(f"Sentence {i}: {sent}")
print(f"Total Sentences: {len(tokenized_sentences)}")

# Create output folder if not exists
os.makedirs("week6", exist_ok=True)

# 3. Train Continuous Bag of Words (CBOW) Model
# Parameters: vector_size=50 (dense representation), window=2, min_count=1 (include all words)
print("\n=== Training CBOW Model (sg=0) ===")
model_cbow = Word2Vec(
    sentences=tokenized_sentences,
    vector_size=50,
    window=3,
    min_count=1,
    sg=0,
    epochs=100,
    seed=42
)
model_cbow.save("week6/week6_cbow.model")
print("CBOW Model trained and saved to 'week6/week6_cbow.model'")

# 4. Train Skip-Gram (SG) Model
print("\n=== Training Skip-Gram Model (sg=1) ===")
model_sg = Word2Vec(
    sentences=tokenized_sentences,
    vector_size=50,
    window=3,
    min_count=1,
    sg=1,
    epochs=100,
    seed=42
)
model_sg.save("week6/week6_sg.model")
print("Skip-Gram Model trained and saved to 'week6/week6_sg.model'")

# 5. Display word vector representation
word_to_inspect = "maize"
print(f"\n=== Word Vector Representation for '{word_to_inspect}' (CBOW) ===")
vector = model_cbow.wv[word_to_inspect]
print(f"Shape: {vector.shape}")
print(f"Vector values:\n{vector}")

# 6. Analyze Semantic Relationships & Similarity (Comparing CBOW and Skip-Gram)
test_words = ["maize", "soil", "fertilizer", "pest"]

print("\n=== Semantic Similarity Analysis ===")
for word in test_words:
    if word in model_cbow.wv:
        print(f"\nMost similar to '{word}':")
        print(f"  [CBOW] : {model_cbow.wv.most_similar(word, topn=3)}")
        print(f"  [Skip-Gram]: {model_sg.wv.most_similar(word, topn=3)}")

# 7. Word similarity scores
word_pair = ("maize", "crops")
sim_cbow = model_cbow.wv.similarity(word_pair[0], word_pair[1])
sim_sg = model_sg.wv.similarity(word_pair[0], word_pair[1])
print(f"\nSimilarity between {word_pair[0]} and {word_pair[1]}:")
print(f"  CBOW Score     : {sim_cbow:.4f}")
print(f"  Skip-Gram Score: {sim_sg:.4f}")

# 8. Analogy Reasoning
# Analogy: "farmer" is to "crops" as "teacher" is to what?
# Mathematically: crops - farmer + teacher = ?
# gensim: positive=['crops', 'teacher'], negative=['farmer']
print("\n=== Analogy Tasks ===")
try:
    analogy_result = model_cbow.wv.most_similar(positive=['crops', 'teacher'], negative=['farmer'], topn=1)
    print(f"Analogy: 'crops' - 'farmer' + 'teacher' = {analogy_result[0][0]} (score: {analogy_result[0][1]:.4f})")
except Exception as e:
    print(f"Analogy error: {e}")
