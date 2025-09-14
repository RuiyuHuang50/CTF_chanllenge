#!/usr/bin/env python3
"""
Advanced EVTX Analysis Script
Look for hostname patterns in Windows Event Logs using multiple methods
"""

import os
import re
import subprocess
from collections import Counter

def analyze_evtx_with_strings(evtx_path):
    """Use strings command to extract readable text and look for hostnames"""
    print("Analyzing EVTX file with strings command...")
    
    try:
        # Get all strings from the file
        result = subprocess.run(['strings', '-a', '-n', '3', evtx_path], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error running strings: {result.stderr}")
            return []
        
        content = result.stdout
        lines = content.split('\n')
        
        print(f"Extracted {len(lines)} text strings from EVTX file")
        
        # Look for potential hostnames and computer names
        hostname_patterns = [
            r'\b([A-Z][A-Z0-9\-]{2,15})\b',  # Typical Windows hostname pattern
            r'WorkstationName[>:"\s]*([A-Z0-9\-]+)',
            r'TargetDomainName[>:"\s]*([A-Z0-9\-]+)', 
            r'SubjectDomainName[>:"\s]*([A-Z0-9\-]+)',
            r'Computer[>:"\s]*([A-Z0-9\-\.]+)',
            r'SourceNetworkAddress[>:"\s]*([0-9\.]+)',
            r'<Computer>([^<]+)</Computer>',
            r'<Data[^>]*>([A-Z0-9\-]+)</Data>',
        ]
        
        potential_hostnames = []
        
        for line in lines:
            # Skip very short lines or lines that look like noise
            if len(line.strip()) < 3:
                continue
                
            for pattern in hostname_patterns:
                matches = re.findall(pattern, line, re.IGNORECASE)
                for match in matches:
                    if match and len(match) > 2:
                        # Filter out common false positives
                        if match.upper() not in ['SYSTEM', 'LOCAL', 'ANONYMOUS', 'NT', 'AUTHORITY', 
                                               'SERVICE', 'NETWORK', 'BATCH', 'INTERACTIVE',
                                               'MICROSOFT', 'WINDOWS', 'CORP', 'DOMAIN']:
                            potential_hostnames.append({
                                'hostname': match.upper(),
                                'context': line.strip()[:100],
                                'pattern': pattern
                            })
        
        return potential_hostnames
        
    except Exception as e:
        print(f"Error analyzing EVTX: {e}")
        return []

def analyze_specific_events(evtx_path):
    """Look for specific Windows logon events"""
    print("Looking for Windows logon events...")
    
    try:
        result = subprocess.run(['strings', '-a', evtx_path], 
                              capture_output=True, text=True)
        content = result.stdout
        
        # Look for Event ID 4624 (successful logon) patterns
        logon_events = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if '4624' in line or 'successful' in line.lower():
                # Look at surrounding lines for hostname info
                context_start = max(0, i-5)
                context_end = min(len(lines), i+5)
                context = '\n'.join(lines[context_start:context_end])
                
                # Extract potential hostnames from context
                hostname_matches = re.findall(r'\b([A-Z][A-Z0-9\-]{3,12})\b', context)
                for hostname in hostname_matches:
                    if hostname not in ['SYSTEM', 'LOCAL', 'SERVICE', 'NETWORK']:
                        logon_events.append({
                            'hostname': hostname,
                            'context': context,
                            'event_line': line
                        })
        
        return logon_events
        
    except Exception as e:
        print(f"Error looking for logon events: {e}")
        return []

def main():
    evtx_path = "../files/logs/Windows Logs/Security.evtx"
    
    if not os.path.exists(evtx_path):
        print(f"EVTX file not found: {evtx_path}")
        return
    
    print("Advanced EVTX Analysis")
    print("=" * 50)
    print(f"Analyzing: {evtx_path}")
    
    # Method 1: General hostname extraction
    print("\n1. General hostname pattern analysis:")
    hostnames = analyze_evtx_with_strings(evtx_path)
    
    if hostnames:
        # Count frequency of each hostname
        hostname_counts = Counter(h['hostname'] for h in hostnames)
        
        print(f"Found {len(hostnames)} potential hostname references")
        print("\nTop hostnames by frequency:")
        
        for hostname, count in hostname_counts.most_common(10):
            print(f"  {hostname}: {count} occurrences")
            
            # Show some context for this hostname
            examples = [h for h in hostnames if h['hostname'] == hostname][:2]
            for example in examples:
                print(f"    Context: {example['context']}")
        
        # Method 2: Logon event specific analysis
        print("\n2. Logon event analysis:")
        logon_events = analyze_specific_events(evtx_path)
        
        if logon_events:
            logon_hostnames = Counter(e['hostname'] for e in logon_events)
            print(f"Found {len(logon_events)} logon-related hostname references")
            
            for hostname, count in logon_hostnames.most_common(5):
                print(f"  Logon from {hostname}: {count} times")
        
        # Determine most likely answer
        print("\n3. Analysis Summary:")
        
        # Combine both analyses, giving more weight to logon events
        all_candidates = list(hostname_counts.keys())
        if logon_events:
            logon_hostnames = Counter(e['hostname'] for e in logon_events)
            # Prioritize hostnames found in logon events
            for hostname in logon_hostnames.keys():
                if hostname in all_candidates:
                    hostname_counts[hostname] += logon_hostnames[hostname] * 2  # Double weight
        
        # Get the most likely candidate
        if hostname_counts:
            top_hostname = hostname_counts.most_common(1)[0][0]
            flag = f"[REDACTED]}}"
            
            print(f"\n🚩 MOST LIKELY FLAG: {flag}")
            print(f"   Based on frequency analysis and logon event correlation")
            
            return flag
    
    print("\nNo clear hostname patterns found. Manual analysis may be needed.")
    return None

if __name__ == "__main__":
    flag = main()
    if flag:
        print(f"\nRecommended answer: {flag}")
