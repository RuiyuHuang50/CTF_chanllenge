#!/usr/bin/env python3

import os
import zlib

def manual_qr_decode():
    """Attempt to manually decode QR code patterns"""
    
    file1 = "binary_qr_code1(2).png"
    file2 = "binary_qr_code(2).png"
    
    print("=== Manual QR Decode Attempt ===")
    
    def extract_pixel_data(filename):
        """Extract pixel data from PNG"""
        with open(filename, 'rb') as f:
            data = f.read()
        
        # Find IDAT chunk and decompress
        pos = 8  # Skip PNG signature
        while pos < len(data) - 8:
            length = int.from_bytes(data[pos:pos+4], 'big')
            chunk_type = data[pos+4:pos+8]
            
            if chunk_type == b'IDAT':
                chunk_data = data[pos+8:pos+8+length]
                try:
                    decompressed = zlib.decompress(chunk_data)
                    
                    # Parse pixel data (29x29 grayscale)
                    pixels = []
                    pos_pixel = 0
                    
                    for row in range(29):
                        if pos_pixel >= len(decompressed):
                            break
                        
                        # Skip filter byte
                        pos_pixel += 1
                        
                        row_pixels = []
                        for col in range(29):
                            if pos_pixel < len(decompressed):
                                pixel = decompressed[pos_pixel]
                                row_pixels.append(1 if pixel < 128 else 0)  # Binary: black=1, white=0
                                pos_pixel += 1
                        
                        if len(row_pixels) == 29:
                            pixels.append(row_pixels)
                    
                    return pixels
                except Exception as e:
                    print(f"Error decompressing {filename}: {e}")
                    return None
            
            pos += 8 + length + 4
        
        return None
    
    # Extract pixel data from both QR codes
    pixels1 = extract_pixel_data(file1)
    pixels2 = extract_pixel_data(file2)
    
    if pixels1 and pixels2:
        print(f"Successfully extracted pixel data:")
        print(f"QR1: {len(pixels1)}x{len(pixels1[0]) if pixels1 else 0}")
        print(f"QR2: {len(pixels2)}x{len(pixels2[0]) if pixels2 else 0}")
        
        # Print visual representation
        def print_qr(pixels, label):
            print(f"\n{label}:")
            for row in pixels:
                line = ''.join('██' if p else '░░' for p in row)
                print(line)
        
        print_qr(pixels1[:10], "QR1 (first 10 rows)")
        print_qr(pixels2[:10], "QR2 (first 10 rows)")
        
        # Calculate differences
        diff_positions = []
        for y in range(len(pixels1)):
            for x in range(len(pixels1[y])):
                if y < len(pixels2) and x < len(pixels2[y]):
                    if pixels1[y][x] != pixels2[y][x]:
                        diff_positions.append((x, y))
        
        print(f"\nFound {len(diff_positions)} pixel differences")
        print(f"First 20 differences: {diff_positions[:20]}")
        
        # Try to extract data from differences
        # Method 1: Get the different pixel values in order
        diff_data1 = []
        diff_data2 = []
        
        for x, y in diff_positions:
            diff_data1.append(pixels1[y][x])
            diff_data2.append(pixels2[y][x])
        
        # Convert to binary strings
        binary1 = ''.join(str(bit) for bit in diff_data1)
        binary2 = ''.join(str(bit) for bit in diff_data2)
        
        print(f"\nBinary from QR1 differences: {binary1[:50]}...")
        print(f"Binary from QR2 differences: {binary2[:50]}...")
        
        # Try to decode as ASCII (8 bits per character)
        def binary_to_text(binary_str):
            text = ""
            for i in range(0, len(binary_str), 8):
                byte_str = binary_str[i:i+8]
                if len(byte_str) == 8:
                    byte_val = int(byte_str, 2)
                    if 32 <= byte_val <= 126:
                        text += chr(byte_val)
                    else:
                        text += '.'
            return text
        
        text1 = binary_to_text(binary1)
        text2 = binary_to_text(binary2)
        
        print(f"Text from QR1 diffs: {text1}")
        print(f"Text from QR2 diffs: {text2}")
        
        # Try XOR of the difference bits
        xor_bits = []
        for i in range(min(len(diff_data1), len(diff_data2))):
            xor_bits.append(diff_data1[i] ^ diff_data2[i])
        
        binary_xor = ''.join(str(bit) for bit in xor_bits)
        text_xor = binary_to_text(binary_xor)
        
        print(f"XOR of differences: {binary_xor[:50]}...")
        print(f"XOR as text: {text_xor}")
        
        # Look for FLAG patterns
        for text, label in [(text1, "QR1"), (text2, "QR2"), (text_xor, "XOR")]:
            if '[REDACTED]: {text}")
            elif '[REDACTED]: {text}")
        
        # Try different bit groupings
        print(f"\nTrying different bit groupings:")
        for bits_per_char in [7, 9, 10, 11, 12]:
            text_alt = ""
            for i in range(0, len(binary_xor), bits_per_char):
                chunk = binary_xor[i:i+bits_per_char]
                if len(chunk) == bits_per_char:
                    val = int(chunk, 2)
                    if 32 <= val <= 126:
                        text_alt += chr(val)
                    else:
                        text_alt += '.'
            
            if len(text_alt) > 5:
                print(f"{bits_per_char} bits/char: {text_alt[:30]}...")
                if 'FLAG' in text_alt:
                    print(f"🎯 FOUND FLAG WITH {bits_per_char} BITS: {text_alt}")

if __name__ == "__main__":
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Wrong_QR")
    manual_qr_decode()
