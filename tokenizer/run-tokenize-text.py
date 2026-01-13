from tokenizers import Tokenizer
from corpora import get_corpus_file
import os
import shutil
from pathlib import Path

TOKENIZERS = {
    # Bielik models
    "bielik-v1": "tokenizers/bielik-v1-tokenizer.json",
    "bielik-v2": "tokenizers/bielik-v2-tokenizer.json",
    "bielik-v3": "tokenizers/bielik-v3-tokenizer.json",

    # DeepSeek model
    "deepseek-11m-7b": "tokenizers/deepseek-11m-7b-tokenizer.json",

    # NKJP corpus tokenizers
    "nkjp-16k": "tokenizers/nkjp-16k-tokenizer.json",
    "nkjp-32k": "tokenizers/nkjp-32k-tokenizer.json",
    "nkjp-60k": "tokenizers/nkjp-60k-tokenizer.json",
    "nkjp-80k": "tokenizers/nkjp-80k-tokenizer.json",

    # Wolnelektury corpus tokenizers
    "wolnelektury-16k": "tokenizers/wolnelektury-16k-tokenizer.json",
    "wolnelektury-32k": "tokenizers/wolnelektury-32k-tokenizer.json",
    "wolnelektury-60k": "tokenizers/wolnelektury-60k-tokenizer.json",
    "wolnelektury-80k": "tokenizers/wolnelektury-80k-tokenizer.json",

    # Pan Tadeusz corpus tokenizers
    "pan_tadeusz-16k": "tokenizers/pan_tadeusz-16k-tokenizer.json",
    "pan_tadeusz-32k": "tokenizers/pan_tadeusz-32k-tokenizer.json",
    "pan_tadeusz-60k": "tokenizers/pan_tadeusz-60k-tokenizer.json",
    "pan_tadeusz-80k": "tokenizers/pan_tadeusz-80k-tokenizer.json",

    # All corpora combined tokenizers
    "all-16k": "tokenizers/all-16k-tokenizer.json",
    "all-32k": "tokenizers/all-32k-tokenizer.json",
    "all-60k": "tokenizers/all-60k-tokenizer.json",
    "all-80k": "tokenizers/all-80k-tokenizer.json",
}

TEST_TEXTS = {
    "pan-tadeusz-ksiega-1": "data/wolnelektury/pan-tadeusz-ksiega-1.txt",
    "the-pickwick-papers-gutenberg": "data/mini/the-pickwick-papers-gutenberg.txt",
    "fryderyk-chopin-wikipedia": "data/mini/fryderyk-chopin-wikipedia.txt",
}


def encode_and_count_tokens(tokenizer_path: str, text: str) -> int:
    """
    Load tokenizer from file, encode the given text and return the number of tokens.
    
    Args:
        tokenizer_path: Path to the tokenizer JSON file
        text: Text to encode
        
    Returns:
        Number of tokens in the encoded text
    """
    tokenizer = Tokenizer.from_file(tokenizer_path)
    encoding = tokenizer.encode(text)
    return len(encoding.ids)


def load_text_file(file_path: str) -> str:
    """Load text from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def print_table(results: dict, text_name: str):
    """Print results in a table format."""
    print(f"\n{'='*60}")
    print(f"Results for: {text_name}")
    print(f"{'='*60}")
    print(f"{'Tokenizer':<25} | {'Token Count':>15}")
    print(f"{'-'*25}-+-{'-'*15}")
    
    for tokenizer_name, token_count in results.items():
        print(f"{tokenizer_name:<25} | {token_count:>15,}")
    
    print(f"{'='*60}")


def save_to_log(results: dict, text_name: str, log_path: str):
    """Save results to log file."""
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"Tokenization results for: {text_name}\n")
        f.write(f"{'='*60}\n\n")
        
        for tokenizer_name, token_count in results.items():
            f.write(f"{tokenizer_name}: {token_count:,} tokens\n")
        
        f.write(f"\n{'='*60}\n")


def find_most_effective(results: dict) -> tuple:
    """Find the tokenizer with the smallest number of tokens."""
    min_tokenizer = min(results.items(), key=lambda x: x[1])
    return min_tokenizer


def main():
    # Clear logs directory if it exists, then create it
    logs_dir = Path("logs")
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
    logs_dir.mkdir(exist_ok=True)
    
    # Store all results for final summary
    all_results = {}
    
    # Process each test text
    for text_name, text_path in TEST_TEXTS.items():
        print(f"\nProcessing: {text_name}...")
        
        # Load text
        text = load_text_file(text_path)
        
        # Test all tokenizers
        results = {}
        for tokenizer_name, tokenizer_path in TOKENIZERS.items():
            token_count = encode_and_count_tokens(tokenizer_path, text)
            results[tokenizer_name] = token_count
        
        # Sort results by token count for better readability
        results = dict(sorted(results.items(), key=lambda x: x[1]))
        
        # Store for final summary
        all_results[text_name] = results
        
        # Print table to console
        print_table(results, text_name)
        
        # Save to log file
        log_path = logs_dir / f"tokenized-{text_name}.log"
        save_to_log(results, text_name, log_path)
        print(f"Results saved to: {log_path}")
    
    # Print summary of most effective tokenizers
    print(f"\n{'='*60}")
    print("MOST EFFECTIVE TOKENIZERS SUMMARY")
    print(f"{'='*60}")
    
    summary_log_path = logs_dir / "summary-most-effective.log"
    with open(summary_log_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write("MOST EFFECTIVE TOKENIZERS SUMMARY\n")
        summary_file.write(f"{'='*60}\n\n")
        
        for text_name, results in all_results.items():
            best_tokenizer, best_count = find_most_effective(results)
            
            output = f"\n{text_name}:\n  Most effective: {best_tokenizer} ({best_count:,} tokens)"
            print(output)
            summary_file.write(output + "\n")
        
        summary_file.write(f"\n{'='*60}\n")
    
    print(f"\n{'='*60}")
    print(f"Summary saved to: {summary_log_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()