import json
import logging
import time
import os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from tokenizers import Tokenizer
from corpora import CORPORA_FILES
from config import (
    TOKENIZER_FILE,
    OUTPUT_DIR,
    OUTPUT_DOC2VEC_MODEL_FILE,
    OUTPUT_DOC2VEC_SENTENCE_MAP_FILE,
    TRAINING_PARAMS_DOC2VEC,
)
from utils import aggregate_raw_sentences

# Setting up logging for gensim
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

# Data selection
files = CORPORA_FILES["ALL"]

OUTPUT_MODEL_FILE = os.path.join(OUTPUT_DIR, OUTPUT_DOC2VEC_MODEL_FILE)
OUTPUT_SENTENCE_MAP = os.path.join(OUTPUT_DIR, OUTPUT_DOC2VEC_SENTENCE_MAP_FILE)

# 1. Loading data
print(f"Loading tokenizer: {TOKENIZER_FILE}")
tokenizer = Tokenizer.from_file(TOKENIZER_FILE)

raw_sentences = aggregate_raw_sentences(files)

if not raw_sentences:
    raise ValueError("Error: Empty corpus data.")

print(f"Collected {len(raw_sentences)} sentences. Starting tokenization...")

# 2. Preparing tagged documents
# In Doc2Vec each sentence must have a unique identifier (tag).
# Here we use the list index as ID (e.g. "0", "1", "2"...).
tagged_data = [
    TaggedDocument(words=tokenizer.encode(sentence).tokens, tags=[str(i)])
    for i, sentence in enumerate(raw_sentences)
]

# 3. Training
print(
    f"Start training Doc2Vec (Epochs={TRAINING_PARAMS_DOC2VEC["EPOCHS"]}, Vector={TRAINING_PARAMS_DOC2VEC["VECTOR_LENGTH"]})..."
)
start_time = time.time()

model = Doc2Vec(
    tagged_data,
    vector_size=TRAINING_PARAMS_DOC2VEC["VECTOR_LENGTH"],
    window=TRAINING_PARAMS_DOC2VEC["WINDOW_SIZE"],
    min_count=TRAINING_PARAMS_DOC2VEC["MIN_COUNT"],
    workers=TRAINING_PARAMS_DOC2VEC["WORKERS"],
    epochs=TRAINING_PARAMS_DOC2VEC["EPOCHS"],
    dm=TRAINING_PARAMS_DOC2VEC["DM_MODE"],
)

end_time = time.time()
print(f"Training completed in {end_time - start_time:.2f}s.")

# 4. Saving results
model.save(OUTPUT_MODEL_FILE)
print(f"Model saved as: {OUTPUT_MODEL_FILE}")

# Saving sentence map (necessary to read inference results!)
with open(OUTPUT_SENTENCE_MAP, "w", encoding="utf-8") as f:
    json.dump(raw_sentences, f, ensure_ascii=False, indent=4)
print(f"Sentence map saved as: {OUTPUT_SENTENCE_MAP}")
