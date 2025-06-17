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
    bitstream = f.read().strip()
    flag = '01111110'
    flag_len = len(flag)
    i = 0
    frame_num = 1
    while i < len(bitstream):
        start = bitstream.find(flag, i)
        if start == -1:
            break
        end = bitstream.find(flag, start + flag_len)
        if end == -1:
            break
        frame = bitstream[start:end+flag_len]
        content = frame[len(flag):-len(flag)]
        print(colored(f'Frame {frame_num}: ', 'blue'), end='')
        print(colored(flag, 'green'), end='')
        # Color stuffed zeros (after five 1s)
        idx = 0
        ones = 0
        while idx < len(content):
            bit = content[idx]
            if bit == '1':
                ones += 1
                print(colored('1', 'yellow'), end='')
                if ones == 5:
                    # Next bit should be stuffed zero
                    if idx+1 < len(content) and content[idx+1] == '0':
                        print(colored('0', 'red', attrs=['bold']), end='')
                        idx += 1
                    ones = 0
            else:
                print('0', end='')
                ones = 0
            idx += 1
        print(colored(flag, 'green'))
        i = end + flag_len
        frame_num += 1

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
