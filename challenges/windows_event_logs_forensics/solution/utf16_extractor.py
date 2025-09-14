#!/usr/bin/env python3
"""
UTF-16 String Extractor for Windows EVTX files
Extract hostname information from Windows Event Logs
"""

import re

def extract_utf16_strings(filename):
    """Extract UTF-16 strings from binary file"""
    print(f"Extracting UTF-16 strings from {filename}...")
    
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        
        # Look for UTF-16LE patterns (null byte after each ASCII char)
        utf16_strings = []
        
        # Pattern: ASCII char followed by null byte, repeated
        i = 0
        while i < len(data) - 8:  # Need at least 8 bytes for a 4-char string
            if data[i] != 0 and data[i+1] == 0:  # Potential UTF-16LE start
                string_bytes = []
                j = i
                while j < len(data) - 1 and data[j] != 0 and data[j+1] == 0:
                    if 32 <= data[j] <= 126:  # Printable ASCII
                        string_bytes.append(data[j])
                        j += 2
                    else:
                        break
                
                if len(string_bytes) >= 4:  # At least 4 characters
                    try:
                        string_val = bytes(string_bytes).decode('ascii')
                        utf16_strings.append(string_val)
                    except:
                        pass
                
                i = j
            else:
                i += 1
        
        return utf16_strings
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def analyze_strings_for_hostnames(strings_list):
    """Analyze extracted strings for potential hostnames"""
    print(f"Analyzing {len(strings_list)} UTF-16 strings...")
    
    potential_hostnames = []
    
    for s in strings_list:
        # Look for hostname-like patterns
        if re.match(r'^[A-Z][A-Z0-9\-]{3,15}$', s):
            # Exclude common system/XML strings
            exclude = {
                'EVENT', 'DATA', 'SYSTEM', 'SECURITY', 'APPLICATION', 'XML',
                'XMLNS', 'HTTP', 'SCHEMA', 'MICROSOFT', 'WINDOWS', 'VERSION',
                'ENCODING', 'PROVIDER', 'CHANNEL', 'COMPUTER', 'EVENTDATA',
                'TASK', 'OPCODE', 'KEYWORDS', 'LEVEL', 'USERID', 'PROCESSID',
                'THREADID', 'PROCESSOR', 'SESSION', 'KERNEL', 'USER', 'GUID',
                'CORRELATION', 'EXECUTION', 'NAMESPACE', 'ELEMENT', 'ATTRIBUTE'
            }
            
            if s not in exclude:
                potential_hostnames.append(s)
    
    return potential_hostnames

def main():
    filename = 'Security.evtx'
    
    print("Advanced UTF-16 EVTX Analysis")
    print("=" * 40)
    
    # Extract UTF-16 strings
    utf16_strings = extract_utf16_strings(filename)
    
    if utf16_strings:
        print(f"Found {len(utf16_strings)} UTF-16 strings")
        
        # Show some samples
        print("\nSample UTF-16 strings found:")
        for i, s in enumerate(utf16_strings[:20]):
            print(f"  {i+1}: {s}")
        
        # Look for hostnames
        hostnames = analyze_strings_for_hostnames(utf16_strings)
        
        if hostnames:
            print(f"\nPotential hostnames found:")
            from collections import Counter
            hostname_counts = Counter(hostnames)
            
            for hostname, count in hostname_counts.most_common():
                print(f"  {hostname}: {count} occurrences")
            
            # Most likely candidate
            top_hostname = hostname_counts.most_common(1)[0][0]
            flag = f"[REDACTED]}}"
            
            print(f"\n🚩 POTENTIAL FLAG: {flag}")
            return flag
        else:
            print("\nNo clear hostname patterns found in UTF-16 strings")
            
            # Show unique strings that might be relevant
            unique_strings = list(set(utf16_strings))
            relevant = [s for s in unique_strings if len(s) >= 4 and s.isalnum()]
            
            print(f"\nOther relevant strings ({len(relevant)} found):")
            for s in sorted(relevant)[:30]:
                print(f"  {s}")
    
    else:
        print("No UTF-16 strings found")
    
    return None

if __name__ == "__main__":
    flag = main()
