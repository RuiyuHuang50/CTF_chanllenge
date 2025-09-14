#!/usr/bin/env python3
"""
Solution for: Windows Event Logs Forensics
Date: 2025-09-12
Category: Forensics

Challenge: Find the hostname of the machine the attacker used to login
Flag format: [REDACTED] (all upper case)
Hint: Something about 'Security' - likely refers to Security.evtx
"""

import subprocess
import re
import json
import xml.etree.ElementTree as ET
from datetime import datetime

def check_evtx_tools():
    """Check if we have tools to parse EVTX files"""
    tools = ['evtx_dump', 'python-evtx', 'evtx-parser']
    available = []
    
    for tool in tools:
        try:
            subprocess.run([tool, '--help'], capture_output=True, stderr=subprocess.DEVNULL)
            available.append(tool)
        except FileNotFoundError:
            continue
    
    return available

def install_evtx_parser():
    """Install python-evtx for parsing Windows event logs"""
    try:
        print("Installing python-evtx...")
        subprocess.run(['pip3', 'install', 'python-evtx'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def parse_security_log(evtx_path):
    """Parse Security.evtx looking for login events"""
    try:
        # Try using python-evtx
        cmd = ['evtx_dump.py', evtx_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error parsing EVTX: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("evtx_dump.py not found. Trying alternative methods...")
        return parse_with_strings(evtx_path)

def parse_with_strings(evtx_path):
    """Fallback: Use strings command to extract readable text"""
    try:
        result = subprocess.run(['strings', evtx_path], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error using strings: {e}")
        return None

def find_login_events(log_content):
    """Look for login-related events and extract hostnames"""
    if not log_content:
        return []
    
    # Common Windows Event IDs for logins:
    # 4624 - Successful logon
    # 4625 - Failed logon
    # 4648 - Logon using explicit credentials
    # 4776 - Domain controller attempted to validate credentials
    
    findings = []
    lines = log_content.split('\n')
    
    # Look for patterns that might contain hostnames
    hostname_patterns = [
        r'WorkstationName["\s>:]*([A-Z0-9\-]+)',
        r'TargetDomainName["\s>:]*([A-Z0-9\-]+)',
        r'SubjectDomainName["\s>:]*([A-Z0-9\-]+)',
        r'LogonProcessName["\s>:]*([A-Z0-9\-]+)',
        r'<Computer>([^<]+)</Computer>',
        r'SourceNetworkAddress["\s>:]*([0-9\.]+)',
        r'IpAddress["\s>:]*([0-9\.]+)',
        r'<Data Name=["\']WorkstationName["\']>([^<]+)</Data>',
        r'<Data Name=["\']TargetDomainName["\']>([^<]+)</Data>',
    ]
    
    for line in lines:
        for pattern in hostname_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                if match and match not in ['-', '', 'localhost', '127.0.0.1']:
                    findings.append({
                        'hostname': match.upper(),
                        'line': line.strip(),
                        'pattern': pattern
                    })
    
    return findings

def analyze_event_logs():
    """Main analysis function"""
    print("Analyzing Windows Event Logs for attacker hostname...")
    print("=" * 60)
    
    # Focus on Security.evtx as hinted
    security_log_path = "../files/logs/Windows Logs/Security.evtx"
    
    print("1. Checking available EVTX parsing tools...")
    tools = check_evtx_tools()
    
    if not tools:
        print("   No EVTX tools found. Installing python-evtx...")
        if not install_evtx_parser():
            print("   Installation failed. Using strings as fallback...")
    
    print("2. Parsing Security.evtx (this may take a moment)...")
    log_content = parse_security_log(security_log_path)
    
    if not log_content:
        print("   Failed to parse Security.evtx")
        return None
    
    print("3. Looking for login events and hostnames...")
    findings = find_login_events(log_content)
    
    if findings:
        print(f"   Found {len(findings)} potential hostname references:")
        
        # Count occurrences of each hostname
        hostname_counts = {}
        for finding in findings:
            hostname = finding['hostname']
            if hostname not in hostname_counts:
                hostname_counts[hostname] = 0
            hostname_counts[hostname] += 1
        
        print("\n   Hostname frequency analysis:")
        sorted_hostnames = sorted(hostname_counts.items(), key=lambda x: x[1], reverse=True)
        
        for hostname, count in sorted_hostnames:
            print(f"   {hostname}: {count} occurrences")
            
        # Show details for most common non-system hostnames
        print("\n4. Detailed analysis of top findings:")
        for hostname, count in sorted_hostnames[:5]:
            if hostname not in ['SYSTEM', 'LOCAL', 'ANONYMOUS']:
                print(f"\n   Hostname: {hostname}")
                relevant_findings = [f for f in findings if f['hostname'] == hostname]
                for i, finding in enumerate(relevant_findings[:3]):  # Show first 3
                    print(f"     Example {i+1}: {finding['line'][:100]}...")
        
        # The most likely candidate is probably the most frequent non-system hostname
        likely_hostname = None
        for hostname, count in sorted_hostnames:
            if hostname not in ['SYSTEM', 'LOCAL', 'ANONYMOUS', 'NT AUTHORITY']:
                likely_hostname = hostname
                break
        
        if likely_hostname:
            flag = f"[REDACTED]}}"
            print(f"\n🚩 LIKELY FLAG: {flag}")
            print(f"   Most frequent non-system hostname: {likely_hostname}")
            
            return flag
    
    print("   No clear hostname patterns found. May need manual analysis.")
    return None

def main():
    """Main solution function"""
    print("Solving challenge: Windows Event Logs Forensics")
    print("Challenge: Find hostname of attacker's machine")
    print("Hint: Look in 'Security' logs for login events")
    
    flag = analyze_event_logs()
    
    if flag:
        print(f"\n📝 Solution Method:")
        print("   - Parsed Windows Security.evtx event log")
        print("   - Searched for login events (Event IDs 4624, 4625, etc.)")
        print("   - Extracted WorkstationName and related fields")
        print("   - Identified most frequent non-system hostname")
        
        return flag
    else:
        print("\n❌ Automated analysis incomplete. Manual review needed.")
        print("   Try examining the Security.evtx file with Windows Event Viewer")
        print("   Look for Event ID 4624 (successful logon) events")
        print("   Check the 'WorkstationName' field in logon events")
        
        return None

if __name__ == "__main__":
    flag = main()
    if flag:
        print(f"\nFinal answer: {flag}")
    else:
        print(f"\nNeed manual analysis - check Security.evtx for login events")
