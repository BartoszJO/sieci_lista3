#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py - uruchamia zestaw testów dla symulacji CSMA/CD (csma_cd.py) z zadania 2.
Każdy test uruchamia symulację z określoną liczbą stacji, długością łącza i liczbą kroków.
Wyniki są wypisywane na konsolę.
"""
import subprocess

# Funkcja uruchamia pojedynczy test z zadanymi parametrami
def run_test(n_stations, length, steps):
    print(f"\n=== Test: stacje={n_stations}, dlugosc={length}, kroki={steps} ===")
    result = subprocess.run([
        'python3', 'csma_cd.py', str(n_stations), str(length), str(steps)
    ], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("BŁĄD:", result.stderr)

# Główna funkcja uruchamiająca wszystkie testy
def main():
    test_cases = [
        (2, 10, 10),   # 2 stacje, długość 10, 10 kroków
        (3, 20, 15),   # 3 stacje, długość 20, 15 kroków
        (4, 30, 20),   # 4 stacje, długość 30, 20 kroków
        (5, 15, 12),   # 5 stacji, długość 15, 12 kroków
    ]
    for n, l, s in test_cases:
        run_test(n, l, s)

if __name__ == "__main__":
    main()
