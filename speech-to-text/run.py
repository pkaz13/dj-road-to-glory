import os
import torch
from pathlib import Path
from transformers import pipeline
from transformers import logging as transformers_logging
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Konfiguracja ścieżek i modelu
MODEL_ID = "openai/whisper-small"
SAMPLES_DIR = Path("samples")
OUTPUT_DIR = Path("output")
VERBOSE = False  # Ustaw True aby włączyć logi z transformers

def get_device():
    """Wybiera najlepsze dostępne urządzenie obliczeniowe."""
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"

def transcribe_audio(verbose=False):
    """Główna funkcja ładująca model i przetwarzająca pliki.
    
    Args:
        verbose: Jeśli True, wyświetla logi z biblioteki transformers.
                 Jeśli False, wycisza większość wyjścia z transformers.
    """
    
    # Konfiguracja logowania transformers
    if verbose:
        transformers_logging.set_verbosity_info()
    else:
        transformers_logging.set_verbosity_error()
    
    # Tworzenie folderów jeśli nie istnieją
    SAMPLES_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    device = get_device()
    print(f"Używane urządzenie: {device.upper()}")

    # Inicjalizacja modelu ASR
    # 'accelerate' pomaga przy automatycznym dopasowaniu wag (device_map)
    print(f"Inicjalizacja modelu {MODEL_ID}...")
    
    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model=MODEL_ID,
        device=device,
        chunk_length_s=30, # Obsługa długich nagrań przez dzielenie na 30s okna
    )

    # Pobranie listy plików .wav
    audio_files = list(SAMPLES_DIR.glob("*.wav"))
    
    if not audio_files:
        print("Folder /samples jest pusty. Dodaj pliki .wav.")
        return

    for file_path in audio_files:
        print(f"Przetwarzanie: {file_path.name}")
        
        # Generowanie transkrypcji
        # return_timestamps=True ułatwia modelowi synchronizację przy długich plikach
        result = asr_pipeline(str(file_path), return_timestamps=True)
        transcription_text = result["text"]

        # Zapis do pliku .txt
        output_path = OUTPUT_DIR / f"{file_path.stem}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcription_text)
            
        print(f"Sukces! Wynik zapisany w: {output_path}")

if __name__ == "__main__":
    print("--- Rozpoczęcie pracy skryptu STT ---")
    transcribe_audio(verbose=VERBOSE)
    print("--- Zadanie zakończone ---")