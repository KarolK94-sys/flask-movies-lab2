# Flask Movies Database

Aplikacja webowa do zarządzania bazą danych filmów, zbudowana z użyciem Flask i SQLite.

## Funkcjonalności

- Wyświetlanie listy filmów
- Dodawanie nowych filmów
- Usuwanie zaznaczonych filmów

## Wymagania

- Python 3.8+
- Flask

## Instalacja

1. Sklonuj repozytorium:
   ```
   git clone <URL_REPOZYTORIUM>
   cd flask-movies-lab2
   ```

2. Utwórz wirtualne środowisko:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # na Windows
   ```

3. Zainstaluj zależności:
   ```
   pip install -r requirements.txt
   ```

## Uruchomienie

Uruchom aplikację:
```
python app.py
```

Aplikacja będzie dostępna pod adresem: http://127.0.0.1:5000

## Struktura projektu

- `app.py`: Główny plik aplikacji Flask
- `templates/`: Szablony HTML (home.html, add.html)
- `static/`: Pliki statyczne (style.css)
- `movies.db`: Baza danych SQLite (tworzona automatycznie)