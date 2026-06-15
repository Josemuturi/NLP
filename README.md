#  Smart Farm — AI Chatbot for Farmers

**Course**: BIT4133 Natural Language Processing  
**Project**: Smart Farm AI Assistant  
**Student**: Joseph Muturi  
**Reg No**: BSCCS/2024/34208

---

## Project Overview

Smart Farm is an AI-powered chatbot that helps farmers diagnose crop problems and receive
solutions by typing or speaking their farming issue. The chatbot applies a full NLP pipeline
covering all concepts taught in Weeks 1–7 of BIT4133.

---

## NLP Concepts Demonstrated

| Week | Concept | Applied In |
|------|---------|------------|
| Week 1 | Tokenization, Stop Words Removal, Stemming, Lemmatization | `week1/nlp_pipeline.py` |
| Week 2 | N-gram Language Models, POS Tagging | `week2/ngram_model.py`, `week2/pos_tagger.py` |
| Week 3 | Hidden Markov Models, Sequence Labeling, Entity Extraction | `week3/hmm_entity.py` |
| Week 4 | Dependency Parsing, Semantic Similarity | `week4/dependency_parser.py` |
| Week 5 | Complete NLP Pipeline, Rule-based Chatbot | `week5/nlp_pipeline_complete.py`, `week5/student_chatbot.py` |
| Week 6 | Word Embeddings (CBOW, Skip-Gram), PCA/t-SNE Visualization | `week6/train_word2vec.py`, `week6/visualize_embeddings.py` |
| Week 7 | Neural Language Models, TensorFlow Next-Word Prediction | `week7/train_neural_lm.py`, `week7/predict_text.py`, `week7/tf_nlp_exercise.py` |

---

## Project Structure

```
smart_farm/
├── requirements.txt         # Python dependencies
├── knowledge_base.py        # Farming problems & solutions dictionary
├── week1/
│   ├── nlp_pipeline.py      # Tokenization, stopwords, stemming, lemmatization
│   └── demo_sentences.py    # 5 farming sentence demonstrations
├── week2/
│   ├── ngram_model.py       # N-gram language model on farming corpus
│   └── pos_tagger.py        # POS tagging and noun/verb extraction
├── week3/
│   ├── hmm_entity.py        # HMM-based entity sequence labeling
│   ├── chatbot.py           # Full CLI chatbot (main entry point)
│   └── speech_input.py      # Speech-to-text input module
├── week4/
│   └── dependency_parser.py # spaCy dependency parsing & semantic similarity
├── week5/
│   ├── nlp_pipeline_complete.py  # Integrated NLP pipeline (all weeks)
│   └── student_chatbot.py   # Student Academic Assistant Chatbot (mini project)
├── week6/
│   ├── train_word2vec.py    # Word2Vec CBOW & Skip-Gram training
│   └── visualize_embeddings.py  # PCA/t-SNE 2D projection plots
└── week7/
    ├── train_neural_lm.py   # TensorFlow neural language model training
    ├── predict_text.py      # CLI next-word predictor
    └── tf_nlp_exercise.py   # Keras tokenization & sequence demo
```

---

## Setup & Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download NLTK data (run once)
python -c "import nltk; nltk.download('all')"

# 3. Run Week 1 demo
python week1/nlp_pipeline.py

# 4. Run Week 2 demo
python week2/ngram_model.py
python week2/pos_tagger.py

# 5. Run Week 4 spaCy demo (requires: pip install spacy && python -m spacy download en_core_web_sm)
python week4/dependency_parser.py

# 6. Run Week 5 complete pipeline and chatbot
python week5/nlp_pipeline_complete.py
python week5/student_chatbot.py --demo

# 7. Launch the full chatbot
python week3/chatbot.py

# 8. Run Week 6 Word2Vec training & visualization
python week6/train_word2vec.py
python week6/visualize_embeddings.py

# 9. Run Week 7 Neural Language Model training & prediction
python week7/train_neural_lm.py
python week7/predict_text.py "the farmer crops"
python week7/tf_nlp_exercise.py
```

---

## Example Interaction

```
 Smart Farm AI Assistant
=====================================
Farmer: My maize leaves are turning yellow

[NLP PIPELINE]
✔ Tokens      : ['My', 'maize', 'leaves', 'are', 'turning', 'yellow']
✔ Filtered    : ['maize', 'leaves', 'turning', 'yellow']
✔ Stems       : ['maiz', 'leav', 'turn', 'yellow']
✔ Lemmas      : ['maize', 'leaf', 'turn', 'yellow']
✔ POS Tags    : [('maize', 'NN'), ('leaves', 'NNS'), ('turning', 'VBG'), ('yellow', 'JJ')]
✔ Entities    : crop=maize | symptom=yellow leaves

 Solution:
   Yellow leaves in maize are often caused by nitrogen deficiency or maize streak virus.
   Apply urea fertilizer at 46% N rate. If viral, remove infected plants.
```

---

## GitHub Commits

| Commit | Week | Description |
|--------|------|--------------|
| Commit 1 | Week 1 | Environment setup, NLTK basics, knowledge base |
| Commit 2 | Week 2 | N-gram model, POS tagging, noun/verb extraction, farming role classifier |
| Commit 3 | Week 3 | HMM entity labeling, full chatbot, speech input |
| Commit 4 | Week 4 | spaCy dependency parsing, semantic similarity, assignments |
| Commit 5 | Week 5 | Complete NLP pipeline, student chatbot mini project, logbook (Weeks 1-5) |
| Commit 6 | Week 6 | Word2Vec CBOW & Skip-Gram training, PCA/t-SNE embedding visualization |
| Commit 7 | Week 7 | TensorFlow neural language model, next-word prediction, tokenization exercise |

---

## License
For academic purposes — BIT4133 NLP Course Project.
