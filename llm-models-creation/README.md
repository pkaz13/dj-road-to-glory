# Tworzenie Własnych Modeli w Ollama (Modelfile Guide)

Niniejszy przewodnik opisuje proces tworzenia, konfiguracji i optymalizacji lokalnych modeli LLM przy użyciu mechanizmu **Modelfile**. Dokumentacja bazuje na modelu **Deepseek-R1:8b**.

Oficjalna dokumentacja: [Modelfile Reference](https://docs.ollama.com/modelfile).

---

## 1. Struktura repozytorium

```
llm-models-creation/
├── README.md
└── ollama/
    └── <nazwa-modelu>/           # np. python-senior-dev
        ├── Modelfile             # przepis na model (FROM, SYSTEM, PARAMETER, …)
        └── blob-layers/          # warstwy utworzone przez Ollama przy budowaniu
            ├── sha256-<hash1>
            ├── sha256-<hash2>
            └── sha256-<hash3>
```

### Czym są `blob-layers`?

Katalog **`blob-layers/`** zawiera pliki o nazwach w formacie **`sha256-<hash>`**. Powstają one automatycznie, gdy uruchomisz:

```bash
ollama create <nazwa-modelu> -f Modelfile
```

Ollama zapisuje w nich zbudowane warstwy modelu (m.in. wagi i metadane). Są to wewnętrzne artefakty budowania – **nie edytuj ani nie usuwaj ich ręcznie**; służą Ollama do odtwarzania i cache’owania modeli. Repozytorium może je przechowywać, aby odtworzyć dokładnie ten sam model w innym środowisku (np. bez ponownego `ollama create` z tego samego Modelfile).

---

## 2. Czym jest Modelfile?

**Modelfile** to plik konfiguracyjny będący "przepisem" na model. Działa analogicznie do `Dockerfile` – definiuje on fundament, zachowanie i parametry techniczne agenta AI.

* **Rola:** Pozwala "zamrozić" instrukcje systemowe i ustawienia silnika, tworząc dedykowane narzędzie (np. asystenta kodu lub audytora danych).
* **Zaleta:** Eliminuje konieczność każdorazowego wpisywania długich promptów instruktażowych.

---

## 3. Komendy CLI: pull → build → run → (opcjonalnie) remove

Poniższe polecenia realizują pełny cykl: pobranie bazy, zbudowanie modelu, uruchomienie i ewentualne usunięcie. Wykonuj je w katalogu zawierającym `Modelfile` (np. `ollama/python-senior-dev/`).

| Krok | Komenda | Opis |
| :--- | :--- | :--- |
| **1. Pull** | `ollama pull <model-bazowy>` | Pobiera bazowy model z biblioteki Ollama (np. `ollama pull deepseek-r1:8b`). Wymagane przed `create`. |
| **2. Build** | `ollama create <nazwa-modelu> -f Modelfile` | Buduje własny model z pliku `Modelfile`; tworzy m.in. pliki w `blob-layers/`. |
| **3. Run** | `ollama run <nazwa-modelu>` | Uruchamia interaktywną sesję z modelem. |
| **Lista** | `ollama list` | Wyświetla listę modeli (w tym zbudowanych). |
| **4. Remove (opcjonalnie)** | `ollama rm <nazwa-modelu>` | Usuwa model z dysku (np. gdy nie jest już potrzebny). |

**Przykład dla modelu z tego repozytorium:**

```bash
cd ollama/python-senior-dev
ollama pull deepseek-r1:8b
ollama create python-senior-dev -f Modelfile
ollama run python-senior-dev
# opcjonalnie: ollama rm python-senior-dev
```

---

## 4. Struktura Pliku Modelfile

Plik konfiguracyjny składa się z instrukcji sterujących zachowaniem modelu:

### Główne Instrukcje
* **`FROM`**: Definiuje model bazowy (np. `FROM deepseek-r1:8b`).
* **`SYSTEM`**: Ustawia tzw. *System Prompt* – stałą instrukcję określającą rolę i zasady zachowania AI.
* **`TEMPLATE`**: Definiuje strukturę promptu przekazywanego do modelu. Określa formatowanie (np. znaczniki `<|user|>`, `[INST]`), które model rozumie. Domyślnie dziedziczone z modelu bazowego.
* **`PARAMETER`**: Konfiguruje techniczne aspekty generowania tekstu.
* **`MESSAGE`**: Pozwala na dodanie historii rozmowy (tzw. few-shot prompting), co uczy model pożądanego formatu odpowiedzi na przykładach.

### Parametry Techniczne (`PARAMETER`)
| Parametr | Opis | Zastosowanie |
| :--- | :--- | :--- |
| `temperature` | Losowość (0.0 - 1.0). | 0.1-0.3 dla logiki i kodu; 0.7+ dla kreatywności. |
| `num_ctx` | Okno kontekstowe (np. 4096). | Określa, ile tekstu wstecz model jest w stanie zapamiętać. |
| `stop` | Ciąg znaków zatrzymania. | Zapobiega generowaniu zbędnych treści (np. pisaniu za użytkownika). |
| `repeat_penalty` | Kara za powtórzenia. | Zapobiega zapętleniu się modelu na tych samych frazach. |

---

## 5. Praktyczny Przykład: Senior Python Dev

Poniższy przykład konfiguruje Deepseek-R1:8b jako eksperta od Pythona. Uwzględniono w nim opcjonalny parametr `TEMPLATE` (dla celów edukacyjnych), choć zazwyczaj dziedziczy się go z modelu bazowego.

### Plik `Modelfile`
```dockerfile
# 1. Baza
FROM deepseek-r1:8b

# 2. Parametry (Precyzja ponad kreatywność)
PARAMETER temperature 0.2
PARAMETER num_ctx 4096

# 3. Szablon (Opcjonalny - tu przykład standardowego formatu ChatML)
# Używamy składni Go templates.
# TEMPLATE """{{ if .System }}<|im_start|>system
# {{ .System }}<|im_end|>
# {{ end }}{{ if .Prompt }}<|im_start|>user
# {{ .Prompt }}<|im_end|>
# {{ end }}<|im_start|>assistant
# """

# 4. Rola i zasady
SYSTEM """
Jesteś seniorem backendu Python. 
Twoje odpowiedzi muszą być techniczne i konkretne.
- Zawsze używaj Type Hinting.
- Nie tłumacz podstawowych pojęć.
- Kod musi być zgodny z PEP 8.
Odpisuj w języku polskim.
"""

# 5. Przykładowy format odpowiedzi (Few-shot)
MESSAGE user "Napisz funkcję do sumowania listy."
MESSAGE assistant "```python\ndef sum_list(items: list[int | float]) -> int | float:\n    return sum(items)\n```"