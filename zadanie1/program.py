#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program ramkowania z zasadą "rozpychania bitów" i weryfikacją CRC
"""

import sys
import os

class FrameProcessor:
    def __init__(self):
        # Wzorzec ramki - flaga początkowa i końcowa
        self.FLAG = "01111110"
        # Wielomian CRC-8: x^8 + x^2 + x^1 + 1 = 100000111
        self.CRC_POLY = "100000111"
        self.CRC_LENGTH = 8
    
    def calculate_crc(self, data_bits):
        """
        Oblicza CRC dla podanych bitów danych
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
    
    def bit_stuffing(self, data):
        """
        Implementuje zasadę rozpychania bitów
        Po pięciu kolejnych jedynkach wstawia zero
        """
        result = ""
        count_ones = 0
        
        for bit in data:
            result += bit
            if bit == '1':
                count_ones += 1
                if count_ones == 5:
                    result += '0'  # Wstawiamy zero po 5 jedynkach
                    count_ones = 0
            else:
                count_ones = 0
        
        return result
    
    def bit_destuffing(self, data):
        """
        Usuwa bity wstawione podczas bit stuffing
        """
        result = ""
        count_ones = 0
        i = 0
        
        while i < len(data):
            bit = data[i]
            result += bit
            
            if bit == '1':
                count_ones += 1
                if count_ones == 5:
                    # Następny bit powinien być zerem do usunięcia
                    if i + 1 < len(data) and data[i + 1] == '0':
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
        stuffed_data = self.bit_stuffing(data_with_crc)
        
        # 4. Dodaj flagi
        frame = self.FLAG + stuffed_data + self.FLAG
        
        return frame
    
    def encode_file(self, input_file, output_file, chunk_size=64):
        """
        Koduje plik źródłowy do ramek
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = f.read().strip()
            
            # Sprawdź czy dane zawierają tylko 0 i 1
            if not all(c in '01' for c in data):
                raise ValueError("Plik źródłowy musi zawierać tylko znaki '0' i '1'")
            
            frames = []
            
            # Podziel dane na fragmenty
            for i in range(0, len(data), chunk_size):
                chunk = data[i:i+chunk_size]
                frame = self.create_frame(chunk)
                frames.append(frame)
            
            # Zapisz ramki do pliku
            with open(output_file, 'w', encoding='utf-8') as f:
                for frame in frames:
                    f.write(frame + '\n')
            
            print(f"Kodowanie zakończone. Utworzono {len(frames)} ramek.")
            print(f"Wynik zapisano do: {output_file}")
            
        except FileNotFoundError:
            print(f"Błąd: Nie można odnaleźć pliku '{input_file}'")
        except Exception as e:
            print(f"Błąd podczas kodowania: {e}")
    
    def verify_crc(self, data_with_crc):
        """
        Weryfikuje poprawność CRC
        """
        if len(data_with_crc) < self.CRC_LENGTH:
            return False
        
        # Oblicz CRC dla całych danych (z dołączonym CRC powinno dać 0)
        remainder = self.calculate_crc(data_with_crc)
        return remainder == "0" * self.CRC_LENGTH
    
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
            destuffed = self.bit_destuffing(content)
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
        Dekoduje plik z ramkami
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            decoded_data = ""
            valid_frames = 0
            total_frames = 0
            
            for line_num, line in enumerate(lines, 1):
                frame = line.strip()
                if not frame:
                    continue
                
                total_frames += 1
                data, status = self.extract_frame_data(frame)
                
                if data is not None:
                    decoded_data += data
                    valid_frames += 1
                    print(f"Ramka {line_num}: OK")
                else:
                    print(f"Ramka {line_num}: BŁĄD - {status}")
            
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

def main():
    processor = FrameProcessor()
    
    if len(sys.argv) < 2:
        print("Użycie:")
        print(f"  {sys.argv[0]} encode <plik_źródłowy> <plik_wynikowy>")
        print(f"  {sys.argv[0]} decode <plik_ramek> <plik_wynikowy>")
        print("\nPrzykłady:")
        print(f"  {sys.argv[0]} encode Z.txt W.txt")
        print(f"  {sys.argv[0]} decode W.txt Z_decoded.txt")
        return
    
    command = sys.argv[1].lower()
    
    if command == "encode":
        if len(sys.argv) != 4:
            print("Błąd: Kodowanie wymaga dwóch argumentów - plik źródłowy i plik wynikowy")
            return
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        processor.encode_file(input_file, output_file)
        
    elif command == "decode":
        if len(sys.argv) != 4:
            print("Błąd: Dekodowanie wymaga dwóch argumentów - plik ramek i plik wynikowy")
            return
        
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        processor.decode_file(input_file, output_file)
        
    else:
        print(f"Nieznana komenda: {command}")
        print("Dostępne komendy: encode, decode")

if __name__ == "__main__":
    main()