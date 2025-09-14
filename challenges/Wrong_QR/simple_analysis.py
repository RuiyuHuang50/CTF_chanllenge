#!/usr/bin/env python3

"""
Simple QR code comparison without external libraries
"""

def extract_png_data(filename):
    """Extract raw PNG image data"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Find IDAT chunk(s) which contain the image data
    idat_chunks = []
    pos = 8  # Skip PNG signature
    
    while pos < len(data):
        # Read chunk length
        if pos + 8 > len(data):
            break
            
        length = int.from_bytes(data[pos:pos+4], 'big')
        chunk_type = data[pos+4:pos+8]
        
        if chunk_type == b'IDAT':
            chunk_data = data[pos+8:pos+8+length]
            idat_chunks.append(chunk_data)
        
        pos += 8 + length + 4  # Move to next chunk (length + type + data + CRC)
    
    return b''.join(idat_chunks)

def compare_files_binary():
    """Compare the two QR code files byte by byte"""
    print("=== Binary File Comparison ===")
    
    with open('binary_qr_code1(2).png', 'rb') as f1:
        data1 = f1.read()
    
    with open('binary_qr_code(2).png', 'rb') as f2:
        data2 = f2.read()
    
    print(f"File 1 size: {len(data1)} bytes")
    print(f"File 2 size: {len(data2)} bytes")
    
    if len(data1) != len(data2):
        print("Files have different sizes!")
        return
    
    differences = []
    for i, (b1, b2) in enumerate(zip(data1, data2)):
        if b1 != b2:
            differences.append((i, b1, b2))
    
    print(f"Number of different bytes: {len(differences)}")
    
    if differences:
        print("First 20 differences:")
        for i, (pos, b1, b2) in enumerate(differences[:20]):
            print(f"  Position {pos}: {b1:02x} vs {b2:02x} (diff: {b1^b2:02x})")
        
        # Try to extract meaningful data from differences
        diff_bytes = [b1^b2 for pos, b1, b2 in differences]
        print(f"\nXOR differences: {[hex(b) for b in diff_bytes[:20]]}")
        
        # Try to interpret as ASCII
        ascii_chars = []
        for b in diff_bytes:
            if 32 <= b <= 126:  # Printable ASCII
                ascii_chars.append(chr(b))
            else:
                ascii_chars.append('.')
        
        print(f"ASCII interpretation: {''.join(ascii_chars)}")
        
        # Look for patterns in the differences
        analyze_difference_patterns(differences)

def analyze_difference_patterns(differences):
    """Analyze patterns in the differences"""
    print("\n=== Analyzing Difference Patterns ===")
    
    # Extract just the XOR values
    xor_values = [b1^b2 for pos, b1, b2 in differences]
    
    # Try to find flag patterns
    xor_bytes = bytes(xor_values)
    
    # Look for [REDACTED]")
            start = xor_bytes.find(pattern)
            end = xor_bytes.find(b'}', start) + 1 if b'}' in xor_bytes[start:] else len(xor_bytes)
            potential_flag = xor_bytes[start:end]
            print(f"Potential flag: {potential_flag}")
    
    # Try interpreting as bit patterns
    print(f"\nAs binary: {''.join(format(b, '08b') for b in xor_values[:10])}...")
    
    # Try grouping bytes
    if len(xor_values) >= 8:
        print("Grouped as 8-byte chunks:")
        for i in range(0, len(xor_values), 8):
            chunk = xor_values[i:i+8]
            hex_str = ' '.join(f'{b:02x}' for b in chunk)
            ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
            print(f"  {hex_str:24} | {ascii_str}")

def try_simple_decode():
    """Try simple approaches to decode the QR codes"""
    print("\n=== Simple Decode Attempts ===")
    
    # Since these are very small QR codes (29x29), they might be custom or simplified
    print("29x29 is quite small for a standard QR code.")
    print("Standard QR code sizes are: 21x21 (Version 1), 25x25 (Version 2), 29x29 (Version 3)")
    print("This suggests Version 3 QR codes, which can hold ~23-35 alphanumeric characters")
    
    # Extract PNG data
    print("\nExtracting PNG image data...")
    try:
        data1 = extract_png_data('binary_qr_code1(2).png')
        data2 = extract_png_data('binary_qr_code(2).png')
        
        print(f"IDAT data 1: {len(data1)} bytes")
        print(f"IDAT data 2: {len(data2)} bytes")
        
        if data1 != data2:
            print("IDAT chunks are different (as expected)")
        
    except Exception as e:
        print(f"Error extracting PNG data: {e}")

def main():
    print("=== Wrong QR Challenge Analysis ===")
    
    # First, compare the files at binary level
    compare_files_binary()
    
    # Try simple decode approaches
    try_simple_decode()
    
    print("\n=== Next Steps ===")
    print("1. The files are definitely different")
    print("2. The differences might encode the flag directly")
    print("3. Try online QR code decoders with both images")
    print("4. The XOR of the differences might reveal the flag")

if __name__ == "__main__":
    main()
