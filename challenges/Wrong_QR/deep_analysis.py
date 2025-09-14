#!/usr/bin/env python3

import os

def deep_qr_analysis():
    """Deep analysis of QR codes focusing on the unique string found"""
    
    file1 = "binary_qr_code1(2).png"
    file2 = "binary_qr_code(2).png"
    
    print("=== Deep QR Analysis ===")
    
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    
    # Find the position of the unique string "Pv$4d"
    unique_str = b"Pv$4d"
    pos = data2.find(unique_str)
    if pos != -1:
        print(f"Found unique string 'Pv$4d' at position {pos} in file 2")
        print(f"Context around position {pos}:")
        start = max(0, pos - 20)
        end = min(len(data2), pos + 20)
        context = data2[start:end]
        print(f"  Hex: {context.hex()}")
        print(f"  ASCII: {repr(context)}")
        
        # Check what's at the same position in file 1
        if pos < len(data1):
            context1 = data1[start:end]
            print(f"File 1 same position:")
            print(f"  Hex: {context1.hex()}")
            print(f"  ASCII: {repr(context1)}")
    
    # Try to decode QR manually by looking at the image data
    print("\n=== Manual QR Analysis ===")
    
    # PNG structure: signature + chunks
    # Each chunk: length (4) + type (4) + data (length) + CRC (4)
    
    def parse_png_chunks(data, filename):
        print(f"\nParsing chunks in {filename}:")
        
        # Skip PNG signature (8 bytes)
        pos = 8
        chunks = []
        
        while pos < len(data) - 8:
            if pos + 8 > len(data):
                break
                
            length = int.from_bytes(data[pos:pos+4], 'big')
            chunk_type = data[pos+4:pos+8]
            
            if pos + 8 + length + 4 > len(data):
                break
                
            chunk_data = data[pos+8:pos+8+length]
            crc = data[pos+8+length:pos+8+length+4]
            
            chunks.append({
                'type': chunk_type,
                'length': length,
                'data': chunk_data,
                'pos': pos
            })
            
            print(f"  Chunk: {chunk_type.decode('ascii', errors='ignore')} (length: {length})")
            
            # If this is IDAT (image data), show some info
            if chunk_type == b'IDAT':
                print(f"    IDAT data preview: {chunk_data[:20].hex()}")
            
            pos += 8 + length + 4
        
        return chunks
    
    chunks1 = parse_png_chunks(data1, file1)
    chunks2 = parse_png_chunks(data2, file2)
    
    # Compare IDAT chunks specifically
    print("\n=== IDAT Chunk Comparison ===")
    
    idat1 = None
    idat2 = None
    
    for chunk in chunks1:
        if chunk['type'] == b'IDAT':
            idat1 = chunk['data']
            break
    
    for chunk in chunks2:
        if chunk['type'] == b'IDAT':
            idat2 = chunk['data']
            break
    
    if idat1 and idat2:
        print(f"IDAT1 length: {len(idat1)}")
        print(f"IDAT2 length: {len(idat2)}")
        
        if len(idat1) == len(idat2):
            # XOR the IDAT data
            idat_xor = bytes(a ^ b for a, b in zip(idat1, idat2))
            non_zero = [i for i, x in enumerate(idat_xor) if x != 0]
            
            print(f"IDAT differences at positions: {non_zero[:20]}...")
            print(f"IDAT XOR (first 50 bytes): {idat_xor[:50].hex()}")
            
            # Try to extract meaningful data from IDAT differences
            idat_diff_clean = bytes(x for x in idat_xor if x != 0)
            print(f"IDAT non-zero differences: {len(idat_diff_clean)} bytes")
            print(f"IDAT diff ASCII attempt: {repr(idat_diff_clean[:50])}")
    
    # Try different interpretation of the unique string
    print(f"\n=== Analysis of unique string 'Pv$4d' ===")
    unique_bytes = b"Pv$4d"
    print(f"Hex: {unique_bytes.hex()}")
    print(f"Decimal: {[b for b in unique_bytes]}")
    print(f"Binary: {' '.join(format(b, '08b') for b in unique_bytes)}")
    
    # Try to interpret as base64 or other encoding
    import base64
    try:
        # Try base64 decode
        b64_decoded = base64.b64decode(unique_bytes + b'==')  # Add padding
        print(f"Base64 decode attempt: {b64_decoded}")
    except:
        print("Not valid base64")
    
    # Check if it could be part of a larger pattern
    print(f"\n=== Looking for extended patterns ===")
    
    # Find all positions where files differ
    diff_positions = []
    for i, (a, b) in enumerate(zip(data1, data2)):
        if a != b:
            diff_positions.append(i)
    
    print(f"Files differ at {len(diff_positions)} positions")
    if diff_positions:
        print(f"First 20 diff positions: {diff_positions[:20]}")
        
        # Extract bytes from these positions
        diff_bytes_from_1 = bytes(data1[pos] for pos in diff_positions)
        diff_bytes_from_2 = bytes(data2[pos] for pos in diff_positions)
        
        print(f"Diff bytes from file 1: {diff_bytes_from_1[:20].hex()}")
        print(f"Diff bytes from file 2: {diff_bytes_from_2[:20].hex()}")
        
        # Try these as ASCII
        try:
            ascii1 = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in diff_bytes_from_1)
            ascii2 = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in diff_bytes_from_2)
            print(f"ASCII from file 1 diffs: {ascii1[:50]}")
            print(f"ASCII from file 2 diffs: {ascii2[:50]}")
            
            # Look for flag patterns in either
            for text, label in [(ascii1, "file1 diffs"), (ascii2, "file2 diffs")]:
                if '[REDACTED]: {text}")
                elif '[REDACTED]: {text}")
                    
        except Exception as e:
            print(f"Error in ASCII conversion: {e}")

if __name__ == "__main__":
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Wrong_QR")
    deep_qr_analysis()
