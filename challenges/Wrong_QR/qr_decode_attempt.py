#!/usr/bin/env python3

import os

def analyze_qr_raw_data():
    """Try to extract QR data without external libraries"""
    
    file1 = "binary_qr_code1(2).png"
    file2 = "binary_qr_code(2).png"
    
    print("=== QR Code Raw Data Analysis ===")
    
    # Read both files
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    print(f"File 1 size: {len(data1)} bytes")
    print(f"File 2 size: {len(data2)} bytes")
    
    # Look for text chunks in PNG files (tEXt, iTXt, zTXt)
    def find_text_chunks(data, filename):
        print(f"\n=== Text chunks in {filename} ===")
        i = 0
        found_text = False
        while i < len(data) - 4:
            if data[i:i+4] == b'tEXt':
                found_text = True
                # Find the next chunk or end
                chunk_start = i - 4  # Length is 4 bytes before tEXt
                if chunk_start >= 0:
                    chunk_len = int.from_bytes(data[chunk_start:chunk_start+4], 'big')
                    chunk_data = data[i+4:i+4+chunk_len]
                    print(f"tEXt chunk: {chunk_data}")
            elif data[i:i+4] == b'iTXt':
                found_text = True
                chunk_start = i - 4
                if chunk_start >= 0:
                    chunk_len = int.from_bytes(data[chunk_start:chunk_start+4], 'big')
                    chunk_data = data[i+4:i+4+chunk_len]
                    print(f"iTXt chunk: {chunk_data}")
            elif data[i:i+4] == b'zTXt':
                found_text = True
                chunk_start = i - 4
                if chunk_start >= 0:
                    chunk_len = int.from_bytes(data[chunk_start:chunk_start+4], 'big')
                    chunk_data = data[i+4:i+4+chunk_len]
                    print(f"zTXt chunk: {chunk_data}")
            i += 1
        
        if not found_text:
            print("No text chunks found")
    
    find_text_chunks(data1, file1)
    find_text_chunks(data2, file2)
    
    # Look for ASCII strings in the raw data
    def find_ascii_strings(data, filename, min_len=4):
        print(f"\n=== ASCII strings in {filename} (min length {min_len}) ===")
        current_string = ""
        strings = []
        
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) >= min_len:
                    strings.append(current_string)
                current_string = ""
        
        if len(current_string) >= min_len:
            strings.append(current_string)
        
        for s in strings:
            if len(s) >= min_len:
                print(f"  {s}")
        
        return strings
    
    strings1 = find_ascii_strings(data1, file1)
    strings2 = find_ascii_strings(data2, file2)
    
    # Look for differences in strings
    print("\n=== String differences ===")
    set1 = set(strings1)
    set2 = set(strings2)
    
    unique_to_1 = set1 - set2
    unique_to_2 = set2 - set1
    
    if unique_to_1:
        print(f"Unique to {file1}:")
        for s in unique_to_1:
            print(f"  {s}")
    
    if unique_to_2:
        print(f"Unique to {file2}:")
        for s in unique_to_2:
            print(f"  {s}")
    
    # Try to find flag-like patterns
    print("\n=== Looking for flag patterns ===")
    all_strings = strings1 + strings2
    for s in all_strings:
        if 'flag' in s.lower() or 'FLAG' in s or '{' in s or '}' in s:
            print(f"Potential flag string: {s}")
    
    # Look at the XOR differences again but try different interpretations
    print("\n=== Alternative XOR interpretations ===")
    
    # Calculate XOR differences
    xor_data = bytes(a ^ b for a, b in zip(data1, data2))
    non_zero_xor = bytes(x for x in xor_data if x != 0)
    
    print(f"Non-zero XOR bytes: {len(non_zero_xor)}")
    
    # Try interpreting as different encodings
    try:
        # Try as Latin-1 (single byte encoding)
        latin1_text = non_zero_xor.decode('latin-1')
        print(f"Latin-1 interpretation: {repr(latin1_text)}")
        
        # Look for flag patterns in Latin-1
        if '[REDACTED]")
    except:
        pass
    
    # Try looking at specific byte positions that might encode data
    print("\n=== Checking specific byte patterns ===")
    
    # Look for repeating patterns in the XOR data
    xor_hex = non_zero_xor.hex()
    print(f"XOR hex (first 100 chars): {xor_hex[:100]}")
    
    # Try grouping bytes differently
    for group_size in [2, 4, 8]:
        print(f"\nGrouped by {group_size} bytes:")
        groups = [non_zero_xor[i:i+group_size] for i in range(0, len(non_zero_xor), group_size)]
        for i, group in enumerate(groups[:10]):  # Show first 10 groups
            hex_val = group.hex()
            try:
                ascii_val = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in group)
                print(f"  Group {i}: {hex_val} -> {ascii_val}")
            except:
                print(f"  Group {i}: {hex_val}")

if __name__ == "__main__":
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Wrong_QR")
    analyze_qr_raw_data()
