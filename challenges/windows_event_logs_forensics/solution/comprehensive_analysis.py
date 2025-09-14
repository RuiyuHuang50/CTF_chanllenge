#!/usr/bin/env python3
"""
Comprehensive EVTX hostname extraction for Windows Event Logs forensics
"""

import subprocess
import re
from collections import Counter

def extract_from_evtx(filename):
    """Extract potential hostnames from EVTX file"""
    print(f"\n=== Analyzing {filename} ===")
    
    try:
        # Get strings from the file
        result = subprocess.run(['strings', '-a', filename], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error processing {filename}")
            return []
        
        content = result.stdout
        
        # Look for hostname patterns
        patterns = [
            r'\b([A-Z][A-Z0-9\-]{3,15})\b',  # General hostname pattern
            r'[">]([A-Z][A-Z0-9\-]{3,12})[<"]',  # XML enclosed
            r'=([A-Z][A-Z0-9\-]{3,12})',  # After equals sign
        ]
        
        candidates = []
        for pattern in patterns:
            matches = re.findall(pattern, content)
            candidates.extend(matches)
        
        # Filter out common system strings
        filtered = []
        exclude = {
            'SYSTEM', 'SERVICE', 'NETWORK', 'LOCAL', 'ANONYMOUS', 'AUTHORITY', 
            'MICROSOFT', 'WINDOWS', 'SECURITY', 'APPLICATION', 'DOMAIN', 'CONTROL', 
            'POLICY', 'EVENT', 'DATA', 'RECORD', 'USER', 'GROUP', 'OBJECT', 'ACCESS',
            'PRIVILEGE', 'PROCESS', 'THREAD', 'TOKEN', 'HANDLE', 'VALUE', 'TYPE',
            'CLASS', 'INSTANCE', 'PROPERTY', 'METHOD', 'ASSEMBLY', 'MODULE',
            'NAMESPACE', 'EXCEPTION', 'ERROR', 'WARNING', 'INFORMATION', 'CRITICAL',
            'VERBOSE', 'DEBUG', 'TRACE', 'SUCCESS', 'FAILURE', 'AUDIT', 'LOGON',
            'LOGOFF', 'INTERACTIVE', 'BATCH', 'UNLOCKED', 'LOCKED', 'WORKSTATION',
            'SERVER', 'CLIENT', 'ADMIN', 'GUEST', 'NULL', 'NONE', 'TRUE', 'FALSE'
        }
        
        for candidate in candidates:
            if candidate.upper() not in exclude and len(candidate) >= 4:
                filtered.append(candidate.upper())
        
        return filtered
        
    except Exception as e:
        print(f"Error analyzing {filename}: {e}")
        return []

def main():
    print("Comprehensive Windows Event Log Hostname Analysis")
    print("=" * 55)
    
    # Analyze all available log files
    log_files = [
        'Security.evtx',
        'System.evtx', 
        'Application.evtx'
    ]
    
    all_hostnames = []
    
    for log_file in log_files:
        try:
            hostnames = extract_from_evtx(log_file)
            all_hostnames.extend(hostnames)
            
            if hostnames:
                counts = Counter(hostnames)
                print(f"  Found hostnames: {dict(counts)}")
            else:
                print(f"  No hostnames found")
                
        except FileNotFoundError:
            print(f"  {log_file} not found")
    
    if all_hostnames:
        print(f"\n=== SUMMARY ===")
        hostname_counts = Counter(all_hostnames)
        
        print("All discovered hostnames (by frequency):")
        for hostname, count in hostname_counts.most_common():
            print(f"  {hostname}: {count} occurrences")
        
        # Most likely candidate
        top_hostname = hostname_counts.most_common(1)[0][0]
        flag = f"[REDACTED]}}"
        
        print(f"\n🚩 MOST LIKELY FLAG: {flag}")
        print(f"   Based on: {top_hostname} appearing {hostname_counts[top_hostname]} times")
        
        return flag
    else:
        print("\n❌ No hostnames found in any log files")
        
        # Fallback: show what we did find
        print("\nLet's see what uppercase strings we found:")
        for log_file in log_files:
            try:
                result = subprocess.run(['strings', '-a', log_file], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    # Find any uppercase strings
                    matches = re.findall(r'\b[A-Z]{3,8}\b', result.stdout)
                    if matches:
                        counts = Counter(matches)
                        print(f"{log_file}: {dict(counts.most_common(5))}")
            except:
                continue
                
        return None

if __name__ == "__main__":
    flag = main()
    if flag:
        print(f"\nRecommended answer: {flag}")
    else:
        print(f"\nManual analysis required")
