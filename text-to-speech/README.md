# Text-To-Speech (Coqui XTTS)

A Python-based Text-to-Speech (TTS) application that uses Coqui XTTS v2 model to generate speech in multiple languages using a reference voice sample.

## Features

- 🎙️ Voice cloning from audio samples (WAV/MP3)
- 🌍 Multilingual support (English and other languages)
- 🚀 Apple Silicon (MPS) GPU acceleration support
- 💾 Automatic model caching (no re-download on subsequent runs)
- 📊 Rich terminal interface with progress indicators

## Requirements

- **Python 3.12** (required)
- **FFmpeg** (system-level installation required)

## Repository Structure

```
text-to-speech/
├── run.py                 # Main application script
├── requirements.txt       # Python dependencies
├── .python-version        # Python version specification
├── samples/              # Input folder for reference voice samples
│   └── sample-my.wav     # Example voice sample
└── output/               # Generated audio files location
    └── output_*.wav      # Cloned voice outputs (timestamped)
```

### Folder Purposes

- **`samples/`** - Place your reference voice audio files here (WAV or MP3 format). The script will use the first audio file found to clone the voice characteristics.

- **`output/`** - Generated audio files are automatically saved here with timestamped filenames (e.g., `output_1770301247.wav`).

## Installation

### 1. Install FFmpeg (Required)

FFmpeg is required for audio processing. Install it system-wide:

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### 2. Set up Python environment

Make sure you have Python 3.12 installed:

```bash
python --version  # Should show Python 3.12.x
```

### 3. Create virtual environment and install dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Prepare your voice sample

Place a voice sample (WAV or MP3) in the `samples/` folder. The sample should:
- Be at least 6-10 seconds long
- Contain clear speech
- Have minimal background noise

### 2. Run the application

```bash
python run.py
```

### 3. First run behavior

On the first run, the script will:
- Download the XTTS v2 model (~2GB) to cache
- This may take several minutes depending on your internet connection
- Model is cached at `~/Library/Application Support/tts/` (macOS)

Subsequent runs will use the cached model and start much faster.

### 4. Output

Generated audio files will be saved in the `output/` folder with timestamped filenames.

## How It Works

1. **Voice Sample Detection**: Script scans the `samples/` folder for audio files
2. **Model Loading**: Loads the Coqui XTTS v2 model (from cache or downloads if needed)
3. **Device Detection**: Automatically detects and uses Apple Silicon (MPS), CUDA GPU, or CPU
4. **Voice Synthesis**: Generates speech using the reference voice characteristics
5. **Output**: Saves the cloned voice audio to the `output/` folder

## Customization

To modify the text being spoken, edit line 113 in `run.py`:

```python
text_to_speak = "Your custom text here"
```

To change the language, modify line 122:

```python
args=(tts, text_to_speak, sample_file, output_filename, "en")  # Change "en" to your language code
```

Supported language codes: `en`, `es`, `fr`, `de`, `it`, `pt`, `pl`, `tr`, `ru`, `nl`, `cs`, `ar`, `zh-cn`, `ja`, `hu`, `ko`

## Troubleshooting

### "Could not load libtorchcodec" error
- Make sure FFmpeg is installed system-wide
- Verify with: `ffmpeg -version`

### "CUDA is not available" error
- This means the script tried to use CUDA (NVIDIA GPU) but it's not available
- Fixed in the current version - now properly detects Apple Silicon (MPS)

### Model download issues
- Check your internet connection
- Ensure you have ~2GB of free disk space
- Model cache location: `~/Library/Application Support/tts/` (macOS)

## Credits

- [Coqui TTS](https://github.com/coqui-ai/TTS) - Text-to-Speech engine
- [XTTS v2](https://huggingface.co/coqui/XTTS-v2) - Voice cloning model
