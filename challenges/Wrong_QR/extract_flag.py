#!/usr/bin/env python3

"""
Extract flag from QR code differences
"""

def extract_flag():
    """Extract the flag from XOR differences between the two QR codes"""
    
    with open('binary_qr_code1(2).png', 'rb') as f1:
        data1 = f1.read()
    
    with open('binary_qr_code(2).png', 'rb') as f2:
        data2 = f2.read()
    
    # Calculate XOR differences
    xor_data = []
    for b1, b2 in zip(data1, data2):
        xor_data.append(b1 ^ b2)
    
    xor_bytes = bytes(xor_data)
    
    print(f"Total XOR data: {len(xor_bytes)} bytes")
    print(f"XOR hex: {xor_bytes.hex()}")
    
    # Look for [REDACTED] in XOR data!")
            start = xor_bytes.find(pattern)
            # Look for closing brace
            end = xor_bytes.find(b'}', start)
            if end != -1:
                flag = xor_bytes[start:end+1]
                print(f"Complete flag: {flag}")
                return flag.decode('utf-8', errors='ignore')
    
    # Try bit shifting/manipulation
    print("\nTrying bit manipulations:")
    
    # Remove null bytes and try again
    clean_xor = bytes(b for b in xor_data if b != 0)
    print(f"Clean XOR (no nulls): {clean_xor}")
    
    for pattern in flag_patterns:
        if pattern in clean_xor:
            print(f"Found {pattern} in clean XOR data!")
            start = clean_xor.find(pattern)
            end = clean_xor.find(b'}', start)
            if end != -1:
                flag = clean_xor[start:end+1]
                print(f"Complete flag: {flag}")
                return flag.decode('utf-8', errors='ignore')
    
    # Try interpreting different sections as ASCII
    print("\nTrying different sections as ASCII:")
    
    # Skip PNG header and try from image data
    png_header_size = 50  # Approximate
    image_xor = xor_bytes[png_header_size:]
    
    ascii_chars = []
    for b in image_xor:
        if 32 <= b <= 126:  # Printable ASCII
            ascii_chars.append(chr(b))
        elif b == 0:
            ascii_chars.append(' ')  # Treat null as space
        else:
            ascii_chars.append('.')
    
    ascii_text = ''.join(ascii_chars)
    print(f"ASCII from image data: {ascii_text[:100]}...")
    
    # Look for flag in ASCII text
    if '[REDACTED]")
    
    # Try reverse
    reversed_xor = xor_bytes[::-1]
    ascii_chars = []
    for b in reversed_xor:
        if 32 <= b <= 126:
            ascii_chars.append(chr(b))
        elif b == 0:
            ascii_chars.append(' ')
        else:
            ascii_chars.append('.')
    
    ascii_text = ''.join(ascii_chars)
    print(f"\nReversed ASCII: {ascii_text[:100]}...")
    
    # Try every 8th byte (might be encoded in a pattern)
    print("\nTrying pattern extractions:")
    
    for step in [1, 2, 4, 8]:
        pattern_bytes = xor_bytes[::step]
        ascii_chars = []
        for b in pattern_bytes:
            if 32 <= b <= 126:
                ascii_chars.append(chr(b))
            elif b == 0:
                ascii_chars.append(' ')
            else:
                ascii_chars.append('.')
        
        ascii_text = ''.join(ascii_chars)
        if '[REDACTED] pattern: {ascii_text}")
    
    # Manual inspection of the differences we saw
    differences = [
        0x01, 0x49, 0x14, 0x01, 0x7d, 0xb1, 0x58, 0x28,
        0x45, 0x91, 0x17, 0xb7, 0x9a, 0x62, 0xb0, 0x02,
        0xef, 0x22, 0x46, 0x90, 0x06, 0x22, 0x70, 0x10,
        0x24, 0x3e, 0x3f, 0x30, 0x06, 0xa2, 0xe4, 0x6f
    ]
    
    print(f"\nFirst 32 XOR differences as ASCII:")
    ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in differences)
    print(f"ASCII: {ascii_str}")
    
    # Try treating as little-endian/big-endian integers
    print("\nTrying as encoded integers:")
    for i in range(0, len(differences)-3, 4):
        chunk = differences[i:i+4]
        big_endian = (chunk[0] << 24) | (chunk[1] << 16) | (chunk[2] << 8) | chunk[3]
        little_endian = chunk[0] | (chunk[1] << 8) | (chunk[2] << 16) | (chunk[3] << 24)
        print(f"Chunk {i//4}: BE={big_endian}, LE={little_endian}")
        
        # Try interpreting as ASCII values
        be_chars = []
        le_chars = []
        for j in range(4):
            be_byte = (big_endian >> (8 * (3-j))) & 0xFF
            le_byte = (little_endian >> (8 * j)) & 0xFF
            be_chars.append(chr(be_byte) if 32 <= be_byte <= 126 else '.')
            le_chars.append(chr(le_byte) if 32 <= le_byte <= 126 else '.')
        
        print(f"  BE ASCII: {''.join(be_chars)}")
        print(f"  LE ASCII: {''.join(le_chars)}")

def try_direct_differences():
    """Try to decode the flag directly from byte differences"""
    
    with open('binary_qr_code1(2).png', 'rb') as f1:
        data1 = f1.read()
    
    with open('binary_qr_code(2).png', 'rb') as f2:
        data2 = f2.read()
    
    # Get just the differing bytes in order
    differences = []
    for i, (b1, b2) in enumerate(zip(data1, data2)):
        if b1 != b2:
            differences.append((i, b1, b2, b1^b2))
    
    print("=== Direct Flag Extraction ===")
    
    # Extract just the XOR values
    xor_values = [diff[3] for diff in differences]
    
    # Try treating XOR values as direct ASCII
    flag_candidate = ""
    for val in xor_values:
        if 32 <= val <= 126:
            flag_candidate += chr(val)
        else:
            flag_candidate += f"\\x{val:02x}"
    
    print(f"XOR as ASCII: {flag_candidate}")
    
    # Look for readable sections
    readable_parts = []
    current_part = ""
    
    for val in xor_values:
        if 32 <= val <= 126:
            current_part += chr(val)
        else:
            if len(current_part) >= 3:  # Keep parts with 3+ readable chars
                readable_parts.append(current_part)
            current_part = ""
    
    if current_part and len(current_part) >= 3:
        readable_parts.append(current_part)
    
    print(f"Readable parts: {readable_parts}")
    
    # Check if any readable part contains flag-like content
    for part in readable_parts:
        if any(keyword in part.lower() for keyword in ['flag', 'ctf', 'bootup']):
            print(f"Potential flag part: {part}")

if __name__ == "__main__":
    print("=== QR Code Flag Extraction ===")
    
    flag = extract_flag()
    if flag:
        print(f"\n🎉 FLAG FOUND: {flag}")
    else:
        print("\n❌ Flag not found in standard patterns")
        print("\nTrying alternative approaches...")
        try_direct_differences()
