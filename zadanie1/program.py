#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
program.py - Kodowanie i dekodowanie ramek z sumą kontrolną CRC, bit stuffingiem i flagami.
Program realizuje ramkowanie, rozpychanie bitów, dodawanie i weryfikację CRC oraz obsługę plików wejściowych/wyjściowych.
"""

import sys

class FrameProcessor:
    def __init__(self):
        # Ustawienia długości ramki i CRC
        self.FRAME_LENGTH = 150  # liczba bitów danych w ramce
        self.CRC_POLY = "100000111"  # wielomian CRC-8 (x^8 + x^2 + x + 1)
        self.CRC_LENGTH = len(self.CRC_POLY) - 1
        self.FLAG = "01111110"  # flaga początku/końca ramki

    def calculate_crc(self, data_bits):
        """
        Oblicza sumę kontrolną CRC-8 dla podanego ciągu bitów (jako string '0'/'1').
        Zwraca resztę z dzielenia modulo 2 (jako string bitów).
        """
        # Dodajemy zera na końcu (długość wielomianu - 1)
        dividend = data_bits + "0" * (len(self.CRC_POLY) - 1)
        divisor = self.CRC_POLY
        
        # Konwertujemy na listy dla łatwiejszej manipulacji
        dividend_list = list(dividend)
        divisor_list = list(divisor)
        
        # Wykonujemy dzielenie modulo 2 (XOR)
        for i in range(len(data_bits)):
            if dividend_list[i] == '1':
                # XOR z wielomianem
                for j in range(len(divisor_list)):
                    if i + j < len(dividend_list):
                        dividend_list[i + j] = str(int(dividend_list[i + j]) ^ int(divisor_list[j]))
        
        # Reszta to ostatnie (len(divisor) - 1) bitów
        remainder = ''.join(dividend_list[-(len(divisor_list) - 1):])
        return remainder
    
    def verify_crc(self, data_with_crc):
        """
        Weryfikuje poprawność CRC dla danych z dołączonym polem CRC.
        Zwraca True, jeśli suma kontrolna jest poprawna.
        """
        if len(data_with_crc) < self.CRC_LENGTH:
            return False
        
        # Oblicz CRC dla całych danych (z dołączonym CRC powinno dać 0)
        remainder = self.calculate_crc(data_with_crc)
        return remainder == "0" * self.CRC_LENGTH
    
    def bit_stuff(self, bits):
        """
        Realizuje rozpychanie bitów: po każdych 5 jedynkach wstawia zero.
        Zwraca nowy ciąg bitów jako string.
        """
        result = ""
        count_ones = 0
        
        for bit in bits:
            result += bit
            if bit == '1':
                count_ones += 1
                if count_ones == 5:
                    result += '0'  # Wstawiamy zero po 5 jedynkach
                    count_ones = 0
            else:
                count_ones = 0
        
        return result
    
    def bit_unstuff(self, bits):
        """
        Usuwa rozpychanie bitów: po każdych 5 jedynkach usuwa następujące zero.
        Zwraca odtworzony ciąg bitów jako string.
        """
        result = ""
        count_ones = 0
        i = 0
        
        while i < len(bits):
            bit = bits[i]
            result += bit
            
            if bit == '1':
                count_ones += 1
                if count_ones == 5:
                    # Następny bit powinien być zerem do usunięcia
                    if i + 1 < len(bits) and bits[i + 1] == '0':
                        i += 1  # Pomijamy wstawione zero
                    count_ones = 0
            else:
                count_ones = 0
            
            i += 1
        
        return result
    
    def create_frame(self, data_chunk):
        """
        Tworzy ramkę z podanego fragmentu danych
        """
        if not data_chunk:
            return ""
        
        # 1. Oblicz CRC
        crc = self.calculate_crc(data_chunk)
        
        # 2. Połącz dane z CRC
        data_with_crc = data_chunk + crc
        
        # 3. Zastosuj bit stuffing
        stuffed_data = self.bit_stuff(data_with_crc)
        
        # 4. Dodaj flagi
        frame = self.FLAG + stuffed_data + self.FLAG
        
        return frame
    
    def encode_file(self, input_file, output_file):
        """
        Koduje plik wejściowy do ramek z CRC, rozpychaniem bitów i flagami.
        Zapisuje wynik do pliku wyjściowego jako jeden ciąg 0 i 1 (bez nowych linii).
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = f.read().strip()
            
            # Sprawdź czy dane zawierają tylko 0 i 1
            if not all(c in '01' for c in data):
                raise ValueError("Plik źródłowy musi zawierać tylko znaki '0' i '1'")
            
            frames = []
            
            # Podziel dane na fragmenty
            for i in range(0, len(data), self.FRAME_LENGTH):
                chunk = data[i:i+self.FRAME_LENGTH]
                frame = self.create_frame(chunk)
                frames.append(frame)
            
            # Połącz wszystkie ramki w jeden ciąg
            output_bits = ''.join(frames)
            
            # Zapisz do pliku jako jeden ciąg 0 i 1
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_bits)
            
            print(f"Kodowanie zakończone. Utworzono {len(frames)} ramek.")
            print(f"Wynik zapisano do: {output_file}")
        
        except FileNotFoundError:
            print(f"Błąd: Nie można odnaleźć pliku '{input_file}'")
        except Exception as e:
            print(f"Błąd podczas kodowania: {e}")
    
    def extract_frame_data(self, frame):
        """
        Wyciąga dane z ramki i weryfikuje je
        """
        # Usuń flagi
        if not (frame.startswith(self.FLAG) and frame.endswith(self.FLAG)):
            return None, "Nieprawidłowe flagi ramki"
        
        content = frame[len(self.FLAG):-len(self.FLAG)]
        
        if not content:
            return None, "Pusta ramka"
        
        # Usuń bit stuffing
        try:
            destuffed = self.bit_unstuff(content)
        except Exception as e:
            return None, f"Błąd podczas usuwania bit stuffing: {e}"
        
        if len(destuffed) < self.CRC_LENGTH:
            return None, "Ramka zbyt krótka"
        
        # Weryfikuj CRC
        if not self.verify_crc(destuffed):
            return None, "Błędne CRC"
        
        # Zwróć dane bez CRC
        data = destuffed[:-self.CRC_LENGTH]
        return data, "OK"
    
    def decode_file(self, input_file, output_file):
        """
        Dekoduje plik ramek: wyszukuje ramki na podstawie flag, usuwa flagi, rozpychanie bitów, weryfikuje CRC.
        Zapisuje poprawne dane do pliku wyjściowego.
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                bitstream = f.read().strip()

            decoded_data = ""
            valid_frames = 0
            total_frames = 0
            flag = self.FLAG
            flag_len = len(flag)
            i = 0
            frames_found = 0
            # Szukaj ramek na podstawie flag
            while i < len(bitstream):
                # Szukaj początku ramki
                start = bitstream.find(flag, i)
                if start == -1:
                    break
                end = bitstream.find(flag, start + flag_len)
                if end == -1:
                    break
                frame = bitstream[start:end+flag_len]
                frames_found += 1
                total_frames += 1
                data, status = self.extract_frame_data(frame)
                if data is not None:
                    decoded_data += data
                    valid_frames += 1
                    print(f"Ramka {frames_found}: OK")
                else:
                    print(f"Ramka {frames_found}: BŁĄD - {status}")
                i = end + flag_len

            if valid_frames > 0:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(decoded_data)
                print(f"\nDekodowanie zakończone.")
                print(f"Prawidłowych ramek: {valid_frames}/{total_frames}")
                print(f"Wynik zapisano do: {output_file}")
            else:
                print("Brak prawidłowych ramek do zdekodowania.")
        except FileNotFoundError:
            print(f"Błąd: Nie można odnaleźć pliku '{input_file}'")
        except Exception as e:
            print(f"Błąd podczas dekodowania: {e}")

if __name__ == "__main__":
    # Obsługa argumentów wiersza poleceń
    if len(sys.argv) < 4:
        print("Użycie: python3 program.py encode|decode <plik_wejściowy> <plik_wyjściowy>")
        sys.exit(1)
    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    processor = FrameProcessor()
    if mode == "encode":
        processor.encode_file(input_file, output_file)
        print(f"Zakodowano plik {input_file} do {output_file}")
    elif mode == "decode":
        processor.decode_file(input_file, output_file)
        print(f"Zdekodowano plik {input_file} do {output_file}")
    else:
        print("Nieznany tryb. Użyj 'encode' lub 'decode'.")