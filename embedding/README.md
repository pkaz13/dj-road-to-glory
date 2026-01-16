# Word Embeddings Training with Subword Tokenization

Gemini thread: https://gemini.google.com/share/02412e72714a

This repository contains Python implementations for training and testing word/document embeddings using two complementary architectures:
* **Word2Vec CBOW** - For learning word-level representations
* **Doc2Vec PV-DM** - For learning sentence/document-level representations

Both implementations are specifically designed to work with subword tokenizers (like BPE), enabling the models to handle complex morphology by aggregating sub-unit vectors.

## 1. Project Overview
The project provides two separate embedding pipelines, each split into training and inference scripts:

### Word2Vec CBOW Pipeline
* **`run-train-cbow.py`** - Trains word-level embeddings (predicts target word from context)
* **`run-inference-cbow.py`** - Tests word similarity and analogies

### Doc2Vec PV-DM Pipeline
* **`run-train-doc2vec.py`** - Trains document-level embeddings (learns sentence representations)
* **`run-inference-doc2vec.py`** - Finds similar sentences from the corpus

Both implementations utilize the **Gensim** library, a robust framework for unsupervised topic modeling and natural language processing.

### What is Word2Vec CBOW?
The **Continuous Bag of Words (CBOW)** model predicts a target word based on the context of its surrounding words. 
* **Mechanism:** It takes the average of the vectors of the context words to predict the middle word.
* **Performance:** CBOW is generally faster to train and shows better performance for frequent words compared to the Skip-gram architecture.
* **Use Case:** Learn semantic relationships between words (e.g., "król" is similar to "monarcha")

### What is Doc2Vec PV-DM?
The **Paragraph Vector - Distributed Memory (PV-DM)** model learns fixed-length feature representations for variable-length pieces of text (sentences, paragraphs, documents).
* **Mechanism:** It predicts words in a document given both the word context and a unique document vector.
* **Performance:** PV-DM acts like a memory that remembers what is missing from the current context, capturing the topic/theme of the document.
* **Use Case:** Find semantically similar sentences or documents, useful for search and recommendation systems.



---

## 2. Project Structure

```
embedding/
├── config.py                           # Shared configuration for both models
├── corpora.py                          # Corpus file paths for training
├── utils.py                            # Shared utility functions
├── requirements.txt                    # Python dependencies
│
├── run-train-cbow.py                  # Word2Vec training (Stages 1-3)
├── run-inference-cbow.py              # Word2Vec inference (Stage 4)
├── run-train-doc2vec.py               # Doc2Vec training
├── run-inference-doc2vec.py           # Doc2Vec inference
│
├── output/                            # Generated model artifacts
│   ├── embedding_tensor_cbow.npy
│   ├── embedding_token_to_index_map.json
│   ├── embedding_word2vec_cbow_model.model
│   ├── embedding_doc2vec_model.model
│   └── embedding_doc2vec_sentence_map.json
│
└── logs/                              # Inference results with timestamps
    ├── word2vec_cbow-results-*.log
    └── doc2vec_pvdm-results-*.log
```

### Core Files

#### Configuration & Utilities
* **`config.py`** - Centralized configuration for both Word2Vec and Doc2Vec models:
  - Tokenizer and output directory paths
  - `TRAINING_PARAMS` - Word2Vec CBOW hyperparameters
  - `TRAINING_PARAMS_DOC2VEC` - Doc2Vec PV-DM hyperparameters
  - Model names and output file names

* **`corpora.py`** - Defines corpus file paths for training:
  - `CORPORA_DIRS` - Dictionary mapping corpus names to directory paths (NKJP, WOLNELEKTURY)
  - `CORPORA_FILES` - Dictionary with file lists for each corpus (including "ALL" for combined training)
  - Helper function `get_corpus_file()` for selective corpus access

* **`utils.py`** - Shared utility functions:
  - `aggregate_raw_sentences()` - Loads and aggregates text from multiple files, used by both training scripts

* **`requirements.txt`** - Python package dependencies (numpy, gensim, tokenizers)

---

## 3. Pipeline Stages

Both Word2Vec and Doc2Vec follow similar training and inference workflows:

### Word2Vec CBOW Pipeline

#### Training Script (`run-train-cbow.py`)

**Stage 1: Preparation & Tokenization (Lines 15-78)**
* **Configuration:** Loads hyperparameters from `config.py` and corpus paths from `corpora.py`
* **Aggregation:** Collects raw text using `aggregate_raw_sentences()` from `utils.py`
* **Tokenization:** Uses a pre-trained BPE tokenizer to split sentences into subword tokens

**Stage 2: Training (Lines 81-93)**
* The Word2Vec model is initialized and trained on tokenized sentences
* Learns vector representations for each subword token based on context windows
* Model iterates for a set number of epochs to learn mathematical relationships

**Stage 3: Export & Persistence (Lines 95-115)**
* **Embedding Tensor:** `.npy` file containing raw numerical weights
* **Token Map:** `.json` file linking string tokens to their indices
* **Gensim Model:** `.model` file preserving the full trained state

#### Inference Script (`run-inference-cbow.py`)

**Stage 4: Inference & Verification (Lines 18-155)**
* **Model Loading:** Loads saved Gensim model and tokenizer
* **Helper Function:** `get_word_vector_and_similar()` reconstructs word vectors by averaging constituent subword vectors
* **Testing:** Runs inference on test words, finds most similar tokens
* **Vector Analogies:** Performs mathematical pattern verification using token combinations
* **Logging:** Results saved to timestamped log files

---

### Doc2Vec PV-DM Pipeline

#### Training Script (`run-train-doc2vec.py`)

**Stage 1: Preparation & Tagged Documents (Lines 22-45)**
* **Configuration:** Loads hyperparameters from `config.py`
* **Aggregation:** Uses `aggregate_raw_sentences()` from `utils.py` to load corpus
* **Tagging:** Each sentence gets a unique ID (its index) and is tokenized into a `TaggedDocument`

**Stage 2: Training (Lines 47-64)**
* Doc2Vec model learns both word vectors and document vectors simultaneously
* Each document vector captures the semantic content of the entire sentence
* Model trains for specified epochs to optimize representations

**Stage 3: Export & Persistence (Lines 66-73)**
* **Doc2Vec Model:** `.model` file containing both word and document vectors
* **Sentence Map:** `.json` file mapping document IDs back to original sentences (critical for inference!)

#### Inference Script (`run-inference-doc2vec.py`)

**Stage 4: Inference & Similarity Search (Lines 17-136)**
* **Model Loading:** Loads Doc2Vec model, tokenizer, and sentence map
* **Helper Function:** `find_similar_sentences()` infers a vector for new text and finds similar documents
* **Testing:** Runs inference on test sentences, returns most similar corpus sentences with similarity scores
* **Logging:** Results saved to timestamped log files with detailed similarity rankings

---

## 4. Key Algorithms

### 4.1 Word2Vec: Subword Aggregation Logic

The function `get_word_vector_and_similar()` in `run-inference-cbow.py` is critical because the model does not store vectors for whole words, but for subword fragments.

1. **Tokenization:** The input word is split into its subword tokens (e.g., "wojsko" $\rightarrow$ `['woj', 'sko']`)
2. **Retrieval:** The script retrieves individual vectors for each fragment from the model's vocabulary
3. **Averaging:** It calculates the mean vector of these fragments:
   $$\vec{v}_{word} = \frac{1}{n} \sum_{i=1}^{n} \vec{v}_{token_i}$$
4. **Similarity:** The model performs a cosine similarity search to find the nearest neighbors to this "averaged" point in the vector space

**Example:**
```python
word_vector, similar = get_word_vector_and_similar("wojsko", tokenizer, model)
# Returns vector for "wojsko" and top similar tokens like "armia", "żołnierz", etc.
```

### 4.2 Doc2Vec: Document Vector Inference

The function `find_similar_sentences()` in `run-inference-doc2vec.py` performs semantic search over the entire corpus.

1. **Tokenization:** The input sentence is tokenized into subword tokens
2. **Inference:** The model generates a document vector for the new text using `infer_vector()`:
   - Freezes the model's word vectors (no retraining)
   - Learns a new document vector that best predicts the words in the query
   - Uses the same number of epochs as during training for stability
3. **Similarity Search:** Performs cosine similarity against all document vectors in the model's memory
4. **Mapping:** Translates document IDs back to original sentences using the sentence map

**Example:**
```python
results = find_similar_sentences("Wielka bitwa wojskowa.", top_n=5)
# Returns 5 most similar sentences from the training corpus
```

---

## 5. Hyperparameter Reference

### Word2Vec CBOW Parameters (`TRAINING_PARAMS` in `config.py`)

| Parameter | Default Value | Impact on Training |
| :--- | :--- | :--- |
| `VECTOR_LENGTH` | 100 | The number of dimensions. Smaller values are better for small datasets but lack nuance. |
| `WINDOW_SIZE` | 5 | The context range. Larger windows capture thematic links; smaller windows capture syntax. |
| `MIN_COUNT` | 2 | Minimum frequency filter. Higher values remove noise but may delete valid rare words. |
| `EPOCHS` | 20 | Number of passes over the data. Higher values improve "memorization" of patterns. |
| `SAMPLE_RATE` | 1e-2 | Threshold for randomly omitting very common words, such as "i", "w", "na". Usually between 0.001 to 0.00001. |
| `WORKERS` | 4 | Number of processors used for parallel training. |
| `SG_MODE` | 0 | Training algorithm: `0` for CBOW, `1` for Skip-gram. |

### Doc2Vec PV-DM Parameters (`TRAINING_PARAMS_DOC2VEC` in `config.py`)

| Parameter | Default Value | Impact on Training |
| :--- | :--- | :--- |
| `VECTOR_LENGTH` | 100 | The number of dimensions for document vectors. Should match word vector size. |
| `WINDOW_SIZE` | 5 | The context range. Similar to Word2Vec but applied to document context. |
| `MIN_COUNT` | 4 | Minimum word frequency. Higher values focus on common words, reducing noise. |
| `WORKERS` | 4 | Number of processors used for parallel training. |
| `EPOCHS` | 10 | Number of training iterations. Doc2Vec often needs fewer epochs than Word2Vec. |
| `DM_MODE` | 1 | Training algorithm: `1` for PV-DM (Distributed Memory), `0` for PV-DBOW (Distributed Bag of Words). |

---

## 6. Usage Guide

The project provides two separate embedding workflows:

### Word2Vec CBOW Workflow

#### Training:
```bash
python run-train-cbow.py
```
This will:
1. Load configuration from `config.py` and corpus paths from `corpora.py`
2. Aggregate and tokenize all sentences using the BPE tokenizer
3. Train the Word2Vec CBOW model
4. Save three files to the `output/` directory:
   - `embedding_tensor_cbow.npy` - Raw embedding weights
   - `embedding_token_to_index_map.json` - Token-to-index mapping
   - `embedding_word2vec_cbow_model.model` - Complete Gensim model

#### Inference:
```bash
python run-inference-cbow.py
```
This will:
1. Load the trained model from the `output/` directory
2. Run inference on predefined test words (e.g., "wojsko", "szlachta", "król")
3. Generate a timestamped log file in `logs/word2vec_cbow-results-*.log`

#### Using in Your Own Code:
```python
from gensim.models import Word2Vec
from tokenizers import Tokenizer
import numpy as np
import os
from config import TOKENIZER_FILE, OUTPUT_DIR, OUTPUT_MODEL_FILE

# Load the saved components
model = Word2Vec.load(os.path.join(OUTPUT_DIR, OUTPUT_MODEL_FILE))
tokenizer = Tokenizer.from_file(TOKENIZER_FILE)

# Get word vector by averaging subword vectors
def get_word_vector(word, tokenizer, model):
    tokens = tokenizer.encode(word).tokens
    vectors = [model.wv[t] for t in tokens if t in model.wv]
    return np.mean(vectors, axis=0) if vectors else None

# Find similar words
word_vector = get_word_vector("wojsko", tokenizer, model)
similar = model.wv.most_similar(positive=[word_vector], topn=5)
```

---

### Doc2Vec PV-DM Workflow

#### Training:
```bash
python run-train-doc2vec.py
```
This will:
1. Load configuration from `config.py` and aggregate sentences using `utils.py`
2. Create tagged documents with unique IDs for each sentence
3. Train the Doc2Vec PV-DM model
4. Save two files to the `output/` directory:
   - `embedding_doc2vec_model.model` - Complete Doc2Vec model
   - `embedding_doc2vec_sentence_map.json` - Mapping of IDs to original sentences

#### Inference:
```bash
python run-inference-doc2vec.py
```
This will:
1. Load the trained model and sentence map from `output/`
2. Run inference on predefined test sentences
3. Generate a timestamped log file in `logs/doc2vec_pvdm-results-*.log`

#### Using in Your Own Code:
```python
import json
from gensim.models.doc2vec import Doc2Vec
from tokenizers import Tokenizer
import os
from config import (
    TOKENIZER_FILE, 
    OUTPUT_DIR, 
    OUTPUT_DOC2VEC_MODEL_FILE,
    OUTPUT_DOC2VEC_SENTENCE_MAP_FILE
)

# Load the saved components
model = Doc2Vec.load(os.path.join(OUTPUT_DIR, OUTPUT_DOC2VEC_MODEL_FILE))
tokenizer = Tokenizer.from_file(TOKENIZER_FILE)

with open(os.path.join(OUTPUT_DIR, OUTPUT_DOC2VEC_SENTENCE_MAP_FILE), 'r') as f:
    sentence_map = json.load(f)

# Find similar sentences
def find_similar(query_text, top_n=5):
    tokens = tokenizer.encode(query_text).tokens
    vector = model.infer_vector(tokens, epochs=model.epochs)
    similar_docs = model.dv.most_similar([vector], topn=top_n)
    
    results = []
    for doc_id, similarity in similar_docs:
        sentence = sentence_map[int(doc_id)]
        results.append((sentence, similarity))
    return results

# Example usage
similar = find_similar("Litwo, ojczyzno moja!", top_n=3)
for sentence, score in similar:
    print(f"[{score:.4f}] {sentence}")
```

---