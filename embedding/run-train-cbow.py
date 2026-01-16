import numpy as np
import json
import logging
from gensim.models import Word2Vec
from tokenizers import Tokenizer
import os
import glob
import shutil
from corpora import CORPORA_FILES
from config import TOKENIZER_FILE, OUTPUT_DIR, OUTPUT_TENSOR_FILE, OUTPUT_MAP_FILE, OUTPUT_MODEL_FILE, TRAINING_PARAMS
from utils import aggregate_raw_sentences

# Setting up logging for gensim
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Phase 1: Tokenizing sentences - preparing data for training

# Config of paths and parameters
files = CORPORA_FILES["ALL"]

# Delete and recreate output directory
if os.path.exists(OUTPUT_DIR):
    print(f"Removing existing output directory: {OUTPUT_DIR}")
    shutil.rmtree(OUTPUT_DIR)

os.makedirs(OUTPUT_DIR)
print(f"Created output directory: {OUTPUT_DIR}")

# Output files with full paths
OUTPUT_TENSOR_FILE = os.path.join(OUTPUT_DIR, OUTPUT_TENSOR_FILE)
OUTPUT_MAP_FILE = os.path.join(OUTPUT_DIR, OUTPUT_MAP_FILE)
OUTPUT_MODEL_FILE = os.path.join(OUTPUT_DIR, OUTPUT_MODEL_FILE)

# Extract training parameters
VECTOR_LENGTH = TRAINING_PARAMS["VECTOR_LENGTH"]
WINDOW_SIZE = TRAINING_PARAMS["WINDOW_SIZE"]
MIN_COUNT = TRAINING_PARAMS["MIN_COUNT"]
WORKERS = TRAINING_PARAMS["WORKERS"]
EPOCHS = TRAINING_PARAMS["EPOCHS"]
SAMPLE_RATE = TRAINING_PARAMS["SAMPLE_RATE"]
SG_MODE = TRAINING_PARAMS["SG_MODE"]

try:
    print(f"Loading tokenizer from file: {TOKENIZER_FILE}")
    tokenizer = Tokenizer.from_file(TOKENIZER_FILE)
except FileNotFoundError:
    print(f"ERROR: File '{TOKENIZER_FILE}' not found. Please make sure the file exists.")
    raise

raw_sentences = aggregate_raw_sentences(files)

# Tokenizing all sentences using BPE tokenizer
print(f"Tokenizing {len(raw_sentences)} sentences...")
encodings = tokenizer.encode_batch(raw_sentences)

# Conversion of Encoding objects to list of list of strings (tokens)
tokenized_sentences = [
    encoding.tokens for encoding in encodings
]
print(f"Prepared {len(tokenized_sentences)} sequences for training.")


# Phase 2: Training Word2Vec (CBOW) model
print("\n--- Starting Word2Vec (CBOW) training ---")
model = Word2Vec(
    sentences=tokenized_sentences,
    vector_size=VECTOR_LENGTH,
    window=WINDOW_SIZE,
    min_count=MIN_COUNT,
    workers=WORKERS,
    sg=SG_MODE,  # 0: CBOW
    epochs=EPOCHS,
    sample=SAMPLE_RATE,
)
print("Training completed successfully.")

# Phase 3: Exporting and saving results

# Exporting embedding tensor
embedding_matrix_np = model.wv.vectors
embedding_matrix_tensor = np.array(embedding_matrix_np, dtype=np.float32)

print(f"\nShape of final tensor: {embedding_matrix_tensor.shape} (Tokens x Dimensions)")

# 1. Saving NumPy tensor (.npy)
np.save(OUTPUT_TENSOR_FILE, embedding_matrix_tensor)
print(f"Embedding tensor saved as: '{OUTPUT_TENSOR_FILE}'.")

# 2. Saving mapping of tokens to indices
token_to_index = {token: model.wv.get_index(token) for token in model.wv.index_to_key}
with open(OUTPUT_MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(token_to_index, f, ensure_ascii=False, indent=4)
print(f"Mapping of tokens to indices saved as: '{OUTPUT_MAP_FILE}'.")

# 3. Saving the entire gensim model (optional, but recommended)
model.save(OUTPUT_MODEL_FILE)
print(f"Full Word2Vec model saved as: '{OUTPUT_MODEL_FILE}'.")