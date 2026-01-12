# Tokenizer Project

A project for building and managing custom tokenizers trained on various corpora using Byte-Pair Encoding (BPE).

## Project Structure

### Data Folder (`data/`)
Contains corpus datasets used for training tokenizers. Currently includes:
- `nkjp/` - NKJP (National Corpus of Polish) dataset with 3,889 text files containing Polish language data

### Tokenizers Folder (`tokenizers/`)
Stores trained tokenizer models in JSON format:
- `nkjp-tokenizer.json` - BPE tokenizer trained on the NKJP corpus

### Core Files

#### `builder-tokenizer.py`
Main script for training custom BPE tokenizers. Features include:
- Byte-level pre-tokenization for handling Unicode characters
- Configurable vocabulary size (default: 32,000 tokens)
- Special tokens support: `[UNK]`, `[CLS]`, `[SEP]`, `[PAD]`, `[MASK]`
- Memory-efficient training on large corpora
- Automatic output to the `tokenizers/` directory

#### `corpora.py`
Utility module for loading and managing corpus data:
- Defines available corpora directories and file collections
- Provides `get_corpus_file()` function for pattern-based file selection
- Supports glob patterns for flexible corpus file filtering
- Currently configured for NKJP corpus data

## Usage

1. Ensure corpus data is available in the `data/` folder
2. Configure tokenizer parameters in `builder-tokenizer.py`
3. Run `python builder-tokenizer.py` to train a new tokenizer
4. Trained tokenizers are automatically saved to `tokenizers/` folder

## Dependencies

See `requirements.txt` for required Python packages.