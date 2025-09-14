#!/usr/bin/env python3

"""
QR Code analyzer for Wrong_QR challenge

This script will:
1. Load and analyze the two QR code images
2. Decode them to extract data
3. Look for patterns or differences between them
4. Attempt to recover the flag
"""

import sys
import os

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("PIL and numpy are required. Install with: pip install pillow numpy")
    sys.exit(1)

def load_qr_images():
    """Load the QR code images"""
    files = ['binary_qr_code1(2).png', 'binary_qr_code(2).png']
    images = {}
    
    for filename in files:
        if os.path.exists(filename):
            img = Image.open(filename)
            images[filename] = img
            print(f"Loaded {filename}: {img.size}")
        else:
            print(f"File not found: {filename}")
    
    return images

def analyze_qr_structure(img):
    """Analyze QR code structure"""
    # Convert to grayscale and then binary
    gray = img.convert('L')
    # Convert to numpy array for analysis
    arr = np.array(gray)
    
    print(f"Image dimensions: {arr.shape}")
    print(f"Unique values: {np.unique(arr)}")
    
    # Simple thresholding to convert to binary
    binary = arr < 128  # True for black pixels, False for white
    
    return binary

def compare_qr_codes(img1, img2):
    """Compare two QR codes to find differences"""
    bin1 = analyze_qr_structure(img1)
    bin2 = analyze_qr_structure(img2)
    
    if bin1.shape != bin2.shape:
        print("QR codes have different sizes!")
        return None
    
    # Find differences
    diff = bin1 != bin2
    diff_count = np.sum(diff)
    
    print(f"Number of different pixels: {diff_count}")
    print(f"Percentage difference: {(diff_count / bin1.size) * 100:.2f}%")
    
    if diff_count > 0:
        print("Positions of differences:")
        diff_positions = np.where(diff)
        for i in range(min(10, len(diff_positions[0]))):  # Show first 10 differences
            row, col = diff_positions[0][i], diff_positions[1][i]
            print(f"  ({row}, {col}): QR1={bin1[row,col]}, QR2={bin2[row,col]}")
    
    return bin1, bin2, diff

def extract_qr_data_manual(binary_array):
    """
    Manual QR code data extraction
    This is a simplified approach - real QR decoding is complex
    """
    print("Attempting manual QR analysis...")
    
    # QR codes have finder patterns in corners
    # Let's look for these patterns
    size = binary_array.shape[0]
    print(f"QR code size: {size}x{size}")
    
    # Check if it's a valid QR size (should be (21 + 4*version))
    version = (size - 21) // 4 + 1 if (size - 21) % 4 == 0 else None
    if version:
        print(f"Estimated QR version: {version}")
    
    return binary_array

def try_decode_with_external():
    """Try to decode with external tools if available"""
    try:
        import cv2
        print("OpenCV available, trying QR detection...")
        
        for filename in ['binary_qr_code1(2).png', 'binary_qr_code(2).png']:
            if os.path.exists(filename):
                img = cv2.imread(filename)
                detector = cv2.QRCodeDetector()
                data, vertices_array, binary_qrcode = detector.detectAndDecode(img)
                
                if data:
                    print(f"{filename}: {data}")
                else:
                    print(f"{filename}: Could not decode")
    except ImportError:
        print("OpenCV not available")
    
    # Try with zbar if available
    try:
        import pyzbar.pyzbar as pyzbar
        print("pyzbar available, trying QR detection...")
        
        for filename in ['binary_qr_code1(2).png', 'binary_qr_code(2).png']:
            if os.path.exists(filename):
                img = Image.open(filename)
                codes = pyzbar.decode(img)
                
                if codes:
                    for code in codes:
                        print(f"{filename}: {code.data.decode('utf-8')}")
                else:
                    print(f"{filename}: Could not decode")
    except ImportError:
        print("pyzbar not available")

def analyze_differences(diff_array):
    """Analyze the differences between QR codes"""
    if diff_array is None:
        return
    
    # Count total differences
    total_diff = np.sum(diff_array)
    
    if total_diff == 0:
        print("QR codes are identical!")
        return
    
    print(f"\nAnalyzing {total_diff} differences...")
    
    # Get positions of all differences
    diff_positions = np.where(diff_array)
    
    # Try to see if differences form a pattern
    diff_coords = list(zip(diff_positions[0], diff_positions[1]))
    
    print("All difference positions:")
    for i, (row, col) in enumerate(diff_coords):
        print(f"  {i+1}: ({row}, {col})")
    
    return diff_coords

def main():
    print("=== QR Code Analysis for Wrong_QR Challenge ===")
    
    # Load images
    images = load_qr_images()
    
    if len(images) != 2:
        print("Could not load both QR code images!")
        return
    
    filenames = list(images.keys())
    img1, img2 = images[filenames[0]], images[filenames[1]]
    
    print(f"\nAnalyzing {filenames[0]}...")
    bin1 = analyze_qr_structure(img1)
    
    print(f"\nAnalyzing {filenames[1]}...")
    bin2 = analyze_qr_structure(img2)
    
    print(f"\nComparing QR codes...")
    comparison = compare_qr_codes(img1, img2)
    
    if comparison:
        bin1, bin2, diff = comparison
        diff_coords = analyze_differences(diff)
        
        # If there are differences, they might encode the flag
        if diff_coords:
            print("\nAttempting to extract flag from differences...")
            # Convert difference positions to potential binary data
            # This is speculative - the actual encoding method would need to be determined
            
            # Try interpreting differences as binary
            binary_string = ""
            for row, col in sorted(diff_coords):
                # Use the difference pattern as binary data
                binary_string += "1"
            
            print(f"Binary string from differences: {binary_string}")
            
            # Try to convert to ASCII
            if len(binary_string) % 8 == 0:
                try:
                    chars = []
                    for i in range(0, len(binary_string), 8):
                        byte = binary_string[i:i+8]
                        chars.append(chr(int(byte, 2)))
                    result = ''.join(chars)
                    print(f"ASCII interpretation: {result}")
                except:
                    print("Could not convert to ASCII")
    
    # Try external decoders
    print("\nTrying external QR decoders...")
    try_decode_with_external()

if __name__ == "__main__":
    main()
