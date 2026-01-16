import numpy as np
import json
import logging
import time
import os
from sentence_transformers import SentenceTransformer
from corpora import CORPORA_FILES
from utils import aggregate_raw_sentences
from config import (
    OUTPUT_DIR,
    OUTPUT_SBERT_EMBEDDINGS_FILE,
    OUTPUT_SBERT_SENTENCES_MAP_FILE,
)

# --- CONFIGURATION ---
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

MODEL_NAME = "intfloat/multilingual-e5-small"
files = CORPORA_FILES["ALL"]

# Output files
OUTPUT_EMBEDDINGS_FILE = os.path.join(OUTPUT_DIR, OUTPUT_SBERT_EMBEDDINGS_FILE)
OUTPUT_SENTENCES_MAP = os.path.join(OUTPUT_DIR, OUTPUT_SBERT_SENTENCES_MAP_FILE)


def main():
    # 1. Loading text data
    try:
        raw_sentences = aggregate_raw_sentences(files)
        print(f"Collected {len(raw_sentences)} sentences.")
    except Exception as e:
        print(f"ERROR: {e}")
        return

    # 2. Loading model
    print(f"Loading Sentence-Transformer model: {MODEL_NAME}...")
    try:
        model = SentenceTransformer(MODEL_NAME)
    except Exception as e:
        print(f"ERROR: {e}")
        return

    # 3. Generating or loading vectors
    # Check if the file already exists, to avoid re-generating without need
    if os.path.exists(OUTPUT_EMBEDDINGS_FILE):
        print(f"Found existing vector file: {OUTPUT_EMBEDDINGS_FILE}")
        choice = input("Do you want to generate vectors again? (t/n): ")
        if choice.lower() != "t":
            print("Skipping generation.")
            # If we are not generating from scratch, let's make sure we save the sentence map.
            # (Note: this is risky if the text files have changed but the vectors have not!)
            # To be on the safe side, we overwrite the sentence map in this script.
            with open(OUTPUT_SENTENCES_MAP, "w", encoding="utf-8") as f:
                json.dump(raw_sentences, f, ensure_ascii=False, indent=4)
            print("Updated sentences map.")
            return

    print("Generating new embeddings...")
    start_time = time.time()

    embeddings = model.encode(
        raw_sentences, show_progress_bar=True, convert_to_numpy=True
    )

    end_time = time.time()
    print(f"Completed in {end_time - start_time:.2f}s. Shape: {embeddings.shape}")

    # 4. Saving results
    print("Saving files...")
    np.save(OUTPUT_EMBEDDINGS_FILE, embeddings)

    with open(OUTPUT_SENTENCES_MAP, "w", encoding="utf-8") as f:
        json.dump(raw_sentences, f, ensure_ascii=False, indent=4)

    print(
        f"Done! Files created:\n - {OUTPUT_EMBEDDINGS_FILE}\n - {OUTPUT_SENTENCES_MAP}"
    )


if __name__ == "__main__":
    main()
