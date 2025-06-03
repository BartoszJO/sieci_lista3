#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Symulacja metody dostępu CSMA/CD na wspólnym łączu (tablica)
Użycie:
  python3 csma_cd.py <liczba_stacji> <długość_łącza> <liczba_kroków>

Stacje są rozmieszczone równomiernie na łączu. Każda stacja może próbować nadawać z prawdopodobieństwem 0.1 na krok.
Wyniki symulacji są wypisywane w czytelnej formie.
"""

import sys
import random

# Klasa reprezentująca stację w sieci
class Station:
    def __init__(self, pos, id):
        self.pos = pos  # pozycja stacji na łączu
        self.id = id    # identyfikator stacji (liczba)
        self.state = 'idle'  # możliwe stany: 'idle' (czeka), 'sending' (nadaje), 'backoff' (odczekuje po kolizji)
        self.backoff = 0     # licznik czasu backoff
        self.collision = False
        self.tx_timer = 0    # licznik czasu nadawania

# Klasa reprezentująca medium transmisyjne (łącze)
class Medium:
    def __init__(self, length):
        self.length = length
        self.cells = ['.'] * length  # '.' = cisza, 'A','B',... = sygnał stacji, 'X' = kolizja
        self.owners = [set() for _ in range(length)]  # lista zbiorów: które stacje mają sygnał w danej komórce

    def clear(self):
        self.cells = ['.'] * self.length
        self.owners = [set() for _ in range(self.length)]

    def propagate(self, signals):
        """
        Propagacja sygnałów stacji po medium.
        signals: lista (pozycja, symbol_stacji)
        Najpierw stacje nadające oznaczają swoje pozycje, potem sygnał rozprzestrzenia się na sąsiednie komórki.
        Kolizje ('X') powstają, gdy w jednej komórce pojawi się sygnał więcej niż jednej stacji.
        """
        # Oznacz źródła sygnału
        fresh_sources = set()
        for pos, symbol in signals:
            if 0 <= pos < self.length:
                if self.cells[pos] == '.' or self.cells[pos] == symbol:
                    self.cells[pos] = symbol
                    self.owners[pos].add(symbol)
                    fresh_sources.add((pos, symbol))
                else:
                    self.cells[pos] = 'X'
                    self.owners[pos].add(symbol)
        # Rozprzestrzenianie sygnału na sąsiednie komórki
        new_signals = []
        for i, c in enumerate(self.cells):
            if c not in ['.', 'X']:
                if i > 0 and self.cells[i-1] == '.':
                    new_signals.append((i-1, c))
                if i < self.length-1 and self.cells[i+1] == '.':
                    new_signals.append((i+1, c))
        for pos, symbol in new_signals:
            if self.cells[pos] == '.' or self.cells[pos] == symbol:
                self.cells[pos] = symbol
                self.owners[pos].add(symbol)
            else:
                self.cells[pos] = 'X'
                self.owners[pos].add(symbol)

    def __str__(self):
        return ''.join(self.cells)

# Funkcja wypisująca stan medium i stacji w danym kroku symulacji
def print_state(step, medium, stations):
    print(f"Krok {step:2d}: {medium}")
    info = []
    for s in stations:
        if s.state == 'sending':
            info.append(f"{chr(65+s.id)}: nadaje")
        elif s.state == 'backoff':
            info.append(f"{chr(65+s.id)}: backoff({s.backoff})")
        else:
            info.append(f"{chr(65+s.id)}: czeka")
    print('  ' + ', '.join(info))

# Główna funkcja symulacji CSMA/CD
# Pobiera parametry z linii poleceń: liczba stacji, długość łącza, liczba kroków
# Rozmieszcza stacje, uruchamia pętlę symulacji i wypisuje wyniki

def main():
    if len(sys.argv) != 4:
        print("Użycie: python3 csma_cd.py <liczba_stacji> <długość_łącza> <liczba_kroków>")
        return
    n_stations = int(sys.argv[1])
    length = int(sys.argv[2])
    steps = int(sys.argv[3])
    random.seed(42)
    # Rozmieszczenie stacji równomiernie na łączu
    positions = [int(i*length/(n_stations+1)) for i in range(1, n_stations+1)]
    stations = [Station(pos, i) for i, pos in enumerate(positions)]
    medium = Medium(length)
    for step in range(steps):
        signals = []
        # Faza 1: decyzja o nadawaniu i zbieranie sygnałów (bez aktualizacji backoff)
        for s in stations:
            if s.state == 'backoff':
                continue  # Stacja w backoff nie nadaje
            if s.state == 'idle' and random.random() < 0.2:
                s.state = 'sending'
                s.tx_timer = 5  # transmisja trwa 5 kroków
            if s.state == 'sending':
                # Sygnał stacji pojawia się na jej pozycji
                signals.append((s.pos, chr(65+s.id)))
        # Faza 2: propagacja sygnałów po medium
        medium.propagate(signals)
        # Faza 3: wykrywanie kolizji
        # Znajdź wszystkie pozycje z kolizją
        collision_positions = set(i for i, c in enumerate(medium.cells) if c == 'X')
        # Zbierz symbole stacji, które brały udział w kolizji
        collided_symbols = set()
        for pos in collision_positions:
            collided_symbols.update(medium.owners[pos])
        for s in stations:
            if s.state == 'sending':
                if chr(65+s.id) in collided_symbols:
                    print(f"  [!] Kolizja: stacja {chr(65+s.id)} wykryła kolizję (jej sygnał brał udział) i przechodzi do backoff.")
                    s.state = 'backoff'
                    s.backoff = random.randint(1, 5)
                    s.tx_timer = 0
        # Po obsłudze kolizji: wyczyść sygnały stacji, które przeszły do backoff
        for s in stations:
            if s.state == 'backoff':
                symbol = chr(65+s.id)
                for i in range(medium.length):
                    if symbol in medium.owners[i]:
                        medium.owners[i].discard(symbol)
                        # Jeśli po usunięciu nie ma już właścicieli, wyczyść komórkę
                        if not medium.owners[i]:
                            medium.cells[i] = '.'
                        # Jeśli była kolizja, ale już tylko jeden właściciel, przywróć symbol
                        elif medium.cells[i] == 'X' and len(medium.owners[i]) == 1:
                            medium.cells[i] = list(medium.owners[i])[0]
        # Faza 4: wypisanie stanu przed aktualizacją liczników backoff i tx_timer
        print_state(step, medium, stations)
        # Faza 5: aktualizacja liczników backoff i tx_timer
        for s in stations:
            if s.state == 'backoff':
                s.backoff -= 1
                if s.backoff <= 0:
                    s.state = 'idle'
            elif s.state == 'sending':
                s.tx_timer -= 1
                if s.tx_timer <= 0:
                    s.state = 'idle'

if __name__ == "__main__":
    main()
