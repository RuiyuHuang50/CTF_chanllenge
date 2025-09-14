#!/usr/bin/env python3
import re

program_path = "/Users/mac/VirtualBox VMs/CTF_chanllenge/intro04/program"

print("🔍 Searching for flag patterns in the binary...")
print("=" * 50)

try:
    with open(program_path, 'rb') as f:
        content = f.read()
        
    # Convert to string for searching, ignore errors
    text_content = content.decode('utf-8', errors='ignore')
    
    # Common flag patterns
    flag_patterns = [
        r'FLAG\{[^}]+\}',
        r'flag\{[^}]+\}',
        r'CTF\{[^}]+\}',
        r'ctf\{[^}]+\}',
        r'BOOTUP\{[^}]+\}',
        r'bootup\{[^}]+\}',
        r'\{[^}]{20,}\}',  # Any long content in braces
    ]
    
    found_flags = []
    
    for pattern in flag_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        found_flags.extend(matches)
    
    if found_flags:
        print("🏁 Found potential flags:")
        for flag in set(found_flags):  # Remove duplicates
            print(f"   {flag}")
    else:
        print("❌ No obvious flag patterns found")
        
    # Also search for any printable strings that might contain the flag
    print("\n🔍 Searching for strings containing 'flag', 'ctf', or 'bootup'...")
    
    # Extract printable strings
    printable_strings = []
    current_string = ""
    
    for byte in content:
        if 32 <= byte <= 126:  # Printable ASCII
            current_string += chr(byte)
        else:
            if len(current_string) >= 4:  # Only keep strings of 4+ chars
                printable_strings.append(current_string)
            current_string = ""
    
    # Add final string if exists
    if len(current_string) >= 4:
        printable_strings.append(current_string)
    
    # Search for interesting strings
    interesting_strings = []
    for s in printable_strings:
        if any(keyword in s.lower() for keyword in ['flag', 'ctf', 'bootup', 'challenge']):
            interesting_strings.append(s)
    
    if interesting_strings:
        print("📝 Interesting strings found:")
        for s in interesting_strings:
            print(f"   {s}")
    else:
        print("❌ No interesting strings found")
        
    # Show some sample strings for context
    print(f"\n📊 Total printable strings found: {len(printable_strings)}")
    print("📝 Sample strings from the binary:")
    for i, s in enumerate(printable_strings[:20]):  # Show first 20
        print(f"   {i+1}: {s}")
        
except Exception as e:
    print(f"❌ Error analyzing binary: {e}")
