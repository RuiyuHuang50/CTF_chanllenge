#!/usr/bin/env python3

import os

def steganographic_analysis():
    """Try steganographic approaches to find the flag"""
    
    file1 = "binary_qr_code1(2).png"
    file2 = "binary_qr_code(2).png"
    
    print("=== Steganographic Analysis ===")
    
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    # Focus on the unique string "Pv$4d" that only appears in file2
    unique_string = b"Pv$4d"
    print(f"Unique string found: {unique_string}")
    print(f"As ASCII: {unique_string.decode('ascii')}")
    print(f"As hex: {unique_string.hex()}")
    
    # Maybe this string IS the flag or part of it
    # Let's see if we can find more context around it
    
    pos = data2.find(unique_string)
    if pos != -1:
        print(f"Found at position {pos}")
        
        # Get larger context
        start = max(0, pos - 50)
        end = min(len(data2), pos + 50)
        context = data2[start:end]
        
        print(f"Extended context ({len(context)} bytes):")
        print(f"Hex: {context.hex()}")
        
        # Look for readable strings in the context
        ascii_context = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in context)
        print(f"ASCII: {ascii_context}")
        
        # Maybe the flag is constructed from multiple parts
        # Let's look for other unique strings
        
    print(f"\n=== Looking for other unique patterns ===")
    
    # Find all positions where files differ
    diff_positions = []
    for i in range(min(len(data1), len(data2))):
        if data1[i] != data2[i]:
            diff_positions.append(i)
    
    print(f"Files differ at {len(diff_positions)} positions")
    
    # Extract bytes from both files at difference positions
    bytes1 = [data1[pos] for pos in diff_positions]
    bytes2 = [data2[pos] for pos in diff_positions]
    
    # Look for patterns in the differences
    diff_string1 = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in bytes1)
    diff_string2 = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in bytes2)
    
    print(f"Readable chars from file1 differences: {diff_string1}")
    print(f"Readable chars from file2 differences: {diff_string2}")
    
    # Try to find "FLAG" in either string
    if 'FLAG' in diff_string1.upper():
        print(f"🎯 FOUND FLAG in file1 differences!")
        # Find the exact position
        flag_pos = diff_string1.upper().find('FLAG')
        flag_context = diff_string1[flag_pos:flag_pos+30]
        print(f"Flag context: {flag_context}")
    
    if 'FLAG' in diff_string2.upper():
        print(f"🎯 FOUND FLAG in file2 differences!")
        flag_pos = diff_string2.upper().find('FLAG')
        flag_context = diff_string2[flag_pos:flag_pos+30]
        print(f"Flag context: {flag_context}")
    
    # Try the "Pv$4d" string with different interpretations
    print(f"\n=== Alternative interpretations of 'Pv$4d' ===")
    
    # Maybe it's encoded or needs transformation
    target = "Pv$4d"
    
    # Try base64-like interpretations
    # ASCII values: P=80, v=118, $=36, 4=52, d=100
    ascii_vals = [ord(c) for c in target]
    print(f"ASCII values: {ascii_vals}")
    
    # Try interpreting as hex digits where possible
    hex_attempt = ""
    for c in target:
        if c in '0123456789abcdefABCDEF':
            hex_attempt += c
    
    if hex_attempt:
        print(f"Hex digits found: {hex_attempt}")
        if len(hex_attempt) % 2 == 0:
            try:
                decoded = bytes.fromhex(hex_attempt)
                print(f"Hex decoded: {decoded}")
            except:
                pass
    
    # Try ROT variations
    def rot_decode(text, shift):
        result = ""
        for c in text:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                result += chr((ord(c) - base - shift) % 26 + base)
            else:
                result += c
        return result
    
    print(f"ROT transformations:")
    for shift in [13, 1, 25]:  # ROT13 and neighbors
        rotated = rot_decode(target, shift)
        print(f"  ROT{shift}: {rotated}")
        if 'FLAG' in rotated.upper():
            print(f"    🎯 Found FLAG with ROT{shift}!")
    
    # Final attempt - maybe the challenge wants us to manually decode the QR codes
    print(f"\n=== Final Manual Check ===")
    # Flag output removed for competition security
    print("the challenge might require:")
    print("1. Manually decoding each QR code using an online tool")
    print("2. Comparing the decoded text content")
    print("3. Finding the flag in the difference between the decoded messages")
    print()
    print("Files to check manually:")
    print("- qr1.png (copy of binary_qr_code1(2).png)")
    print("- qr2.png (copy of binary_qr_code(2).png)")
    print()
    print("Use an online QR decoder like https://zxing.org/w/decode.jsp")
    print("Upload each file and compare the decoded text.")

if __name__ == "__main__":
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Wrong_QR")
    steganographic_analysis()
