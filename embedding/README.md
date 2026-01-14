# Word2Vec CBOW Training with Subword Tokenization

Gemini thread: https://gemini.google.com/share/02412e72714a

This repository contains a Python implementation for training and testing word embeddings using the **Word2Vec Continuous Bag of Words (CBOW)** architecture. The implementation is specifically designed to work with subword tokenizers (like BPE), enabling the model to handle complex morphology by aggregating sub-unit vectors.

## 1. Project Overview
The project is split into two main scripts that handle the complete pipeline from raw text processing to vector space verification:
* **`run-train-cbow.py`** - Handles data preparation, model training, and saving
* **`run-inference-cbow.py`** - Loads the trained model and performs inference/testing

The implementation utilizes the **Gensim** library, a robust framework for unsupervised topic modeling and natural language processing.

### What is CBOW?
The **Continuous Bag of Words (CBOW)** model predicts a target word based on the context of its surrounding words. 
* **Mechanism:** It takes the average of the vectors of the context words to predict the middle word.
* **Performance:** CBOW is generally faster to train and shows better performance for frequent words compared to the Skip-gram architecture.



---

## 2. Project Structure

```
embedding/
├── config.py                    # Configuration file with paths and hyperparameters
├── corpora.py                   # Defines corpus file paths for training
├── requirements.txt             # Python dependencies
├── run-train-cbow.py           # Training pipeline (Stages 1-3)
├── run-inference-cbow.py       # Inference pipeline (Stage 4)
├── output/                     # Generated model artifacts
│   ├── embedding_tensor_cbow.npy
│   ├── embedding_token_to_index_map.json
│   └── embedding_word2vec_cbow_model.model
└── logs/                       # Inference results with timestamps
    └── word2vec_cbow-results-*.log
```

### Configuration Files
* **`config.py`** - Centralized configuration for tokenizer paths, output directories, model names, and all training hyperparameters
* **`corpora.py`** - Defines the corpus files to be used for training (referenced by `CORPORA_FILES` dictionary)
* **`requirements.txt`** - Python package dependencies (numpy, gensim, tokenizers)

---

## 3. Pipeline Stages

The pipeline is organized into four distinct stages split across two scripts:

### Training Script (`run-train-cbow.py`)

#### Stage 1: Preparation & Tokenization (Lines 15-78)
* **Configuration:** Loads hyperparameters from `config.py` and corpus paths from `corpora.py`
* **Aggregation:** Collects raw text from multiple files defined in the `CORPORA_FILES` dictionary
* **Tokenization:** Uses a pre-trained BPE tokenizer to split sentences into subword tokens rather than whole words

#### Stage 2: Training (Lines 81-93)
This is the core learning phase where the Word2Vec model is initialized. The model iterates through the tokenized sentences for a set number of epochs to learn the mathematical relationships between tokens.

#### Stage 3: Export & Persistence (Lines 95-115)
To ensure the model can be used without retraining, the script exports:
* **Embedding Tensor:** A `.npy` file containing the raw numerical weights
* **Token Map:** A `.json` file linking string tokens to their specific indices in the tensor
* **Gensim Model:** A `.model` file that preserves the full state of the trained model

### Inference Script (`run-inference-cbow.py`)

#### Stage 4: Inference & Verification (Lines 18-155)
This stage tests the quality of the embeddings. It includes:
* **Model Loading:** Loads the saved Gensim model and tokenizer
* **Helper Function:** `get_word_vector_and_similar()` handles "whole word" queries by reconstructing word meanings from their constituent subword parts
* **Testing:** Runs inference on test words and logs results with timestamps
* **Vector Analogies:** Performs mathematical pattern verification using vector combinations

---

## 4. The Subword Aggregation Logic

The function `get_word_vector_and_similar` is critical because the model does not store vectors for whole words, but for fragments. 

1. **Tokenization:** The input word is split into its subword tokens (e.g., "wojsko" $\rightarrow$ `['woj', 'sko']`).
2. **Retrieval:** The script retrieves individual vectors for each fragment from the model's vocabulary.
3. **Averaging:** It calculates the mean vector of these fragments:
   $$\vec{v}_{word} = \frac{1}{n} \sum_{i=1}^{n} \vec{v}_{token_i}$$
4. **Similarity:** The model then performs a cosine similarity search to find the nearest neighbors to this "averaged" point in the vector space.

---

## 5. Hyperparameter Reference

| Parameter | Value | Impact on Training |
| :--- | :--- | :--- |
| `VECTOR_LENGTH` | 20 | The number of dimensions. Smaller values are better for small datasets but lack nuance. |
| `WINDOW_SIZE` | 6 | The context range. Larger windows capture thematic links; smaller windows capture syntax. |
| `MIN_COUNT` | 2 | Minimum frequency filter. Higher values remove noise but may delete valid rare words. |
| `EPOCHS` | 20 | Number of passes over the data. Higher values improve "memorization" of patterns. |
| `SAMPLE_RATE` | 1e-2 | Threshold for random omitting very common words, such as "i", "w", "na". Usually between 0.001 do 0.00001. |
| `WORKERS` | 4 | Number of processors used for training |
| `SG_MODE` | 0 | Training algorithm: `0` for CBOW, `1` for Skip-gram. |

---

## 6. Usage Guide: Training vs. Inference

The project is already split into two separate workflows for training and inference:

### To Train:
```bash
python run-train-cbow.py
```
This will:
1. Load configuration from `config.py` and corpus paths from `corpora.py`
2. Tokenize all sentences using the BPE tokenizer
3. Train the Word2Vec CBOW model
4. Save three files to the `output/` directory:
   - `embedding_tensor_cbow.npy` - Raw embedding weights
   - `embedding_token_to_index_map.json` - Token-to-index mapping
   - `embedding_word2vec_cbow_model.model` - Complete Gensim model

### To Test (Inference Only):
```bash
python run-inference-cbow.py
```
This will:
1. Load the trained model from the `output/` directory
2. Run inference on predefined test words
3. Generate a timestamped log file in `logs/` with detailed results

### To Use in Your Own Code:
```python
from gensim.models import Word2Vec
from tokenizers import Tokenizer
import os
from config import TOKENIZER_FILE, OUTPUT_DIR, OUTPUT_MODEL_FILE

# Load the saved components
model = Word2Vec.load(os.path.join(OUTPUT_DIR, OUTPUT_MODEL_FILE))
tokenizer = Tokenizer.from_file(TOKENIZER_FILE)

# Use the get_word_vector_and_similar function from run-inference-cbow.py