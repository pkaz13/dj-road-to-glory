# Tokenizer Project

A project for building and managing custom tokenizers trained on various Polish language corpora using Byte-Pair Encoding (BPE).

## Gemini thread
https://gemini.google.com/share/c688827e6d56

## Project Structure

### Data Folder (`data/`)
Contains corpus datasets used for training and testing tokenizers:
- `nkjp/` - NKJP (National Corpus of Polish) with ~3,889 text files
- `wolnelektury/` - Wolne Lektury corpus (Polish literature, including Pan Tadeusz)
- `mini/` - Small test files for tokenizer evaluation (e.g., Wikipedia articles, Gutenberg texts)

### Tokenizers Folder (`tokenizers/`)
Stores trained tokenizer models in JSON format. Includes:
- Pre-trained models (Bielik v1/v2/v3, DeepSeek)
- Custom-trained tokenizers with varying vocabulary sizes (16k, 32k, 60k, 80k) for each corpus

### Logs Folder (`logs/`)
Generated during tokenizer evaluation. Contains:
- Individual test results for each text sample
- Summary of most effective tokenizers across all test cases

### Core Files

#### `builder-tokenizer.py`
Trains BPE tokenizers on selected corpora with multiple vocabulary sizes. Iterates through corpus combinations (NKJP, WOLNELEKTURY, PAN_TADEUSZ, ALL) and vocab sizes (16k, 32k, 60k, 80k), generating tokenizers for each combination. Uses ByteLevel pre-tokenization and saves models to `tokenizers/`.

#### `corpora.py`
Corpus management utility that maps corpus names to data directories and file collections. Defines NKJP, WOLNELEKTURY, PAN_TADEUSZ (subset of Wolne Lektury), and ALL (combined corpora without duplicates). Provides `get_corpus_file()` for pattern-based file retrieval.

#### `run-tokenize-text.py`
Evaluates and compares tokenizer efficiency on test texts. Loads all available tokenizers, encodes predefined test texts (Pan Tadeusz excerpt, English texts), counts tokens for each tokenizer, and generates comparative logs showing which tokenizer produces the most compact encoding for each text.

## Usage

### Training Tokenizers
```bash
python builder-tokenizer.py
```
Trains multiple tokenizers across all corpus combinations and vocabulary sizes.

### Evaluating Tokenizers
```bash
python run-tokenize-text.py
```
Compares all tokenizers on test texts and generates detailed efficiency reports in `logs/`.

### Managing Corpora
```bash
python corpora.py
```
Displays available corpora and file counts.

## Dependencies

See `requirements.txt` for required Python packages.