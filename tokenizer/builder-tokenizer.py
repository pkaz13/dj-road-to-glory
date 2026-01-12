import os
from typing import List
from tokenizers import Tokenizer, models, pre_tokenizers, decoders, trainers, processors
from corpora import get_corpus_file

def train_dynamic_tokenizer(corpus_files: List[str], corpus_name: str, vocab_size: int = 30000):
    """
    Trains a BPE tokenizer on the provided corpus files and saves it to a JSON file.
    
    Args:
        corpus_files: List of paths to text files containing the training data.
        corpus_name: Name of the corpus (used for output filename).
        vocab_size: The maximum size of the vocabulary to be generated.
    """
    
    # 1. Initialize the Tokenizer with a BPE model
    # We use BPE because it handles unknown words well by breaking them into subwords.
    tokenizer = Tokenizer(models.BPE(unk_token="[UNK]"))

    # 2. Pre-tokenization
    # ByteLevel is popular for LLMs (like GPT-2/Mistral). It handles unicode characters 
    # directly at the byte level, ensuring no "unknown" characters usually.
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)

    # 3. Decoding
    # This ensures we can reverse the process (IDs -> Text) correctly.
    tokenizer.decoder = decoders.ByteLevel()

    # 4. Post-processing
    # Not strictly necessary for raw training, but useful if you want to mimic 
    # specific model inputs (like adding BOS/EOS tokens automatically).
    # Here we leave it basic for versatility.

    # 5. Define the Trainer
    # The trainer manages the vocabulary learning process.
    # special_tokens are critical for LLMs (Unknown, Beginning of Sentence, End of Sentence, Padding).
    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"],
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet()
    )

    print(f"Starting training for corpus: '{corpus_name}'...")
    
    # 6. Train the tokenizer
    # The library reads the files line by line (memory efficient).
    tokenizer.train(files=corpus_files, trainer=trainer)

    # 7. Save the tokenizer
    output_dir = "tokenizers"
    os.makedirs(output_dir, exist_ok=True)
    
    output_filename = f"{corpus_name}-tokenizer.json"
    output_path = os.path.join(output_dir, output_filename)
    
    tokenizer.save(output_path)
    print(f"Success! Tokenizer saved to: {output_path}")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    
    # NKJP corpus
    # Ensure this files exist in your 'data' folder
    corpus_files = [str(file) for file in get_corpus_file("NKJP", "*.txt")]
    corpus_name = "nkjp" 

    # Run the training
    try:
        train_dynamic_tokenizer(corpus_files, corpus_name, vocab_size=32000)
    except Exception as e:
        print(f"Error during training: {e}")