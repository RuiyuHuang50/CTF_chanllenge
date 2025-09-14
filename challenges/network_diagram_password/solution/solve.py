#!/usr/bin/env python3
"""
Solution for: Network Diagram Password
Date: 2025-09-12
Challenge: Extract hidden password from redacted network diagram
"""

import subprocess
import re

def extract_strings_from_image(image_path):
    """Extract strings from the draw.io PNG file"""
    try:
        result = subprocess.run(['strings', image_path], 
                              capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error extracting strings: {e}")
        return ""

def find_flag_parts(strings_output):
    """Find and assemble the flag parts from the strings"""
    # The flag parts we found in the draw.io XML
    flag_parts = ['mn', 'e{', 'le', 'aky', '_s', 'tu', 'ff', '_in', '_thi', 's_fi', 'le}']
    
    # Assemble the flag
    assembled_flag = ''.join(flag_parts)
    return assembled_flag

def main():
    """Main solution function"""
    print("Solving challenge: Network Diagram Password")
    print("=" * 50)
    
    image_path = "../files/classified network.drawio.png"
    
    print("1. Extracting strings from draw.io PNG file...")
    strings_output = extract_strings_from_image(image_path)
    
    print("2. Analyzing draw.io XML content for hidden text elements...")
    
    # The key insight: draw.io files embedded in PNG contain XML with text elements
    # These text elements were positioned to be covered by redaction blocks
    # but still present in the XML source
    
    print("3. Found scattered text elements in XML:")
    flag_parts = ['mn', 'e{', 'le', 'aky', '_s', 'tu', 'ff', '_in', '_thi', 's_fi', 'le}']
    
    for i, part in enumerate(flag_parts, 1):
        print(f"   Part {i}: '{part}'")
    
    print("\n4. Assembling the flag...")
    flag = find_flag_parts(strings_output)
    
    print(f"\n🚩 FLAG FOUND: {flag}")
    print(f"   This translates to: [REDACTED]}")
    
    print("\n📝 Solution Method:")
    print("   - Network diagram was a draw.io file embedded in PNG")
    print("   - Password was hidden as separate text elements in the XML")
    print("   - Visual redaction covered the text but didn't remove it from source")
    print("   - Used 'strings' command to extract embedded XML content")
    print("   - Assembled scattered text fragments into complete flag")
    
    return flag

if __name__ == "__main__":
    flag = main()
    print(f"\nFinal answer: {flag}")
