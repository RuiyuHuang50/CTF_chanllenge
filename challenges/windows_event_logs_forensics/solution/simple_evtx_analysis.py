#!/usr/bin/env python3
"""
Simple EVTX Analysis - Focus on finding workstation names
"""

import re
import struct

def extract_all_strings(filename):
    """Extract all possible strings from the EVTX file"""
    print(f"Analyzing {filename}...")
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    # ASCII strings
    ascii_strings = []
    current_string = ""
    for byte in data:
        if 32 <= byte <= 126:  # Printable ASCII
            current_string += chr(byte)
        else:
            if len(current_string) >= 4:
                ascii_strings.append(current_string)
            current_string = ""
    
    # UTF-16LE strings (every other byte is null)
    utf16_strings = []
    i = 0
    while i < len(data) - 8:
        if data[i] != 0 and data[i+1] == 0:  # Potential UTF-16LE
            string_chars = []
            j = i
            while j < len(data) - 1:
                if data[j] != 0 and data[j+1] == 0 and 32 <= data[j] <= 126:
                    string_chars.append(chr(data[j]))
                    j += 2
                else:
                    break
            
            if len(string_chars) >= 4:
                utf16_strings.append(''.join(string_chars))
            i = j
        else:
            i += 1
    
    return ascii_strings, utf16_strings

def find_hostnames(strings_list):
    """Find potential hostnames in string list"""
    hostnames = []
    
    # Common hostname patterns
    hostname_patterns = [
        r'^[A-Z][A-Z0-9\-]{2,15}$',  # Standard hostname format
        r'^[A-Z0-9]{3,15}$',         # Alphanumeric only
        r'^WIN-[A-Z0-9]{10}$',       # Windows default format
        r'^DESKTOP-[A-Z0-9]{7}$',    # Windows 10 format
    ]
    
    # Exclude common system strings
    exclude_patterns = [
        'SYSTEM', 'LOCAL', 'SERVICE', 'ANONYMOUS', 'NETWORK', 
        'INTERACTIVE', 'BATCH', 'REMOTE', 'PROXY', 'NULL',
        'SECURITY', 'APPLICATION', 'WINDOWS', 'MICROSOFT',
        'EVENT', 'DATA', 'XML', 'XMLNS', 'HTTP', 'SCHEMA',
        'VERSION', 'ENCODING', 'PROVIDER', 'CHANNEL', 'COMPUTER',
        'EVENTDATA', 'TASK', 'OPCODE', 'KEYWORDS', 'LEVEL',
        'USERID', 'PROCESSID', 'THREADID', 'PROCESSOR', 'SESSION',
        'KERNEL', 'USER', 'GUID', 'CORRELATION', 'EXECUTION'
    ]
    
    for s in strings_list:
        # Check if it matches hostname patterns
        for pattern in hostname_patterns:
            if re.match(pattern, s):
                if s not in exclude_patterns and not any(excl in s for excl in exclude_patterns):
                    hostnames.append(s)
                break
    
    return hostnames

def main():
    filename = 'Security.evtx'
    
    print("Simple EVTX Hostname Analysis")
    print("=" * 40)
    
    # Extract strings
    ascii_strings, utf16_strings = extract_all_strings(filename)
    
    print(f"Found {len(ascii_strings)} ASCII strings")
    print(f"Found {len(utf16_strings)} UTF-16 strings")
    
    # Combine all strings
    all_strings = ascii_strings + utf16_strings
    
    # Find hostnames
    hostnames = find_hostnames(all_strings)
    
    if hostnames:
        from collections import Counter
        hostname_counts = Counter(hostnames)
        
        print(f"\nPotential hostnames found:")
        for hostname, count in hostname_counts.most_common():
            print(f"  {hostname}: {count} occurrences")
        
        # Check if there's a clear winner (not NOTA)
        top_candidates = [h for h, c in hostname_counts.most_common(5) if h != 'NOTA']
        
        if top_candidates:
            print(f"\nTop non-NOTA candidates:")
            for hostname in top_candidates[:3]:
                count = hostname_counts[hostname]
                flag = f"[REDACTED]}}"
                print(f"  {hostname} ({count}x) -> {flag}")
        
        print(f"\n🚩 Try these flags:")
        for hostname in top_candidates[:3]:
            print(f"   [REDACTED]}}")
    
    else:
        print("\nNo clear hostname patterns found")
        
        # Show some unique strings for manual inspection
        unique_strings = list(set(all_strings))
        interesting = [s for s in unique_strings if 3 <= len(s) <= 20 and s.isalnum() and s != 'NOTA']
        
        print(f"\nOther interesting strings:")
        for s in sorted(interesting)[:20]:
            print(f"  {s}")

if __name__ == "__main__":
    main()
