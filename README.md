# Faceit Stats Finder

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.3.2-green)
![Tkinter](https://img.shields.io/badge/tkinter-gui-yellow)
![License](https://img.shields.io/badge/license-MIT-orange)

Aplikacja do analizy statystyk graczy FACEIT CS2 poprzez integrację z API Steam i FACEIT.

## Spis treści
- [Funkcjonalności](#funkcjonalności)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Konfiguracja](#konfiguracja)
- [Uruchomienie](#uruchomienie)
- [API Endpoints](#api-endpoints)
- [Przykłady użycia](#przykłady-użycia)
- [Wsparcie](#wsparcie)
- [Licencja](#licencja)

## Funkcjonalności
✅ **Integracja z API**:
- Pobieranie danych z Steam (Vanity URL → SteamID64)
- Pobieranie statystyk FACEIT CS2
- Pobieranie informacji o koncie Steam

📊 **Statystyki**:
- Poziom i ELO FACEIT
- K/D Ratio, % headshotów, win rate
- Godziny w CS2 (ogółem/ostatnie 2 tygodnie)
- Status konta Steam (publiczne/prywatne)

👤 **Dane społecznościowe**:
- Awatar gracza
- Lista znajomych na Steam
- Link do profilu Steam

## Wymagania
- Python 3.8+
- Klucze API:
  - [FACEIT Developer Portal](https://developers.faceit.com/)
  - [Steam API Key](https://steamcommunity.com/dev/apikey)

## Instalacja
```bash
git clone https://github.com/twoj_nick/faceit-stats-finder.git
cd faceit-stats-finder
pip install -r requirements.txt
```

## Konfiguracja
Utwórz plik `.env` w głównym katalogu projektu:
```ini
FACEIT_API_KEY=your_faceit_key_here
STEAM_API_KEY=your_steam_key_here
```

## Uruchomienie
**Serwer API:**
```bash
python server.py
```

**Klient GUI:**
```bash
python client.py
```


## API Endpoints
### `GET /api/player`
**Parametry:**
- `steam_url` - URL profilu Steam (wymagane)

**Przykładowa odpowiedź:**
```json
{
  "nick": "ExamplePlayer",
  "elo": 2450,
  "level": 8,
  "stats": {
    "lifetime": {
      "Average K/D Ratio": "1.25",
      "Win Rate %": "52.3"
    }
  },
  "steam_profile_url": "https://steamcommunity.com/profiles/123456789"
}
```

## Przykłady użycia
1. Wprowadź URL profilu Steam:
   ```
   https://steamcommunity.com/id/nickname
   ```
   lub
   ```
   https://steamcommunity.com/profiles/76561197960287930
   ```

2. Kliknij "SZUKAJ GRACZA"

3. Przeglądaj statystyki w zakładkach:
   - **Statystyki gracza** - dane FACEIT i Steam
   - **Znajomi** - lista znajomych na Steam

## Wsparcie
Problem? [Otwórz issue](https://github.com/twoj_nick/faceit-stats-finder/issues)

## Licencja
Ten projekt jest dostępny jako **open-source** na licencji MIT.

---
