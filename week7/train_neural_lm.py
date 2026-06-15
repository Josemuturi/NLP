"""
week7/train_neural_lm.py
===========================================================
BIT4133 – Natural Language Processing
Week 7: Neural Language Models and Deep Learning for NLP

Trains a feed-forward Neural Language Model in TensorFlow/Keras to
predict the next word given a 3-word farming context.

Run: python week7/train_neural_lm.py
"""

import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Flatten, Dense
from tensorflow.keras.preprocessing.text import Tokenizer

# 1. Define farming-focused corpus (same as Week 6 for consolidation)
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

# 2. Tokenize and clean text
# Lowercase, clean, and fit Tokenizer
tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', oov_token='<unk>')
tokenizer.fit_on_texts(corpus)
vocab_size = len(tokenizer.word_index) + 1
print(f"Vocabulary Size: {vocab_size} (including OOV token)")

# Save the tokenizer mappings as JSON
os.makedirs("week7", exist_ok=True)
with open("week7/tokenizer_word_index.json", "w") as f:
    json.dump(tokenizer.word_index, f, indent=4)
print("Saved word_index mapping to 'week7/tokenizer_word_index.json'")

# 3. Create training sequences using 3-word sliding context window
# Format: [word_1, word_2, word_3] -> predict [word_4]
input_sequences = []
context_length = 3

for sentence in corpus:
    # Convert sentence to numerical sequence
    sequence = tokenizer.texts_to_sequences([sentence])[0]
    
    # Generate sub-sequences
    for i in range(context_length, len(sequence)):
        sub_seq = sequence[i - context_length : i + 1]
        input_sequences.append(sub_seq)

input_sequences = np.array(input_sequences)
print(f"Total training sequences generated: {len(input_sequences)}")

# Split into inputs (X) and target outputs (y)
X = input_sequences[:, :-1]
y = input_sequences[:, -1]

# 4. Define Neural Language Model architecture
model = Sequential([
    # Input layer: Embedding layer representing words in dense 16-D space
    Embedding(input_dim=vocab_size, output_dim=16, input_shape=(context_length,)),
    # Flatten the 3x16 matrix into a 48-element vector
    Flatten(),
    # Hidden Layer 1 with ReLU activation
    Dense(32, activation='relu'),
    # Hidden Layer 2 with ReLU activation (optional depth)
    Dense(16, activation='relu'),
    # Output Layer: Softmax outputs probabilities over all words in vocabulary
    Dense(vocab_size, activation='softmax')
])

# 5. Compile the model
# Using sparse_categorical_crossentropy so we don't have to one-hot encode targets
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# 6. Train the model
print("\n=== Training Neural Language Model ===")
history = model.fit(
    X, y,
    epochs=180,
    batch_size=8,
    verbose=1
)

# 7. Save trained model
# Using Keras modern native format (.keras)
model_path = "week7/neural_lm.keras"
model.save(model_path)
print(f"\nModel successfully trained and saved to '{model_path}'")
