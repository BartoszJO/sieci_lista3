import subprocess
import os
from termcolor import colored

# Paths
SCRIPT = 'program.py'
INPUT_FILE = 'test_input.txt'
ENCODED_FILE = 'test_encoded.txt'
DECODED_FILE = 'test_decoded.txt'

# Sample bit string (can be changed for more tests)
BIT_STRING = '01111110111111000001111110000011111' * 220  # purposely includes many 1s for stuffing

# Write input file
print(colored('\n--- INPUT DATA ---', 'cyan'))
print(BIT_STRING)
with open(INPUT_FILE, 'w') as f:
    f.write(BIT_STRING)

# Encode
subprocess.run(['python3', SCRIPT, 'encode', INPUT_FILE, ENCODED_FILE], check=True)

# Read and print encoded output with color
print(colored('\n--- ENCODED FRAMES ---', 'cyan'))
with open(ENCODED_FILE) as f:
    for line in f:
        frame = line.strip()
        # Highlight flag, CRC, and stuffed bits
        # Flag: 01111110
        if frame.startswith('01111110') and frame.endswith('01111110'):
            flag = '01111110'
            content = frame[len(flag):-len(flag)]
            # Color flags
            print(colored(flag, 'green'), end='')
            # Color stuffed zeros (after five 1s)
            i = 0
            ones = 0
            while i < len(content):
                bit = content[i]
                if bit == '1':
                    ones += 1
                    print(colored('1', 'yellow'), end='')
                    if ones == 5:
                        # Next bit should be stuffed zero
                        if i+1 < len(content) and content[i+1] == '0':
                            print(colored('0', 'red', attrs=['bold']), end='')
                            i += 1
                        ones = 0
                else:
                    print('0', end='')
                    ones = 0
                i += 1
            print(colored(flag, 'green'))
        else:
            print(frame)

# Decode
subprocess.run(['python3', SCRIPT, 'decode', ENCODED_FILE, DECODED_FILE], check=True)

# Read and print decoded output
with open(DECODED_FILE) as f:
    decoded = f.read().strip()

print(colored('\n--- DECODED DATA ---', 'cyan'))
print(decoded)

# Compare
if decoded == BIT_STRING:
    print(colored('\nSUCCESS: Decoded data matches original input!', 'green', attrs=['bold']))
else:
    print(colored('\nFAIL: Decoded data does NOT match original input!', 'red', attrs=['bold']))

# Cleanup (optional)
# os.remove(INPUT_FILE)
# os.remove(ENCODED_FILE)
# os.remove(DECODED_FILE)
