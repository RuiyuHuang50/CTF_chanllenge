#!/usr/bin/env python3

import os

def final_flag_extraction():
    """Final attempt to extract the flag from QR differences"""
    
    file1 = "binary_qr_code1(2).png"
    file2 = "binary_qr_code(2).png"
    
    print("=== Final Flag Extraction Attempt ===")
    
    # Read both files
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    # Calculate full XOR
    full_xor = bytes(a ^ b for a, b in zip(data1, data2))
    
    # Get only non-zero bytes
    non_zero_xor = []
    non_zero_positions = []
    
    for i, byte in enumerate(full_xor):
        if byte != 0:
            non_zero_xor.append(byte)
            non_zero_positions.append(i)
    
    print(f"Found {len(non_zero_xor)} non-zero bytes in XOR")
    
    # Convert to different representations
    xor_bytes = bytes(non_zero_xor)
    
    print(f"XOR as hex: {xor_bytes.hex()}")
    
    # Try different chunking and interpretations
    def try_interpretation(data, description):
        print(f"\n--- {description} ---")
        
        # Direct ASCII
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)
        print(f"ASCII: {ascii_str}")
        
        # Look for flag patterns
        if '[REDACTED]")
            return True
        elif '[REDACTED]")
            return True
        
        # Try reversing
        reversed_ascii = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[::-1])
        print(f"Reversed ASCII: {reversed_ascii}")
        
        if '[REDACTED]")
            return True
        
        # Try every 2nd byte
        every_2nd = data[::2]
        ascii_2nd = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in every_2nd)
        print(f"Every 2nd byte: {ascii_2nd}")
        
        if '[REDACTED]")
            return True
        
        # Try every 2nd byte starting from offset 1
        every_2nd_offset = data[1::2]
        ascii_2nd_offset = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in every_2nd_offset)
        print(f"Every 2nd byte (offset 1): {ascii_2nd_offset}")
        
        if '[REDACTED]")
            return True
        
        return False
    
    # Try different interpretations
    if try_interpretation(xor_bytes, "Direct XOR bytes"):
        return
    
    # Try interpreting the bytes from each file separately at difference positions
    bytes_from_file1 = bytes(data1[pos] for pos in non_zero_positions)
    bytes_from_file2 = bytes(data2[pos] for pos in non_zero_positions)
    
    if try_interpretation(bytes_from_file1, "Bytes from file 1 at diff positions"):
        return
    
    if try_interpretation(bytes_from_file2, "Bytes from file 2 at diff positions"):
        return
    
    # Try bitwise operations
    print("\n--- Bitwise operations ---")
    
    # Try AND operation
    and_bytes = bytes(data1[pos] & data2[pos] for pos in non_zero_positions)
    if try_interpretation(and_bytes, "AND operation"):
        return
    
    # Try OR operation
    or_bytes = bytes(data1[pos] | data2[pos] for pos in non_zero_positions)
    if try_interpretation(or_bytes, "OR operation"):
        return
    
    # Try looking at the high/low nibbles separately
    print("\n--- Nibble analysis ---")
    
    high_nibbles = bytes((b >> 4) & 0x0F for b in xor_bytes)
    low_nibbles = bytes(b & 0x0F for b in xor_bytes)
    
    # Convert nibbles to ASCII by adding ASCII offset
    high_ascii = ''.join(chr((b % 26) + ord('A')) for b in high_nibbles)
    low_ascii = ''.join(chr((b % 26) + ord('A')) for b in low_nibbles)
    
    print(f"High nibbles as letters: {high_ascii}")
    print(f"Low nibbles as letters: {low_ascii}")
    
    if 'FLAG' in high_ascii:
        print(f"🎯 FOUND FLAG IN HIGH NIBBLES: {high_ascii}")
    if 'FLAG' in low_ascii:
        print(f"🎯 FOUND FLAG IN LOW NIBBLES: {low_ascii}")
    
    # Try interpreting as decimal values
    print("\n--- Decimal interpretation ---")
    decimal_chars = ''.join(chr(b % 95 + 32) for b in xor_bytes)
    print(f"Decimal mod interpretation: {decimal_chars}")
    
    if '[REDACTED]")
    
    # Last resort - show all interpretations for manual analysis
    print("\n--- All interpretations for manual review ---")
    print(f"Raw XOR hex: {xor_bytes.hex()}")
    print(f"Length: {len(xor_bytes)} bytes")
    
    # Show chunks of 16 bytes
    for i in range(0, len(xor_bytes), 16):
        chunk = xor_bytes[i:i+16]
        hex_str = chunk.hex()
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        print(f"Offset {i:3d}: {hex_str:<32} | {ascii_str}")
    
    # Try the differences as coordinates or indices into a message
    print(f"\n--- Position analysis ---")
    print(f"Difference positions: {non_zero_positions[:20]}...")
    
    # Maybe the positions themselves encode something?
    if len(non_zero_positions) > 0:
        pos_as_chars = ''.join(chr(pos % 95 + 32) for pos in non_zero_positions if pos < 127)
        print(f"Positions as ASCII: {pos_as_chars[:50]}")
        
        if '[REDACTED]")

if __name__ == "__main__":
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Wrong_QR")
    final_flag_extraction()
