# Wyjaśnienie pliku `csma_cd.py`

Ten plik realizuje symulację metody dostępu do medium CSMA/CD (Carrier Sense Multiple Access with Collision Detection) na wspólnym łączu, modelowanym jako tablica.

## Kluczowe elementy programu

- **Medium** – reprezentowane przez klasę `Medium`, która przechowuje stan łącza jako listę znaków (każda komórka to fragment łącza). Sygnały stacji są propagowane do sąsiednich komórek, a kolizje oznaczane jako 'X'.
- **Stacje** – klasa `Station` reprezentuje pojedynczą stację, która może być w stanie oczekiwania (`idle`), nadawania (`sending`) lub wycofania po kolizji (`backoff`).
- **Rozmieszczenie stacji** – stacje są rozmieszczone równomiernie na łączu.
- **Symulacja krokowa** – w każdej iteracji (kroku):
  1. Stacje decydują, czy próbują nadawać (z prawdopodobieństwem 0.1 na krok).
  2. Sygnały są propagowane w medium.
  3. Wykrywane są kolizje – jeśli stacja wykryje kolizję w swoim miejscu, przechodzi w stan `backoff` na losową liczbę kroków.
  4. Stan medium i stacji jest wypisywany w czytelnej formie.

## Przykład działania

- Każda stacja jest oznaczona literą (A, B, C...).
- Medium jest wyświetlane jako ciąg znaków: '.' oznacza ciszę, litera – sygnał stacji, 'X' – kolizję.
- Informacje o stanie każdej stacji są wypisywane pod medium.

## Użycie

```
python3 csma_cd.py <liczba_stacji> <długość_łącza> <liczba_kroków>
```

Przykład:
```
python3 csma_cd.py 3 20 15
```

## Podsumowanie

Plik ten pozwala na wizualizację i analizę działania algorytmu CSMA/CD na prostym modelu, pokazując propagację sygnałów, wykrywanie kolizji i zachowanie stacji w czasie.

# Wyjaśnienie przykładowego przebiegu symulacji CSMA/CD

Poniżej znajduje się interpretacja przykładowego wyjścia programu dla 5 stacji, długości łącza 15 i 12 kroków symulacji.

## Format wyjścia

- Każdy wiersz `Krok N: ...` pokazuje stan medium w danym kroku:
  - `.` – cisza (brak sygnału)
  - `A`, `B`, `C`, `D`, `E` – sygnał nadawany przez odpowiednią stację
  - `X` – kolizja (sygnały różnych stacji na tej samej pozycji)
- Pod spodem wypisany jest stan każdej stacji:
  - `nadaje` – stacja aktywnie nadaje sygnał
  - `czeka` – stacja nie nadaje, czeka na swoją kolej
  - `backoff(x)` – stacja odczekuje po kolizji (nie występuje w tym fragmencie)

## Przykład i interpretacja

```
Krok  0: ....BBB........
  A: czeka, B: nadaje, C: czeka, D: czeka, E: czeka
```
- Tylko stacja B zaczęła nadawać, jej sygnał propaguje się w medium.

```
Krok  2: .AAABBB..DDD...
  A: nadaje, B: nadaje, C: czeka, D: nadaje, E: czeka
```
- Stacje A, B i D nadają jednocześnie, ich sygnały rozchodzą się w medium.

```
Krok  3: .AAABBXCCDDD...
  A: nadaje, B: nadaje, C: nadaje, D: nadaje, E: czeka
```
- Stacja C zaczęła nadawać.
- W miejscu, gdzie sygnały B i C się spotykają, pojawia się `X` – kolizja.

```
Krok  9: .AAABBXCCDDXEE.
  A: nadaje, B: nadaje, C: nadaje, D: nadaje, E: nadaje
```
- Wszystkie stacje nadają.
- W medium pojawiają się dwie kolizje (`X`): jedna między B i C, druga między D i E.

## Wnioski

- Kolizje powstają tam, gdzie sygnały różnych stacji spotykają się w medium.
- Stacje, które wykryją kolizję w swoim miejscu, w rzeczywistej sieci Ethernet przechodzą w stan `backoff` (tutaj mogą jeszcze przez chwilę nadawać, zależnie od implementacji).
- Symulacja pozwala obserwować propagację sygnałów i miejsca kolizji, co ilustruje działanie CSMA/CD.
