# Calendar Manager - Harmonogram zajęć

Aplikacja do wizualizacji harmonogramu zajęć na podstawie plików kalendarzy w formacie ICS.

## Opis

Calendar Manager to aplikacja z interfejsem graficznym (GUI) stworzona w Pythonie, która pozwala na:
- Wczytywanie kalendarzy z plików `.ics`
- Wizualizację harmonogramu tygodniowego
- Filtrowanie wydarzeń według różnych kalendarzy
- Ukrywanie/pokazywanie wykładów
- Interaktywne wyświetlanie szczegółów wydarzeń

## Wymagania systemowe

- Python 3.6 lub nowszy
- System operacyjny: Windows, macOS lub Linux

## Instalacja zależności

Przed uruchomieniem aplikacji zainstaluj wymagane biblioteki:

```bash
pip install matplotlib ics
```

**Uwaga:** Biblioteka `tkinter` jest zazwyczaj dołączona do standardowej instalacji Pythona.


## Struktura folderów

```
calendar_manager/
├── main_app.py          # Główny plik aplikacji
├── README.md           # Ten plik
├── .resources/         # Zasoby aplikacji
│   └── icon.png       # Ikona aplikacji
└── calendars/         # Folder na pliki kalendarzy (pliki .ics)
    ├── kalendarz1.ics
    ├── kalendarz2.ics
    └── ...
```

## Jak dodać kalendarze

1. **Utwórz folder `calendars`** (jeśli nie istnieje):
   ```bash
   mkdir calendars
   ```

2. **Umieść pliki kalendarzy** w formacie **`.ics`** w folderze `calendars/`

3. **Format plików**: Aplikacja obsługuje standardowe pliki kalendarzowe ICS (iCalendar), które można wyeksportować z:
   - Google Calendar
   - Outlook
   - Apple Calendar
   - Innych aplikacji kalendarzowych

### Przykład eksportu z Google Calendar:
1. Otwórz Google Calendar
2. Kliknij na kalendarz, który chcesz wyeksportować
3. Wybierz "Ustawienia i udostępnianie"
4. Przewiń do sekcji "Integruj kalendarz"
5. Skopiuj link "Publiczny adres w formacie iCal"
6. Pobierz plik lub zapisz zawartość jako plik `.ics`

## Uruchamianie aplikacji

1. **Upewnij się**, że masz zainstalowane wszystkie zależności
2. **Umieść pliki `.ics`** w folderze `calendars/`
3. **Uruchom aplikację**:

```bash
python main_app.py
```

## Jak korzystać z aplikacji

1. **Uruchom aplikację** - otworzy się okno z harmonogramem
2. **Wybierz kalendarze** - zaznacz/odznacz checkboxy po lewej stronie
3. **Pokaż/ukryj wykłady** - użyj checkboxa "Pokaż wykłady (W)"
4. **Zaktualizuj wykres** - kliknij przycisk "Zaktualizuj wykres"
5. **Przeglądaj szczegóły** - najedź myszą na wydarzenia, aby zobaczyć ich nazwy