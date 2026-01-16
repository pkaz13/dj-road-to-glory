# Word Embeddings Training with Subword Tokenization

Gemini thread: https://gemini.google.com/share/02412e72714a

This repository contains Python implementations for training and testing word/document embeddings using three complementary architectures:
* **Word2Vec CBOW** - For learning word-level representations from scratch
* **Doc2Vec PV-DM** - For learning sentence/document-level representations from scratch
* **Sentence-BERT (SBERT)** - For leveraging pre-trained transformer models for semantic sentence search

Word2Vec and Doc2Vec implementations are specifically designed to work with subword tokenizers (like BPE), enabling the models to handle complex morphology by aggregating sub-unit vectors. SBERT uses pre-trained multilingual transformer models for state-of-the-art semantic similarity.

## 1. Project Overview
The project provides three separate embedding pipelines with different approaches and use cases:

### Word2Vec CBOW Pipeline
* **`run-train-cbow.py`** - Trains word-level embeddings (predicts target word from context)
* **`run-inference-cbow.py`** - Tests word similarity and analogies

### Doc2Vec PV-DM Pipeline
* **`run-train-doc2vec.py`** - Trains document-level embeddings (learns sentence representations)
* **`run-inference-doc2vec.py`** - Finds similar sentences from the corpus

### Sentence-BERT (SBERT) Pipeline
* **`generate-sbert.py`** - Generates sentence embeddings using pre-trained transformers
* **`search_sbert.py`** - Interactive semantic search system with real-time queries

Word2Vec and Doc2Vec implementations utilize the **Gensim** library, while SBERT uses the **Sentence-Transformers** library with pre-trained multilingual models (e.g., `intfloat/multilingual-e5-small`).

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

### What is Sentence-BERT (SBERT)?
**Sentence-BERT** is a modification of BERT that uses siamese and triplet network structures to derive semantically meaningful sentence embeddings from pre-trained transformer models.
* **Mechanism:** Uses pre-trained multilingual models (like E5) that have been fine-tuned on millions of sentence pairs for semantic similarity.
* **Performance:** State-of-the-art quality for semantic search, significantly better than averaging word embeddings. Much faster inference than BERT's sentence-pair classification.
* **Use Case:** Production-ready semantic search, question answering, clustering, and information retrieval with minimal training required.
* **Trade-off:** Requires more computational resources and larger models compared to Word2Vec/Doc2Vec, but provides superior semantic understanding.



---

## 2. Project Structure

```
embedding/
├── config.py                           # Shared configuration for all models
├── corpora.py                          # Corpus file paths for training
├── utils.py                            # Shared utility functions
├── requirements.txt                    # Python dependencies
│
├── run-train-cbow.py                  # Word2Vec training (Stages 1-3)
├── run-inference-cbow.py              # Word2Vec inference (Stage 4)
│
├── run-train-doc2vec.py               # Doc2Vec training
├── run-inference-doc2vec.py           # Doc2Vec inference
│
├── generate-sbert.py                  # SBERT embeddings generation
├── search_sbert.py                    # SBERT interactive search
│
├── output/                            # Generated model artifacts
│   ├── embedding_tensor_cbow.npy
│   ├── embedding_token_to_index_map.json
│   ├── embedding_word2vec_cbow_model.model
│   ├── embedding_doc2vec_model.model
│   ├── embedding_doc2vec_sentence_map.json
│   ├── sbert_sentence_embeddings.npy
│   └── sbert_sentences_map.json
│
└── logs/                              # Inference results with timestamps
    ├── word2vec_cbow-results-*.log
    └── doc2vec_pvdm-results-*.log
```

### Core Files

#### Configuration & Utilities
* **`config.py`** - Centralized configuration for all three embedding models:
  - Tokenizer and output directory paths
  - `TRAINING_PARAMS` - Word2Vec CBOW hyperparameters
  - `TRAINING_PARAMS_DOC2VEC` - Doc2Vec PV-DM hyperparameters
  - Output file names for Word2Vec, Doc2Vec, and SBERT
  - Model names for logging

* **`corpora.py`** - Defines corpus file paths for training:
  - `CORPORA_DIRS` - Dictionary mapping corpus names to directory paths (NKJP, WOLNELEKTURY)
  - `CORPORA_FILES` - Dictionary with file lists for each corpus (including "ALL" for combined training)
  - Helper function `get_corpus_file()` for selective corpus access

* **`utils.py`** - Shared utility functions:
  - `aggregate_raw_sentences()` - Loads and aggregates text from multiple files, used by training scripts

* **`requirements.txt`** - Python package dependencies:
  - `tokenizers` - For BPE tokenization (Word2Vec/Doc2Vec)
  - `numpy` - For numerical operations and embedding storage
  - `gensim` - For Word2Vec and Doc2Vec implementations
  - `sentence-transformers` - For SBERT pre-trained models
  - `huggingface_hub[cli]` - For downloading pre-trained transformer models

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

### Sentence-BERT (SBERT) Pipeline

#### Generation Script (`generate-sbert.py`)

**Stage 1: Embedding Generation (Lines 28-79)**
* **Configuration:** Uses pre-trained model `intfloat/multilingual-e5-small` from HuggingFace
* **Aggregation:** Uses `aggregate_raw_sentences()` from `utils.py` to load corpus
* **Model Loading:** Downloads and loads pre-trained Sentence-Transformer model
* **Encoding:** Generates dense vector representations for all sentences in one batch
* **Persistence:** Saves two files:
  - **Embeddings Array:** `.npy` file with all sentence vectors (shape: [num_sentences, 384])
  - **Sentence Map:** `.json` file mapping indices to original sentences
* **Smart Caching:** Checks for existing embeddings to avoid redundant computation

#### Search Script (`search_sbert.py`)

**Stage 2: Interactive Semantic Search (Lines 19-96)**
* **Resource Loading:** Loads pre-generated embeddings, sentence map, and model
* **Helper Function:** `search()` encodes query and computes cosine similarity against all corpus vectors
* **Efficient Search:** Uses NumPy vectorized operations for fast similarity computation
* **Interactive Mode:** Provides a REPL (Read-Eval-Print Loop) for real-time queries
* **Performance:** Sub-second search across entire corpus (much faster than Doc2Vec inference)

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

### 4.3 SBERT: Pre-computed Embeddings + Cosine Similarity

The SBERT pipeline uses a two-phase approach: pre-computation and search.

#### Phase 1: Embedding Generation (`generate-sbert.py`)
1. **Corpus Loading:** All sentences are loaded from the corpus files
2. **Batch Encoding:** The pre-trained transformer model encodes all sentences in batches:
   ```python
   embeddings = model.encode(sentences, show_progress_bar=True)
   ```
3. **Storage:** Embeddings are saved as a NumPy array for fast loading

#### Phase 2: Semantic Search (`search_sbert.py`)
1. **Query Encoding:** The user's query is encoded into a vector using the same model
2. **Similarity Computation:** Cosine similarity is calculated between the query vector and all corpus vectors:
   $$\text{similarity}(q, d_i) = \frac{\vec{q} \cdot \vec{d_i}}{||\vec{q}|| \cdot ||\vec{d_i}||}$$
3. **Ranking:** Results are sorted by similarity score in descending order
4. **Return:** Top-k most similar sentences are returned with their scores

**Example:**
```python
results = search("Wielka bitwa wojskowa.", model, corpus_embeddings, sentences, top_k=5)
# Returns 5 most similar sentences with cosine similarity scores
# Typical execution time: < 0.1s for 100k+ sentences
```

**Key Advantages:**
* **Speed:** Pre-computed embeddings enable instant search (no inference needed for corpus)
* **Quality:** Transformer models capture deep semantic meaning beyond word overlap
* **Scalability:** Can be extended with approximate nearest neighbor search (FAISS, Annoy) for millions of documents

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

### Sentence-BERT (SBERT) Workflow

#### Generating Embeddings:
```bash
python generate-sbert.py
```
This will:
1. Load configuration from `config.py` and aggregate sentences using `utils.py`
2. Download pre-trained model `intfloat/multilingual-e5-small` (if not cached)
3. Generate embeddings for all corpus sentences with progress bar
4. Save two files to the `output/` directory:
   - `sbert_sentence_embeddings.npy` - Dense vectors (shape: [num_sentences, 384])
   - `sbert_sentences_map.json` - Index-to-sentence mapping

**Note:** If embeddings already exist, the script will ask before regenerating (useful for saving time).

#### Interactive Search:
```bash
python search_sbert.py
```
This will:
1. Load pre-computed embeddings and sentence map from `output/`
2. Load the pre-trained model for query encoding
3. Start an interactive REPL for real-time semantic search
4. Display top 5 results with similarity scores and execution time

**Example session:**
```
--- SEMANTIC SEARCH SYSTEM (SBERT) ---
Enter a sentence to find similar in the corpus.
Enter 'exit' or 'q' to exit.

Query: Litwo, ojczyzno moja!
Results (time: 0.043s):
  [0.8234] Litwo, ojczyzno moja! ty jesteś jak zdrowie.
  [0.7456] Ojczyzna to najświętsza rzecz dla Polaka.
  [0.7123] Tęsknota za rodzinną ziemią nie opuszczała go nigdy.
  ...
```

#### Using in Your Own Code:
```python
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
from config import (
    OUTPUT_DIR,
    OUTPUT_SBERT_EMBEDDINGS_FILE,
    OUTPUT_SBERT_SENTENCES_MAP_FILE
)

# Load resources
model = SentenceTransformer("intfloat/multilingual-e5-small")
embeddings = np.load(os.path.join(OUTPUT_DIR, OUTPUT_SBERT_EMBEDDINGS_FILE))

with open(os.path.join(OUTPUT_DIR, OUTPUT_SBERT_SENTENCES_MAP_FILE), 'r') as f:
    sentences = json.load(f)

# Perform semantic search
def semantic_search(query, top_k=5):
    # Encode query
    query_embedding = model.encode([query], convert_to_numpy=True)
    
    # Compute similarities
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    
    # Get top results
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        results.append({
            'text': sentences[idx],
            'score': similarities[idx]
        })
    return results

# Example usage
results = semantic_search("Wielka bitwa wojskowa.", top_k=3)
for r in results:
    print(f"[{r['score']:.4f}] {r['text']}")
```

---

## 7. Comparison of Approaches

| Feature | Word2Vec CBOW | Doc2Vec PV-DM | Sentence-BERT |
| :--- | :--- | :--- | :--- |
| **Granularity** | Word-level tokens | Sentence/document | Sentence/document |
| **Training** | From scratch | From scratch | Pre-trained (fine-tuning optional) |
| **Quality** | Good for word similarity | Good for document similarity | State-of-the-art semantic similarity |
| **Speed (Training)** | Fast (~minutes) | Medium (~minutes) | Very fast (no training needed) |
| **Speed (Inference)** | Fast | Slow (requires inference per query) | Very fast (pre-computed embeddings) |
| **Model Size** | Small (~MBs) | Small (~MBs) | Large (~100-500MB) |
| **Memory Usage** | Low | Low | Medium-High |
| **Use Case** | Word analogies, morphology | Document classification, simple search | Production semantic search, clustering |
| **Multilingual** | Depends on corpus | Depends on corpus | Yes (with multilingual models) |
| **OOV Handling** | Via subword tokens | Via subword tokens | Via transformer tokenization |

### When to Use Each:

- **Word2Vec CBOW**: When you need word-level embeddings for specific domain vocabulary, word analogies, or morphological analysis
- **Doc2Vec PV-DM**: When you want to learn document representations from scratch on domain-specific corpus without external dependencies
- **SBERT**: When you need high-quality semantic search in production, have sufficient computational resources, and want multilingual support

---