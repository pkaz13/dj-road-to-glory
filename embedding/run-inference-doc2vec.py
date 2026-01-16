import json
import logging
import os
from datetime import datetime
from gensim.models.doc2vec import Doc2Vec
from tokenizers import Tokenizer
from config import (
    TOKENIZER_FILE,
    OUTPUT_DIR,
    OUTPUT_DOC2VEC_MODEL_FILE,
    OUTPUT_DOC2VEC_SENTENCE_MAP_FILE,
    TRAINING_PARAMS_DOC2VEC,
    MODEL_NAME_DOC2VEC,
)


# 1. Loading resources
print(f"Loading model: {OUTPUT_DOC2VEC_MODEL_FILE}")
MODEL_FILE = os.path.join(OUTPUT_DIR, OUTPUT_DOC2VEC_MODEL_FILE)
SENTENCE_MAP_FILE = os.path.join(OUTPUT_DIR, OUTPUT_DOC2VEC_SENTENCE_MAP_FILE)

try:
    model = Doc2Vec.load(MODEL_FILE)
    tokenizer = Tokenizer.from_file(TOKENIZER_FILE)
    with open(SENTENCE_MAP_FILE, 'r', encoding='utf-8') as f:
        sentence_lookup = json.load(f)

    print("All resources loaded successfully.")

except FileNotFoundError as e:
    print(f"ERROR: Missing required file: {e}")
    exit(1)

# 2. Setting up logging
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print(f"Created logs directory: {LOGS_DIR}")

# Create log file with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"{MODEL_NAME_DOC2VEC}-results-{timestamp}.log"
log_filepath = os.path.join(LOGS_DIR, log_filename)

print("\n--- Starting Doc2Vec inference ---")
print(f"Results will be logged to: {log_filepath}")

# --- 2. Inference function ---
def find_similar_sentences(text_query, top_n=5):
    """
    1. Tokenize the query.
    2. Generate a vector for it (infer_vector).
    3. Find the most similar documents in the model's memory.
    4. Translate document IDs to text using sentence_lookup.
    """
    # Tokenization
    tokens = tokenizer.encode(text_query).tokens
    
    # Inference vector (freezing model weights, fitting new document vector)
    # Using the same number of epochs as during training for stability
    inferred_vector = model.infer_vector(tokens, epochs=model.epochs)
    
    # Finding similar documents
    # model.dv is a shortcut for model.docvecs (in newer gensim versions)
    sims = model.dv.most_similar([inferred_vector], topn=top_n)
    
    results = []
    for doc_id, similarity in sims:
        try:
            doc_index = int(doc_id) # Tag is a string "5", convert to int 5
            sentence_content = sentence_lookup[doc_index]
            results.append((sentence_content, similarity))
        except (ValueError, IndexError):
            results.append(("[Error index/map]", similarity))
            
    return results

# 3. Main testing with logging
test_sentences = [
    "Jestem bardzo głodny.",
    "Litwo, ojczyzno moja!",
    "Wielka bitwa wojskowa.",
]

# Open log file for writing
with open(log_filepath, 'w', encoding='utf-8') as log_file:
    # Write header and configuration
    log_file.write("=" * 80 + "\n")
    log_file.write("Doc2Vec PV-DM Model Inference Results\n")
    log_file.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write("=" * 80 + "\n\n")

    # Write model and tokenizer info
    log_file.write("MODEL INFORMATION:\n")
    log_file.write("-" * 80 + "\n")
    log_file.write(f"Model file: {MODEL_FILE}\n")
    log_file.write(f"Tokenizer file: {TOKENIZER_FILE}\n")
    log_file.write(f"Sentence map file: {SENTENCE_MAP_FILE}\n")
    log_file.write("\n")

    # Write training parameters
    log_file.write("TRAINING PARAMETERS:\n")
    log_file.write("-" * 80 + "\n")
    for param, value in TRAINING_PARAMS_DOC2VEC.items():
        log_file.write(f"{param}: {value}\n")
    log_file.write("\n")

    # Write test results
    log_file.write("TEST RESULTS:\n")
    log_file.write("-" * 80 + "\n\n")

    print("\n" + "="*50)
    print("=== START INFERENCE ===")
    print("="*50)

    for text in test_sentences:
        print(f"\nQuery: \"{text}\"")
        log_file.write(f"Query: \"{text}\"\n")

        similar = find_similar_sentences(text, top_n=3)

        print("Most similar sentences from the corpus:")
        log_file.write("Most similar sentences from the corpus:\n")

        for content, score in similar:
            result_line = f"  [{score:.4f}] {content}"
            print(result_line)
            log_file.write(result_line + "\n")

        log_file.write("\n")
        print()

    log_file.write("=" * 80 + "\n")
    log_file.write("End of results\n")

print(f"\nResults saved to: {log_filepath}")

# Optional: Interactive mode
# while True:
#     query = input("\nEnter a sentence (or 'q' to exit): ")
#     if query == 'q': break
#     ...