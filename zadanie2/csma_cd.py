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
        self.cells = ['.'] * length
        self.owners = [set() for _ in range(length)]
        self.wavefronts = []  # lista aktywnych czoł sygnałów: (pos, symbol, kierunek)

    def clear(self):
        self.cells = ['.'] * self.length
        self.owners = [set() for _ in range(self.length)]
        self.wavefronts = []

    def start_transmission(self, stations):
        # Dodaj nowe czoła sygnałów dla stacji, które zaczynają nadawać
        for s in stations:
            if s.state == 'sending':
                self.wavefronts.append((s.pos, chr(65+s.id), 0))  # 0 = źródło

    def propagate(self):
        # Nowa lista czoł sygnałów na kolejny krok
        new_wavefronts = []
        # Zaznacz sygnały w medium
        for pos, symbol, _ in self.wavefronts:
            if 0 <= pos < self.length:
                self.owners[pos].add(symbol)
        # Wykryj kolizje i ustaw symbole w medium
        for i in range(self.length):
            if len(self.owners[i]) > 1:
                self.cells[i] = 'X'
            elif len(self.owners[i]) == 1:
                self.cells[i] = list(self.owners[i])[0]
            else:
                self.cells[i] = '.'
        # Rozszerz czoła sygnałów na sąsiednie komórki
        for pos, symbol, direction in self.wavefronts:
            if direction == 0:
                # Rozchodzenie się od źródła w obie strony
                if pos > 0:
                    new_wavefronts.append((pos-1, symbol, -1))
                if pos < self.length-1:
                    new_wavefronts.append((pos+1, symbol, 1))
            elif direction == -1 and pos > 0:
                new_wavefronts.append((pos-1, symbol, -1))
            elif direction == 1 and pos < self.length-1:
                new_wavefronts.append((pos+1, symbol, 1))
        self.wavefronts = new_wavefronts

    def remove_symbol(self, symbol):
        # Usuwa sygnał danej stacji z medium i czoła sygnałów
        self.wavefronts = [w for w in self.wavefronts if w[1] != symbol]
        for i in range(self.length):
            if symbol in self.owners[i]:
                self.owners[i].discard(symbol)
                if not self.owners[i]:
                    self.cells[i] = '.'
                elif self.cells[i] == 'X' and len(self.owners[i]) == 1:
                    self.cells[i] = list(self.owners[i])[0]

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
        # Faza 1: decyzja o nadawaniu
        for s in stations:
            if s.state == 'backoff':
                continue
            if s.state == 'idle' and random.random() < 0.2:
                s.state = 'sending'
                s.tx_timer = 5
        # Faza 2: rozpoczęcie transmisji (dodanie nowych czoł sygnałów)
        medium.start_transmission(stations)
        # Faza 3: propagacja sygnałów o jeden krok
        medium.propagate()
        # Faza 4: wykrywanie kolizji
        collision_symbols = set()
        for i in range(medium.length):
            if medium.cells[i] == 'X':
                collision_symbols.update(medium.owners[i])
        for s in stations:
            if s.state == 'sending' and chr(65+s.id) in collision_symbols:
                print(f"  [!] Kolizja: stacja {chr(65+s.id)} wykryła kolizję (jej sygnał brał udział) i przechodzi do backoff.")
                s.state = 'backoff'
                s.backoff = random.randint(1, 5)
                s.tx_timer = 0
                medium.remove_symbol(chr(65+s.id))
        # Faza 5: wypisanie stanu
        print_state(step, medium, stations)
        # Faza 6: aktualizacja liczników
        for s in stations:
            if s.state == 'backoff':
                s.backoff -= 1
                if s.backoff <= 0:
                    s.state = 'idle'
            elif s.state == 'sending':
                s.tx_timer -= 1
                if s.tx_timer <= 0:
                    s.state = 'idle'
                    medium.remove_symbol(chr(65+s.id))

if __name__ == "__main__":
    main()
