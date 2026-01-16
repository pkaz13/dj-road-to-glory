# loading raw sentences from files and aggregating them
def aggregate_raw_sentences(files):
    raw_sentences = []
    print("Loading text from files...")
    print(f"Number of files to load: {len(files)}")
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
                raw_sentences.extend(lines)
        except FileNotFoundError:
            print(f"WARNING: File '{file}' not found. Skipping.")
            continue

    if not raw_sentences:
        print("ERROR: Input files are empty or not loaded.")
        exit()
    return raw_sentences