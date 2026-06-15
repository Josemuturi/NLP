"""
week6/visualize_embeddings.py
===========================================================
BIT4133 – Natural Language Processing
Week 6: Word Embeddings and Distributed Representations

Loads the trained Word2Vec model, applies PCA and t-SNE to project words
into 2D space, and plots them using Matplotlib.

Run: python week6/visualize_embeddings.py
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def main():
    model_path = "week6/week6_cbow.model"
    if not os.path.exists(model_path):
        print(f"Error: Model not found at '{model_path}'. Run train_word2vec.py first.")
        return

    # 1. Load the model
    model = Word2Vec.load(model_path)
    wv = model.wv

    # 2. Select words to visualize (must be in vocabulary)
    words = [
        "maize", "crops", "fertilizer", "soil", "leaves", "yellow", 
        "farmer", "water", "irrigation", "pests", "pesticides",
        "healthy", "diseases", "seeds", "weeds", "wheat", "urea",
        "student", "teacher", "school", "learning", "compost"
    ]
    
    # Filter words to only include those in the vocabulary
    words = [w for w in words if w in wv]
    print(f"Visualizing {len(words)} words in vocabulary.")

    # 3. Retrieve vectors
    word_vectors = np.array([wv[w] for w in words])

    # 4. Apply PCA (Principal Component Analysis)
    pca = PCA(n_components=2)
    coords_pca = pca.fit_transform(word_vectors)

    # 5. Apply t-SNE (t-Distributed Stochastic Neighbor Embedding)
    # Perplexity must be less than the number of samples
    tsne = TSNE(n_components=2, perplexity=min(5, len(words) - 1), random_state=42)
    coords_tsne = tsne.fit_transform(word_vectors)

    # Make sure target directory exists
    os.makedirs("week6", exist_ok=True)

    # 6. Plot PCA
    plt.figure(figsize=(10, 8), dpi=150)
    plt.style.use("seaborn-v0_8-dark" if "seaborn-v0_8-dark" in plt.style.available else "default")
    
    plt.scatter(coords_pca[:, 0], coords_pca[:, 1], color='#3b82f6', edgecolors='#1e3a8a', s=100, alpha=0.8)
    for i, word in enumerate(words):
        plt.annotate(word, xy=(coords_pca[i, 0], coords_pca[i, 1]), xytext=(5, 2),
                     textcoords='offset points', fontsize=11, fontweight='bold', color='#1f2937')
    
    plt.title("2D Projection of Farming Word Embeddings (PCA)", fontsize=14, fontweight='bold', pad=15)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    pca_img_path = "week6/embeddings_pca.png"
    plt.savefig(pca_img_path)
    plt.close()
    print(f"Saved PCA visualization to '{pca_img_path}'")

    # 7. Plot t-SNE
    plt.figure(figsize=(10, 8), dpi=150)
    plt.scatter(coords_tsne[:, 0], coords_tsne[:, 1], color='#10b981', edgecolors='#065f46', s=100, alpha=0.8)
    for i, word in enumerate(words):
        plt.annotate(word, xy=(coords_tsne[i, 0], coords_tsne[i, 1]), xytext=(5, 2),
                     textcoords='offset points', fontsize=11, fontweight='bold', color='#1f2937')
    
    plt.title("2D Projection of Farming Word Embeddings (t-SNE)", fontsize=14, fontweight='bold', pad=15)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    tsne_img_path = "week6/embeddings_tsne.png"
    plt.savefig(tsne_img_path)
    plt.close()
    print(f"Saved t-SNE visualization to '{tsne_img_path}'")

if __name__ == "__main__":
    main()
