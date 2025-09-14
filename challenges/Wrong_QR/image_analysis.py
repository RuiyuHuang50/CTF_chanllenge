#!/usr/bin/env python3

import os
import zlib

def analyze_qr_image_data():
    """Analyze the actual QR code image data after PNG decompression"""
    
    file1 = "binary_qr_code1(2).png"
    file2 = "binary_qr_code(2).png"
    
    print("=== QR Image Data Analysis ===")
    
    def extract_idat_data(filename):
        """Extract and decompress IDAT chunk data"""
        with open(filename, 'rb') as f:
            data = f.read()
        
        # Find IDAT chunk
        pos = 8  # Skip PNG signature
        while pos < len(data) - 8:
            length = int.from_bytes(data[pos:pos+4], 'big')
            chunk_type = data[pos+4:pos+8]
            
            if chunk_type == b'IDAT':
                chunk_data = data[pos+8:pos+8+length]
                print(f"Found IDAT chunk in {filename}, length: {length}")
                
                # Decompress the data
                try:
                    decompressed = zlib.decompress(chunk_data)
                    print(f"Decompressed IDAT data length: {len(decompressed)}")
                    return decompressed
                except Exception as e:
                    print(f"Error decompressing IDAT: {e}")
                    return None
            
            pos += 8 + length + 4
        
        return None
    
    # Extract image data from both files
    img_data1 = extract_idat_data(file1)
    img_data2 = extract_idat_data(file2)
    
    if img_data1 and img_data2:
        print(f"\nImage data 1 length: {len(img_data1)}")
        print(f"Image data 2 length: {len(img_data2)}")
        
        # The image data should represent a 29x29 QR code
        # PNG format includes filter bytes, so let's analyze the structure
        
        print(f"First 20 bytes of image 1: {img_data1[:20].hex()}")
        print(f"First 20 bytes of image 2: {img_data2[:20].hex()}")
        
        # For a grayscale PNG, each row starts with a filter byte
        # followed by the pixel data
        width = 29  # QR code is 29x29
        height = 29
        
        def parse_png_rows(data, label):
            print(f"\n=== Parsing {label} rows ===")
            rows = []
            pos = 0
            
            for row in range(height):
                if pos >= len(data):
                    break
                
                filter_byte = data[pos]
                pos += 1
                
                # For grayscale, each pixel is 1 byte
                row_data = data[pos:pos+width]
                pos += width
                
                if len(row_data) == width:
                    rows.append(row_data)
                    # Print first few rows for debugging
                    if row < 5:
                        row_ascii = ''.join('█' if b < 128 else '░' for b in row_data)
                        print(f"Row {row} (filter {filter_byte}): {row_ascii}")
            
            return rows
        
        rows1 = parse_png_rows(img_data1, "Image 1")
        rows2 = parse_png_rows(img_data2, "Image 2")
        
        # Compare the QR code patterns
        if len(rows1) == len(rows2):
            print(f"\n=== QR Pattern Comparison ===")
            diff_positions = []
            
            for y in range(min(len(rows1), len(rows2))):
                if len(rows1[y]) == len(rows2[y]):
                    for x in range(len(rows1[y])):
                        if rows1[y][x] != rows2[y][x]:
                            diff_positions.append((x, y))
            
            print(f"Found {len(diff_positions)} pixel differences")
            
            if diff_positions:
                print(f"First 20 differences: {diff_positions[:20]}")
                
                # Try to extract meaningful data from the differences
                diff_pattern1 = []
                diff_pattern2 = []
                
                for x, y in diff_positions:
                    if y < len(rows1) and x < len(rows1[y]):
                        diff_pattern1.append(rows1[y][x])
                    if y < len(rows2) and x < len(rows2[y]):
                        diff_pattern2.append(rows2[y][x])
                
                print(f"Diff pattern 1 (first 20): {diff_pattern1[:20]}")
                print(f"Diff pattern 2 (first 20): {diff_pattern2[:20]}")
                
                # Convert pixel differences to binary
                binary1 = ''.join('1' if p < 128 else '0' for p in diff_pattern1)
                binary2 = ''.join('1' if p < 128 else '0' for p in diff_pattern2)
                
                print(f"Binary pattern 1: {binary1[:50]}...")
                print(f"Binary pattern 2: {binary2[:50]}...")
                
                # Try to interpret as ASCII
                def binary_to_ascii(binary_str):
                    """Convert binary string to ASCII"""
                    result = ""
                    for i in range(0, len(binary_str), 8):
                        byte_str = binary_str[i:i+8]
                        if len(byte_str) == 8:
                            byte_val = int(byte_str, 2)
                            if 32 <= byte_val <= 126:
                                result += chr(byte_val)
                            else:
                                result += '.'
                    return result
                
                ascii1 = binary_to_ascii(binary1)
                ascii2 = binary_to_ascii(binary2)
                
                print(f"ASCII interpretation 1: {ascii1}")
                print(f"ASCII interpretation 2: {ascii2}")
                
                # Look for flag patterns
                for text, label in [(ascii1, "pattern 1"), (ascii2, "pattern 2")]:
                    if '[REDACTED]: {text}")
                    elif '[REDACTED]: {text}")
                
                # Also try XOR of the two patterns
                if len(diff_pattern1) == len(diff_pattern2):
                    xor_pattern = [a ^ b for a, b in zip(diff_pattern1, diff_pattern2)]
                    binary_xor = ''.join('1' if p != 0 else '0' for p in xor_pattern)
                    ascii_xor = binary_to_ascii(binary_xor)
                    
                    print(f"XOR binary pattern: {binary_xor[:50]}...")
                    print(f"XOR ASCII interpretation: {ascii_xor}")
                    
                    if '[REDACTED]")
        
        # Also try direct XOR of the decompressed image data
        print(f"\n=== Direct Image Data XOR ===")
        if len(img_data1) == len(img_data2):
            img_xor = bytes(a ^ b for a, b in zip(img_data1, img_data2))
            non_zero_xor = bytes(x for x in img_xor if x != 0)
            
            print(f"Non-zero XOR bytes in image data: {len(non_zero_xor)}")
            ascii_attempt = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in non_zero_xor)
            print(f"ASCII attempt: {ascii_attempt}")
            
            if '[REDACTED]")

if __name__ == "__main__":
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Wrong_QR")
    analyze_qr_image_data()
