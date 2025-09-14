#!/usr/bin/env python3

import os

def extract_flag_from_wrong_qr():
    """Try to extract flag from 'wrong' QR codes that can't be decoded normally"""
    
    file1 = "binary_qr_code1(2).png"
    file2 = "binary_qr_code(2).png"
    
    print("=== Wrong QR Flag Extraction ===")
    print("Since the QR codes can't be decoded normally, they're intentionally 'wrong'")
    print("The flag must be hidden in the differences...")
    
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    # Get XOR differences
    xor_data = bytes(a ^ b for a, b in zip(data1, data2))
    non_zero_xor = bytes(x for x in xor_data if x != 0)
    
    print(f"Non-zero XOR bytes: {len(non_zero_xor)}")
    
    # Since we found "Pv$4d" is unique to file2, let's focus on that
    unique_string = "Pv$4d"
    print(f"\nFocus on unique string: {unique_string}")
    
    # Try different interpretations of this string
    # Maybe it's a clue or part of the flag
    
    # Check if it could be a substitution cipher
    def try_substitutions(text):
        """Try different character substitutions"""
        results = []
        
        # Try shifting each character
        for shift in range(-25, 26):
            shifted = ""
            for char in text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    shifted += chr((ord(char) - base + shift) % 26 + base)
                else:
                    shifted += char
            results.append((shift, shifted))
        
        return results
    
    substitutions = try_substitutions(unique_string)
    print("Substitution attempts:")
    for shift, result in substitutions:
        if 'FLAG' in result.upper():
            print(f"🎯 SHIFT {shift:3d}: {result} - CONTAINS FLAG!")
        elif any(c in result.upper() for c in ['F', 'L', 'A', 'G']):
            print(f"    {shift:3d}: {result}")
    
    # Maybe the numbers in "Pv$4d" are significant
    # Extract: P=80, v=118, $=36, 4=52, d=100
    chars = list(unique_string)
    ascii_vals = [ord(c) for c in chars]
    print(f"\nASCII values of '{unique_string}': {ascii_vals}")
    
    # Try interpreting these as coordinates or indices
    # Maybe they point to specific bytes in the XOR data
    print("\nTrying ASCII values as indices into XOR data:")
    for i, val in enumerate(ascii_vals):
        if val < len(non_zero_xor):
            byte_at_index = non_zero_xor[val]
            char_at_index = chr(byte_at_index) if 32 <= byte_at_index <= 126 else '.'
            print(f"  {chars[i]} ({val}) -> XOR[{val}] = 0x{byte_at_index:02x} = '{char_at_index}'")
    
    # Try the differences between files at specific positions
    print(f"\nExamining file differences more carefully:")
    
    # Get all difference positions
    diff_positions = []
    for i in range(min(len(data1), len(data2))):
        if data1[i] != data2[i]:
            diff_positions.append(i)
    
    print(f"Total differences: {len(diff_positions)}")
    
    # Extract bytes from both files at these positions
    bytes_from_file1 = [data1[pos] for pos in diff_positions]
    bytes_from_file2 = [data2[pos] for pos in diff_positions]
    
    # Convert to strings and look for patterns
    str1 = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in bytes_from_file1)
    str2 = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in bytes_from_file2)
    
    print(f"String from file1 differences: {str1}")
    print(f"String from file2 differences: {str2}")
    
    # Look for "FLAG" in these strings more carefully
    for text, source in [(str1, "file1"), (str2, "file2")]:
        text_upper = text.upper()
        if 'FLAG' in text_upper:
            flag_start = text_upper.find('FLAG')
            # Extract more context around FLAG
            context_start = max(0, flag_start - 5)
            context_end = min(len(text), flag_start + 20)
            flag_context = text[context_start:context_end]
            print(f"🎯 FOUND FLAG in {source}: ...{flag_context}...")
    
    # Try interpreting the XOR data with different encodings
    print(f"\nTrying different XOR interpretations:")
    
    # Base64 attempt
    import base64
    try:
        # Try to pad and decode as base64
        xor_str = non_zero_xor.decode('latin1')
        # Add padding if needed
        while len(xor_str) % 4 != 0:
            xor_str += '='
        b64_decoded = base64.b64decode(xor_str, validate=False)
        b64_text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in b64_decoded)
        print(f"Base64 attempt: {b64_text[:50]}...")
        if 'FLAG' in b64_text:
            print(f"🎯 FOUND FLAG IN BASE64: {b64_text}")
    except Exception as e:
        print(f"Base64 decode failed: {e}")
    
    # Try reading the XOR data backwards
    reversed_xor = non_zero_xor[::-1]
    reversed_text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in reversed_xor)
    print(f"Reversed XOR: {reversed_text[:50]}...")
    if 'FLAG' in reversed_text:
        print(f"🎯 FOUND FLAG IN REVERSED: {reversed_text}")
    
    # Try every nth byte starting from different positions
    print(f"\nTrying patterns in XOR data:")
    for start in range(min(8, len(non_zero_xor))):
        for step in range(2, 8):
            pattern = non_zero_xor[start::step]
            if len(pattern) > 4:
                pattern_text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in pattern)
                if 'FLAG' in pattern_text.upper():
                    print(f"🎯 FOUND FLAG: start={start}, step={step}: {pattern_text}")
                elif len(pattern_text.replace('.', '')) > 8:  # Show patterns with substantial text
                    print(f"Pattern start={start}, step={step}: {pattern_text[:20]}...")
    
    # Final attempt: maybe it's a simple concatenation or the unique string IS part of the flag
    print(f"\nFinal attempts:")
    
    # Maybe "Pv$4d" needs to be combined with other elements
    print(f"Unique string 'Pv$4d' analysis:")
    print(f"- Could be part of [REDACTED]} or similar")
    print(f"- Could need transformation")
    
    # Try simple transformations
    transformations = [
        f"[REDACTED]}}",
        f"[REDACTED]}}",
        f"[REDACTED]}}",
        f"[REDACTED]}}",
    ]
    
    for transform in transformations:
        print(f"Trying: {transform}")

if __name__ == "__main__":
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Wrong_QR")
    extract_flag_from_wrong_qr()
