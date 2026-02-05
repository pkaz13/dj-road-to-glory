import os
import sys
import threading
import time
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
import warnings

# Inicjalizacja konsoli Rich
console = Console()

warnings.filterwarnings("ignore", category=UserWarning)

# Konfiguracja ścieżek
SAMPLES_DIR = Path("samples")
OUTPUT_DIR = Path("output")
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"


def get_first_sample():
    """Pobiera pierwszy dostępny plik audio z folderu samples."""
    supported_ext = [".wav", ".mp3"]
    for file in SAMPLES_DIR.iterdir():
        if file.suffix.lower() in supported_ext:
            return file
    return None


def generate_audio_thread(tts_obj, text, speaker_wav, output_path, lang="en"):
    """Funkcja uruchamiana w osobnym wątku - wykonuje generowanie."""
    try:
        # Generowanie pliku (to jest proces blokujący)
        tts_obj.tts_to_file(
            text=text,
            file_path=str(output_path),
            speaker_wav=str(speaker_wav),
            language=lang,
            split_sentences=True,
        )
    except Exception as e:
        # Przekazujemy wyjątek wyżej (w uproszczeniu zapisujemy go w atrybucie wątku)
        threading.current_thread().error = e


def main():
    console.print(
        Panel.fit(
            "[bold blue]AI Voice Cloner (Coqui XTTS)[/bold blue]", border_style="blue"
        )
    )

    # KROK 1: Sprawdzenie środowiska
    if not SAMPLES_DIR.exists():
        SAMPLES_DIR.mkdir()
        console.print(
            f"[bold red]Błąd:[/bold red] Utworzono brakujący folder '{SAMPLES_DIR}'. Wrzuć tam plik .wav lub .mp3 i uruchom ponownie."
        )
        return

    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir()

    sample_file = get_first_sample()
    if not sample_file:
        console.print(
            f"[bold red]Błąd:[/bold red] Folder '{SAMPLES_DIR}' jest pusty. Dodaj plik dźwiękowy (wav/mp3)."
        )
        return

    console.print(
        f"[bold green]Sukces:[/bold green] Znaleziono próbkę głosu: [cyan]{sample_file.name}[/cyan]"
    )

    # Import TTS wewnątrz main, aby nie spowalniać startu skryptu, ale tu robimy to globalnie
    # dla czytelności. Najcięższe jest ładowanie modelu.

    tts = None

    # KROK 2: Ładowanie modelu
    try:
        # Importujemy tutaj, aby złapać ewentualne błędy importu
        from TTS.api import TTS
        from TTS.utils.manage import ModelManager
        import torch

        # Wykrycie odpowiedniego urządzenia
        if torch.cuda.is_available():
            device = "cuda"
            device_txt = "CUDA GPU"
        elif torch.backends.mps.is_available():
            device = "mps"
            device_txt = "Apple Silicon (MPS)"
        else:
            device = "cpu"
            device_txt = "CPU"

        console.print(f"[bold cyan]Wykryto urządzenie:[/bold cyan] {device_txt}")

        # Sprawdzenie czy model jest już pobrany (przed pobraniem)
        manager = ModelManager()
        
        # Pobierz ścieżkę do cache modelu
        output_path = Path(manager.output_prefix)
        model_dir_name = MODEL_NAME.replace("/", "--")
        model_cache_path = output_path / model_dir_name
        
        print("ścieżka modelu:", model_cache_path)
        is_cached = model_cache_path.exists() and any(model_cache_path.iterdir())

        if is_cached:
            console.print("[bold green]✓[/bold green] Model znaleziony w cache")
            status_msg = "[bold yellow]Ładowanie modelu...[/bold yellow]"
        else:
            console.print("[bold yellow]⚠[/bold yellow] Model nie znaleziony - rozpoczynam pobieranie")
            status_msg = "[bold yellow]Pobieranie i ładowanie modelu (pierwsza instalacja, ~2GB, może potrwać)...[/bold yellow]"

        with console.status(status_msg, spinner="dots"):
            # Inicjalizacja modelu (TTS automatycznie pobiera model jeśli nie istnieje)
            tts = TTS(model_name=MODEL_NAME, progress_bar=False)

            # Przeniesienie modelu na odpowiednie urządzenie
            tts.to(device)

        console.print(f"[bold green]Sukces:[/bold green] Model załadowany i gotowy.")

    except Exception as e:
        console.print(
            f"[bold red]Błąd krytyczny podczas ładowania modelu:[/bold red] {e}"
        )
        return

    # Tekst do syntezy
    text_to_speak = (
        "To jest testowy tekst do syntezy głosu."
    )
    output_filename = OUTPUT_DIR / f"output_{int(time.time())}.wav"

    # KROK 3: Generowanie (w osobnym wątku)
    console.print(
        f"[bold white]Rozpoczynam generowanie dla tekstu:[/bold white] '{text_to_speak}'"
    )

    generation_thread = threading.Thread(
        target=generate_audio_thread,
        args=(tts, text_to_speak, sample_file, output_filename, "pl"),
    )

    # Uruchomienie wątku
    generation_thread.start()

    # Wyświetlanie paska postępu/spinnera dopóki wątek żyje
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Generowanie dźwięku...[/cyan]", total=None)

        while generation_thread.is_alive():
            time.sleep(0.1)
            # Tutaj można by aktualizować pasek, gdyby API Coqui zwracało % w callbacku,
            # ale XTTS tego nie robi w prosty sposób, więc używamy 'indeterminate' spinnera.

    # Sprawdzenie czy wystąpił błąd w wątku
    if hasattr(generation_thread, "error"):
        console.print(
            f"[bold red]Błąd podczas generowania:[/bold red] {generation_thread.error}"
        )
    else:
        console.print(
            f"[bold green]Sukces![/bold green] Plik zapisano w: [bold underline]{output_filename}[/bold underline]"
        )


if __name__ == "__main__":
    # Ustawienie zmiennej środowiskowej, aby Coqui nie pytało o zgodę na licencję w CLI
    os.environ["COQUI_TOS_AGREED"] = "1"
    main()
