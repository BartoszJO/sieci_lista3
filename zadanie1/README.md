"""
README - zadanie 1
Kodowanie i dekodowanie ramek z sumą kontrolną CRC, bit stuffingiem i flagami.

Pliki:
- program.py         - główny plik z kodem
- test_frameprocessor.py - testowanie kodowania i dekodowania
- sposoby_uzycia.txt - przykłady użycia

Opis działania:
Program koduje plik wejściowy do ramek z CRC, bit stuffingiem i flagami, a następnie umożliwia dekodowanie z powrotem do oryginalnych danych.

Uruchomienie:
python3 program.py encode <plik_wejściowy> <plik_wyjściowy>
python3 program.py decode <plik_wejściowy> <plik_wyjściowy>

Testowanie:
python3 test_frameprocessor.py
"""

# Ramkowanie z rozpychaniem bitów i weryfikacją CRC

## Opis zadania

Program realizuje ramkowanie zgodnie z zasadą "rozpychania bitów" (bit stuffing) oraz weryfikację poprawności ramki metodą CRC. Odpowiada na wymagania:

- Odczyt pliku źródłowego `Z` zawierającego ciąg znaków '0' i '1' (symulacja strumienia bitów).
- Podział danych na ramki, dodanie pól kontrolnych CRC, zastosowanie rozpychania bitów.
- Zapis sformatowanych ramek do pliku wynikowego `W`.
- Możliwość odwrotnej operacji: odczyt pliku ramek `W`, weryfikacja CRC, usunięcie rozpychania bitów i odtworzenie oryginalnego pliku `Z`.

## Jak program spełnia wymagania?

1. **Ramkowanie i rozpychanie bitów**
   - Dane wejściowe są dzielone na fragmenty (domyślnie po 64 bity).
   - Każdy fragment jest ramkowany: na początku i końcu dodawana jest flaga (`01111110`).
   - Zasada rozpychania bitów: po każdych pięciu kolejnych jedynkach wstawiane jest zero, aby uniknąć przypadkowego pojawienia się wzorca flagi w danych.

2. **Weryfikacja i pole CRC**
   - Dla każdego fragmentu danych obliczane jest CRC-8 (wielomian x⁸ + x² + x¹ + 1).
   - Wartość CRC jest dołączana do danych przed rozpychaniem bitów.
   - Podczas dekodowania CRC jest weryfikowane – tylko poprawne ramki są przepisywane do pliku wynikowego.

3. **Obsługa plików**
   - Program przyjmuje polecenia:
     - `encode Z.txt W.txt` – koduje plik źródłowy do ramek.
     - `decode W.txt Z_decoded.txt` – dekoduje plik ramek, odtwarzając oryginalne dane.
   - Obsługa błędów i informacja o liczbie poprawnych ramek.

## Przykład użycia

Zakładając, że plik `Z.txt` zawiera:
```
110111111111000101...
```
Kodowanie:
```
python3 program.py encode Z.txt W.txt
```
- Odczyt danych z `Z.txt`
- Podział na fragmenty, obliczenie CRC, rozpychanie bitów, dodanie flag
- Zapis ramek do `W.txt`

Dekodowanie:
```
python3 program.py decode W.txt Z_decoded.txt
```
- Odczyt ramek z `W.txt`
- Usunięcie flag, rozpychania bitów, weryfikacja CRC
- Zapis poprawnych danych do `Z_decoded.txt` (powinien być identyczny z oryginalnym `Z.txt`)

## Podsumowanie

Program automatyzuje proces ramkowania i weryfikacji danych zgodnie z wymaganiami zadania, umożliwiając zarówno kodowanie, jak i dekodowanie plików binarnych z zachowaniem integralności danych dzięki CRC i rozpychaniu bitów.
