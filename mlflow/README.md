# MLFlow quickstart

MLFlow to paczka pythonowa - musisz mieć ją zainstalowaną (globalnie lub środowisko typu virtualenv).
Quickstart: https://mlflow.org/docs/latest/genai/getting-started/

## FLOW

- agent integruje się z modelem (wiadomo)
- mlflow "nasłuchuje" tę komunikację
- musimy sprowokować dowolnego nasłuchiwanego agenta aby się "odezwał" do modelu
  - może to być `claude -p "bla bla"` (z CLI)
  - może to być dowolny lokalny model (uruchomiony za pośrednictwem ollama, llama.cpp, cokolwiek)
- (po zainstalowaniu zależności - wiadomo) uruchamiasz `mlflow ui`

Szczegółowe instrukcje poniżej.

## venv setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

albo `pip install mlflow`

## uruchomienie MLFlow UI (konieczne)

    mlflow ui
    mlflow ui --port 5001

## Podsłuchiwanie Claude

    mlflow autolog claude -u file:./mlruns

check:

    mlflow autolog claude --status

uruchomienie claude z konsoli:

    claude -p "write a poem about MLFlow in Polish"

albo edycja pliku pythonowego:

    claude -p "claude -p 'refactor the python function in test.py to use list comprehension'"

wyłączenie:

    mlflow autolog claude --disable

## Trouble shooting

Po uruchomieniu komendy 

```bash
mlflow autolog claude -u file:./mlruns
```

generuje się plik .claude/settings.json:

```json
{
  "environment": {
    "MLFLOW_TRACKING_URI": "file:./mlruns",
    "MLFLOW_CLAUDE_TRACING_ENABLED": "true"
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python -c \"from mlflow.claude_code.hooks import stop_hook_handler; stop_hook_handler()\""
          }
        ]
      }
    ]
  }
}
```

trzeba zastąpić komendę

```python
python -c \"from mlflow.claude_code.hooks import stop_hook_handler; stop_hook_handler()\"
```

na

```python
python -c 'from mlflow.claude_code.hooks import stop_hook_handler; stop_hook_handler()'