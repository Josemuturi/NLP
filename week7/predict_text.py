"""
week7/predict_text.py
===========================================================
BIT4133 – Natural Language Processing
Week 7: Neural Language Models and Deep Learning for NLP

CLI script to load the trained neural language model and predict the next word
for a given 3-word sentence fragment.

Run: python week7/predict_text.py "the farmer crops"
"""

import sys
import json
import numpy as np
import tensorflow as tf

def predict_next_word(model, word_index, index_word, text_fragment, top_n=3):
    # Preprocess text input
    tokens = text_fragment.lower().split()
    
    # Pad or truncate to the context length of 3
    if len(tokens) > 3:
        tokens = tokens[-3:]
    elif len(tokens) < 3:
        # Pad with OOV token '<unk>' at the beginning
        tokens = ['<unk>'] * (3 - len(tokens)) + tokens

    # Convert tokens to indices
    seq = [word_index.get(t, word_index['<unk>']) for t in tokens]
    seq_arr = np.array([seq])
    
    # Predict probabilities
    preds = model.predict(seq_arr, verbose=0)[0]
    
    # Sort predictions by confidence in descending order
    top_indices = np.argsort(preds)[::-1][:top_n]
    
    print(f"\nContext Input: \"{text_fragment}\" -> Transformed to index sequence: {seq}")
    print("Predicted Next Words:")
    results = []
    for idx in top_indices:
        word = index_word.get(str(idx), "<unknown>")
        prob = preds[idx]
        print(f"  - '{word:<15}' : Confidence {prob * 100:.2f}%")
        results.append((word, float(prob)))
    return results

def main():
    model_path = "week7/neural_lm.keras"
    vocab_path = "week7/tokenizer_word_index.json"

    # Validate model and vocabulary existence
    if not os.path.exists(model_path) or not os.path.exists(vocab_path):
        print("Error: Model or word_index not found. Run 'train_neural_lm.py' first.")
        sys.exit(1)

    # Load resources
    model = tf.keras.models.load_model(model_path)
    with open(vocab_path, "r") as f:
        word_index = json.load(f)
    
    # Reverse index mapping
    index_word = {str(idx): word for word, idx in word_index.items()}

    # Check argument input
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = "the farmer crops" # Default

    predict_next_word(model, word_index, index_word, user_input)

if __name__ == "__main__":
    import os
    main()
