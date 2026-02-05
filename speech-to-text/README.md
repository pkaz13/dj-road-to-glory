# Speech-to-Text

Automatic speech recognition tool using OpenAI's Whisper model to transcribe audio files from WAV to text.

## Purpose

This tool processes audio files (WAV format) and generates text transcriptions using the Whisper-small model. It automatically detects and utilizes available hardware acceleration (CUDA, MPS, or CPU).

## Repository Structure

```
speech-to-text/
├── run.py              # Main script for transcription
├── requirements.txt    # Python dependencies
├── samples/           # Input folder - place your .wav files here
└── output/            # Output folder - transcriptions saved here as .txt files
```

### Folders

- **`samples/`** - Place your audio files (.wav) here for transcription
- **`output/`** - Transcribed text files are automatically saved here with matching filenames

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your audio files to the `samples/` folder

## Usage

Run the transcription:
```bash
python run.py
```

The script will:
- Automatically download the Whisper-small model on first run
- Process all `.wav` files in the `samples/` folder
- Save transcriptions to the `output/` folder

### Configuration

Edit `run.py` to customize:
- `MODEL_ID` - Change the Whisper model (default: `openai/whisper-small`)
- `VERBOSE` - Set to `True` to enable transformers library logs

## Cleanup

To delete the downloaded model and free up disk space:

```bash
# Remove Hugging Face cache (includes all downloaded models)
rm -rf ~/.cache/huggingface/hub/models--openai--whisper-small
```

Or remove all Hugging Face models:
```bash
rm -rf ~/.cache/huggingface/
```

The model cache location may vary by system. Common locations:
- Linux/macOS: `~/.cache/huggingface/`
- Windows: `C:\Users\USERNAME\.cache\huggingface\`
