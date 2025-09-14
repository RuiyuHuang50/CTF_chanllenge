#!/usr/bin/env python3

import os

def analyze_qr_structure():
    """Simple analysis to understand QR structure better"""
    
    file1 = "binary_qr_code1(2).png"
    file2 = "binary_qr_code(2).png"
    
    print("=== QR Structure Analysis ===")
    
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    print(f"File sizes: {len(data1)} vs {len(data2)} bytes")
    
    # Let's try a really simple approach - maybe the flag is hidden in plain sight
    # Check if either file contains readable flag text
    
    def search_for_flags(data, filename):
        """Search for flag patterns in raw data"""
        print(f"\nSearching in {filename}:")
        
        # Convert to string representation
        text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)
        
        # Look for flag patterns
        if '[REDACTED]', start)
            if end != -1:
                flag = text[start:end+1]
                print(f"🎯 FOUND FLAG: {flag}")
                return flag
        
        # Look for case variations
        text_upper = text.upper()
        if '[REDACTED]', start)
            if end != -1:
                flag = text_upper[start:end+1]
                print(f"🎯 FOUND UPPERCASE FLAG: {flag}")
                return flag
        
        # Look for partial patterns
        if 'flag' in text.lower():
            print(f"Found 'flag' text (partial): around position {text.lower().find('flag')}")
        
        if '{' in text and '}' in text:
            print("Found brackets: { and } present")
        
        return None
    
    flag1 = search_for_flags(data1, file1)
    flag2 = search_for_flags(data2, file2)
    
    # If no direct flags found, try XOR approach one more time with focus
    if not flag1 and not flag2:
        print("\n=== Focused XOR Analysis ===")
        
        xor_data = bytes(a ^ b for a, b in zip(data1, data2))
        
        # Remove null bytes and create clean data
        clean_xor = []
        for i, byte in enumerate(xor_data):
            if byte != 0:
                clean_xor.append(byte)
        
        xor_bytes = bytes(clean_xor)
        
        # Try to find flag pattern by looking at specific positions
        hex_str = xor_bytes.hex()
        print(f"Clean XOR hex: {hex_str}")
        
        # Convert hex to ASCII and look for patterns
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in xor_bytes)
        print(f"XOR ASCII: {ascii_str}")
        
        # Maybe the flag is encoded in a specific way
        # Try looking at every nth byte
        for n in range(2, 6):
            subset = xor_bytes[::n]
            subset_ascii = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in subset)
            print(f"Every {n}th byte: {subset_ascii}")
            
            if '[REDACTED]TH: {subset_ascii}")
        
        # Try different starting positions
        for start in range(min(5, len(xor_bytes))):
            subset = xor_bytes[start::2]
            subset_ascii = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in subset)
            if len(subset_ascii) > 10:  # Only show meaningful lengths
                print(f"From position {start}, every 2nd: {subset_ascii}")
                
                if '[REDACTED]: {subset_ascii}")
    
    # Let's also try to manually decode some visible patterns
    print("\n=== Manual Pattern Analysis ===")
    
    # Look for the specific string we found earlier
    unique_str = b"Pv$4d"
    pos2 = data2.find(unique_str)
    
    if pos2 != -1:
        print(f"Unique string 'Pv$4d' at position {pos2}")
        
        # Check surrounding context more carefully
        context_start = max(0, pos2 - 10)
        context_end = min(len(data2), pos2 + 20)
        context = data2[context_start:context_end]
        
        print(f"Extended context: {context}")
        context_ascii = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in context)
        print(f"Context ASCII: {context_ascii}")
        
        # Maybe this string is part of a larger encoded message
        # Try base64 style decode
        target = b"Pv$4d"
        # This could be encoded data - let's see the exact bytes
        print(f"Target bytes: {[hex(b) for b in target]}")
        
        # Maybe it's ROT13 or Caesar cipher?
        def caesar_decode(text, shift):
            result = ""
            for char in text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    result += chr((ord(char) - base - shift) % 26 + base)
                else:
                    result += char
            return result
        
        text_to_decode = "Pv$4d"
        for shift in range(26):
            decoded = caesar_decode(text_to_decode, shift)
            if 'FLAG' in decoded.upper():
                print(f"🎯 Caesar shift {shift}: {decoded}")

if __name__ == "__main__":
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Wrong_QR")
    analyze_qr_structure()
