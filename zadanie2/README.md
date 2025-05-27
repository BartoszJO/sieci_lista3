# Symulacja metody CSMA/CD w Ethernet

## Opis zadania

Programy w tym katalogu realizują symulację ethernetowej metody dostępu do medium transmisyjnego (CSMA/CD). Wspólne łącze jest reprezentowane przez tablicę, a propagacja sygnału odbywa się poprzez przekazywanie wartości do sąsiednich komórek tej tablicy. Celem jest umożliwienie łatwego testowania różnych scenariuszy oraz uzyskanie czytelnych wyników.

## Struktura rozwiązania

- **csma_cd.py** – główny program symulujący działanie stacji korzystających z CSMA/CD.
- **main.py** – skrypt uruchamiający automatycznie serię testów z różnymi parametrami (liczba stacji, długość łącza, liczba kroków symulacji).

## Jak to działa?

1. **Reprezentacja medium**  
   Medium transmisyjne (wspólne łącze) jest modelowane jako tablica (lista), gdzie każda komórka odpowiada fragmentowi łącza. Sygnały (np. transmisja, kolizja) są propagowane do sąsiednich komórek w kolejnych krokach czasowych, co imituje rzeczywistą propagację sygnału w przewodzie.

2. **Stacje**  
   Każda stacja jest przypisana do określonego miejsca na łączu. Stacje próbują nadawać zgodnie z algorytmem CSMA/CD: najpierw nasłuchują medium, a jeśli jest wolne – rozpoczynają transmisję. W przypadku wykrycia kolizji, stacja przerywa nadawanie i stosuje algorytm ponownego nadawania (backoff).

3. **Symulacja krokowa**  
   Symulacja przebiega w zadanej liczbie kroków czasowych. W każdym kroku aktualizowany jest stan medium oraz stacji, a sygnały są propagowane w tablicy.

4. **Testowanie i wyniki**  
   Skrypt `main.py` automatycznie uruchamia symulacje dla różnych konfiguracji (liczba stacji, długość łącza, liczba kroków). Wyniki są wypisywane na standardowe wyjście w czytelnej formie, co ułatwia analizę działania algorytmu i interpretację rezultatów.

## Jak uruchomić?

W katalogu `zadanie2` uruchom:
```
python3 main.py
```
Program automatycznie przeprowadzi serię testów i wyświetli wyniki.

### Przykład użycia i wyjaśnienie

Fragment kodu z `main.py`:
```python
test_cases = [
    (2, 10, 10),   # (liczba stacji, długość łącza, liczba kroków)
    (3, 20, 15),
    (4, 30, 20),
    (5, 15, 12),
]
for n, l, s in test_cases:
    run_test(n, l, s)
```
- `(2, 10, 10)`  
  - **2** – liczba stacji w symulacji  
  - **10** – długość łącza (liczba komórek tablicy reprezentującej medium)  
  - **10** – liczba kroków symulacji (ile razy zostanie zaktualizowany stan sieci)

Wywołanie:
```
python3 main.py
```
spowoduje uruchomienie czterech testów z powyższymi parametrami. Każdy test wypisze na ekranie wyniki symulacji dla danej konfiguracji.

Przykładowy fragment wyjścia:
```
=== Test: stacje=2, dlugosc=10, kroki=10 ===
[tu pojawi się wynik działania csma_cd.py dla tych parametrów]
```
- **stacje=2** – liczba stacji w tym teście
- **dlugosc=10** – długość łącza
- **kroki=10** – liczba kroków symulacji

## Podsumowanie

Rozwiązanie umożliwia łatwe eksperymentowanie z parametrami symulacji CSMA/CD oraz analizę zachowania sieci Ethernet w różnych warunkach. Dzięki modularnej budowie i automatyzacji testów, kod jest wygodny do dalszych modyfikacji i rozbudowy.
