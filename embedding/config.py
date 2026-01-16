# Shared configuration for Word2Vec CBOW training and inference

# Paths
TOKENIZER_FILE = "../tokenizer/tokenizers/all-60k-tokenizer.json"
OUTPUT_DIR = "output"

# Output files
OUTPUT_TENSOR_FILE = "embedding_tensor_cbow.npy"
OUTPUT_MAP_FILE = "embedding_token_to_index_map.json"
OUTPUT_MODEL_FILE = "embedding_word2vec_cbow_model.model"
OUTPUT_DOC2VEC_MODEL_FILE = "embedding_doc2vec_model.model"
OUTPUT_DOC2VEC_SENTENCE_MAP_FILE = "embedding_doc2vec_sentence_map.json"
OUTPUT_SBERT_EMBEDDINGS_FILE = "sbert_sentence_embeddings.npy"
OUTPUT_SBERT_SENTENCES_MAP_FILE = "sbert_sentences_map.json"

# Training parameters for Word2Vec (CBOW model)
TRAINING_PARAMS = {
    "VECTOR_LENGTH": 100,
    "WINDOW_SIZE": 5,
    "MIN_COUNT": 2,
    "WORKERS": 4,
    "EPOCHS": 20,
    "SAMPLE_RATE": 1e-2,
    "SG_MODE": 0,  # 0 dla CBOW, 1 dla Skip-gram
}

# Training parameters for Doc2Vec (PV-DM model)
TRAINING_PARAMS_DOC2VEC = {
    "VECTOR_LENGTH": 100,
    "WINDOW_SIZE": 5,
    "MIN_COUNT": 4,
    "WORKERS": 4,
    "EPOCHS": 10,
    "DM_MODE": 1,  # 1 = PV-DM (Distributed Memory)
}

# Model name (used for logging)
MODEL_NAME = "word2vec_cbow"
MODEL_NAME_DOC2VEC = "doc2vec_pvdm"
