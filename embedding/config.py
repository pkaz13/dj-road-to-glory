# Shared configuration for Word2Vec CBOW training and inference

# Paths
TOKENIZER_FILE = "../tokenizer/tokenizers/all-60k-tokenizer.json"
OUTPUT_DIR = "output"

# Output files
OUTPUT_TENSOR_FILE = "embedding_tensor_cbow.npy"
OUTPUT_MAP_FILE = "embedding_token_to_index_map.json"
OUTPUT_MODEL_FILE = "embedding_word2vec_cbow_model.model"

# Training parameters for Word2Vec (CBOW model)
TRAINING_PARAMS = {
    "VECTOR_LENGTH": 100,
    "WINDOW_SIZE": 5,
    "MIN_COUNT": 2,
    "WORKERS": 4,
    "EPOCHS": 20,
    "SAMPLE_RATE": 1e-2,
    "SG_MODE": 0  # 0 dla CBOW, 1 dla Skip-gram
}

# Model name (used for logging)
MODEL_NAME = "word2vec_cbow"
