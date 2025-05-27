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

class Station:
    def __init__(self, pos, id):
        self.pos = pos
        self.id = id
        self.state = 'idle'  # 'idle', 'sending', 'backoff'
        self.backoff = 0
        self.collision = False

class Medium:
    def __init__(self, length):
        self.length = length
        self.cells = ['.'] * length  # '.' = cisza, 'A','B',... = sygnał stacji, 'X' = kolizja

    def clear(self):
        self.cells = ['.'] * self.length

    def propagate(self, signals):
        """
        signals: lista (pos, symbol)
        propaguje sygnały do sąsiednich komórek
        """
        for pos, symbol in signals:
            if 0 <= pos < self.length:
                if self.cells[pos] == '.' or self.cells[pos] == symbol:
                    self.cells[pos] = symbol
                else:
                    self.cells[pos] = 'X'  # kolizja
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
            else:
                self.cells[pos] = 'X'

    def __str__(self):
        return ''.join(self.cells)

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

def main():
    if len(sys.argv) != 4:
        print("Użycie: python3 csma_cd.py <liczba_stacji> <długość_łącza> <liczba_kroków>")
        return
    n_stations = int(sys.argv[1])
    length = int(sys.argv[2])
    steps = int(sys.argv[3])
    random.seed(42)
    # Rozmieść stacje równomiernie
    positions = [int(i*length/(n_stations+1)) for i in range(1, n_stations+1)]
    stations = [Station(pos, i) for i, pos in enumerate(positions)]
    medium = Medium(length)
    for step in range(steps):
        medium.clear()
        # 1. Stacje decydują o nadawaniu
        signals = []
        for s in stations:
            if s.state == 'backoff':
                s.backoff -= 1
                if s.backoff <= 0:
                    s.state = 'idle'
                continue
            if s.state == 'idle' and random.random() < 0.1:
                s.state = 'sending'
            if s.state == 'sending':
                signals.append((s.pos, chr(65+s.id)))
        # 2. Propagacja sygnałów
        medium.propagate(signals)
        # 3. Kolizje i wykrywanie
        for s in stations:
            if s.state == 'sending':
                if medium.cells[s.pos] == 'X':
                    s.state = 'backoff'
                    s.backoff = random.randint(1, 5)
        print_state(step, medium, stations)

if __name__ == "__main__":
    main()
