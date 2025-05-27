#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py - uruchamia testy dla csma_cd.py z zadania2
"""
import subprocess

def run_test(n_stations, length, steps):
    print(f"\n=== Test: stacje={n_stations}, dlugosc={length}, kroki={steps} ===")
    result = subprocess.run([
        'python3', 'csma_cd.py', str(n_stations), str(length), str(steps)
    ], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("BŁĄD:", result.stderr)

def main():
    test_cases = [
        (2, 10, 10),
        (3, 20, 15),
        (4, 30, 20),
        (5, 15, 12),
    ]
    for n, l, s in test_cases:
        run_test(n, l, s)

if __name__ == "__main__":
    main()
