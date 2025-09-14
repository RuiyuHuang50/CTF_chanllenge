#!/usr/bin/env python3

import os

def ultimate_flag_search():
    """Ultimate flag search - try all possible encodings"""
    
    file1 = "binary_qr_code1(2).png"
    file2 = "binary_qr_code(2).png"
    
    print("=== Ultimate Flag Search ===")
    
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    # Get XOR differences
    xor_data = bytes(a ^ b for a, b in zip(data1, data2))
    non_zero_xor = bytes(x for x in xor_data if x != 0)
    
    print(f"XOR differences: {len(non_zero_xor)} bytes")
    
    # Try the unique string "Pv$4d" in different ways
    unique_string = "Pv$4d"
    print(f"\n=== Analysis of unique string: {unique_string} ===")
    
    # ROT13 and other Caesar shifts
    def apply_caesar(text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char
        return result
    
    print("Caesar cipher attempts:")
    for shift in range(1, 26):
        decoded = apply_caesar(unique_string, shift)
        print(f"  Shift {shift:2d}: {decoded}")
        if 'FLAG' in decoded.upper():
            print(f"    🎯 Potential match!")
    
    # Try interpreting the hex values differently
    print(f"\n=== Hex interpretation of 'Pv$4d' ===")
    hex_vals = [hex(ord(c)) for c in unique_string]
    print(f"Hex values: {hex_vals}")
    
    # Try the XOR data with different interpretations
    print(f"\n=== Advanced XOR interpretations ===")
    
    # Group bytes and try as ASCII
    xor_hex = non_zero_xor.hex()
    
    # Try reading as hex pairs interpreted as ASCII
    ascii_from_hex = ""
    for i in range(0, len(xor_hex), 2):
        if i + 1 < len(xor_hex):
            hex_pair = xor_hex[i:i+2]
            try:
                val = int(hex_pair, 16)
                if 32 <= val <= 126:
                    ascii_from_hex += chr(val)
                else:
                    ascii_from_hex += '.'
            except:
                ascii_from_hex += '.'
    
    print(f"Hex pairs as ASCII: {ascii_from_hex}")
    
    if '[REDACTED]")
    
    # Try interpreting specific patterns
    # Look for "FLAG" pattern in different representations
    flag_pattern = "FLAG"
    flag_hex = ''.join(hex(ord(c))[2:] for c in flag_pattern)
    print(f"FLAG pattern in hex: {flag_hex}")
    
    if flag_hex in xor_hex.lower():
        pos = xor_hex.lower().find(flag_hex)
        print(f"Found FLAG pattern at hex position {pos}")
        
        # Extract surrounding context
        context_start = max(0, pos - 10)
        context_end = min(len(xor_hex), pos + 50)
        context = xor_hex[context_start:context_end]
        print(f"Context: {context}")
    
    # Try bit manipulation on the unique string
    print(f"\n=== Bit manipulation of unique string ===")
    unique_bytes = [ord(c) for c in unique_string]
    print(f"Decimal values: {unique_bytes}")
    
    # XOR with different values
    for xor_val in [1, 16, 32, 64, 128]:
        xor_result = [b ^ xor_val for b in unique_bytes]
        xor_string = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in xor_result)
        print(f"XOR with {xor_val:3d}: {xor_string}")
        
        if 'FLAG' in xor_string.upper():
            print(f"    🎯 Found FLAG with XOR {xor_val}!")
    
    # Try concatenating the unique string with other data
    print(f"\n=== String concatenation attempts ===")
    
    # Maybe the flag is split across the differences
    # Try taking characters at specific intervals from XOR data
    for interval in [5, 7, 8, 13, 16]:
        chars = []
        for i in range(0, len(non_zero_xor), interval):
            if i < len(non_zero_xor):
                byte = non_zero_xor[i]
                if 32 <= byte <= 126:
                    chars.append(chr(byte))
        
        if chars:
            result = ''.join(chars)
            print(f"Every {interval:2d}th char: {result}")
            
            if 'FLAG' in result.upper():
                print(f"    🎯 Found FLAG with interval {interval}!")
    
    # Last resort - try interpreting the raw XOR data in chunks
    print(f"\n=== Chunk analysis ===")
    
    # Try 4-byte chunks as little-endian integers, then as ASCII
    for chunk_size in [4, 8]:
        print(f"Analyzing {chunk_size}-byte chunks:")
        for i in range(0, len(non_zero_xor) - chunk_size + 1, chunk_size):
            chunk = non_zero_xor[i:i+chunk_size]
            
            # Try as integer
            try:
                int_val = int.from_bytes(chunk, 'little')
                ascii_attempt = ''.join(chr((int_val >> (8*j)) & 0xFF) 
                                      for j in range(chunk_size) 
                                      if 32 <= ((int_val >> (8*j)) & 0xFF) <= 126)
                
                if len(ascii_attempt) >= 2:
                    print(f"  Chunk {i//chunk_size}: {ascii_attempt}")
                    
                    if 'FLAG' in ascii_attempt.upper():
                        print(f"    🎯 Found FLAG in chunk {i//chunk_size}!")
            except:
                pass
    
    print(f"\n=== Final attempt: manual inspection ===")
    print("XOR data broken into readable chunks:")
    
    # Show XOR data in a more readable format
    for i in range(0, len(non_zero_xor), 16):
        chunk = non_zero_xor[i:i+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        print(f"{i:3d}: {hex_str:<48} | {ascii_str}")

if __name__ == "__main__":
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Wrong_QR")
    ultimate_flag_search()
