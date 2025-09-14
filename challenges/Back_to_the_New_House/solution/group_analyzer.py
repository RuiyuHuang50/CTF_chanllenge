#!/usr/bin/env python3
"""
Windows Event Log Analyzer for Back to the New House Challenge
Find group creation events in Windows Event Logs
"""

import struct
import xml.etree.ElementTree as ET
import sys
import re
from datetime import datetime

def parse_evtx_simple(filepath):
    """Simple EVTX parser to extract readable strings"""
    print(f"🔍 Analyzing {filepath}")
    
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Look for XML-like structures in the binary data
        # EVTX files contain XML data embedded in binary format
        
        # Try to find XML patterns
        xml_patterns = []
        
        # Look for Event XML structures
        event_pattern = rb'<Event xmlns'
        start_pos = 0
        
        while True:
            pos = content.find(event_pattern, start_pos)
            if pos == -1:
                break
            
            # Try to find the end of this XML block
            end_pos = content.find(b'</Event>', pos)
            if end_pos != -1:
                end_pos += len(b'</Event>')
                xml_data = content[pos:end_pos]
                try:
                    # Try to decode as UTF-16 or UTF-8
                    xml_str = xml_data.decode('utf-16le', errors='ignore')
                    if '<Event' in xml_str:
                        xml_patterns.append(xml_str)
                except:
                    try:
                        xml_str = xml_data.decode('utf-8', errors='ignore')
                        if '<Event' in xml_str:
                            xml_patterns.append(xml_str)
                    except:
                        pass
            
            start_pos = pos + 1
        
        print(f"📊 Found {len(xml_patterns)} potential XML event blocks")
        
        # Analyze XML patterns for group creation
        group_events = []
        for i, xml_str in enumerate(xml_patterns):
            if any(keyword in xml_str.lower() for keyword in ['group', 'created', '4727', '4731']):
                group_events.append(xml_str)
                print(f"📋 Event {i+1} contains group-related content")
        
        return group_events
        
    except Exception as e:
        print(f"❌ Error parsing {filepath}: {e}")
        return []

def extract_group_names(xml_events):
    """Extract group names from XML events"""
    print("🔍 Extracting group names from events...")
    
    group_names = []
    
    for xml_str in xml_events:
        # Look for group name patterns
        group_patterns = [
            r'<Data Name="TargetUserName">([^<]+)</Data>',
            r'<Data Name="GroupName">([^<]+)</Data>',
            r'<Data Name="SamAccountName">([^<]+)</Data>',
            r'Group Name:\s*([^\r\n]+)',
            r'Target Account Name:\s*([^\r\n]+)'
        ]
        
        for pattern in group_patterns:
            matches = re.findall(pattern, xml_str, re.IGNORECASE)
            for match in matches:
                group_name = match.strip()
                if group_name and group_name not in group_names:
                    print(f"🎯 Found potential group name: {group_name}")
                    group_names.append(group_name)
    
    return group_names

def analyze_binary_content(filepath):
    """Analyze binary content for group-related strings"""
    print(f"🔍 Binary analysis of {filepath}")
    
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Look for UTF-16 encoded strings (common in Windows)
        utf16_strings = []
        
        # Decode as UTF-16LE and look for readable text
        try:
            decoded = content.decode('utf-16le', errors='ignore')
            # Find words that might be group names
            words = re.findall(r'[A-Za-z][A-Za-z0-9_-]{2,20}', decoded)
            
            # Filter for potential group names
            potential_groups = []
            for word in words:
                if any(keyword in word.lower() for keyword in ['group', 'admin', 'user', 'guest', 'power', 'backup']):
                    if word not in potential_groups:
                        potential_groups.append(word)
            
            if potential_groups:
                print("🎯 Potential group-related names found:")
                for group in potential_groups[:20]:  # Show first 20
                    print(f"  - {group}")
                    
            return potential_groups
            
        except Exception as e:
            print(f"❌ UTF-16 decode error: {e}")
            return []
            
    except Exception as e:
        print(f"❌ Error in binary analysis: {e}")
        return []

def main():
    print("🕵️  Windows Event Log Group Analyzer")
    print("=" * 60)
    
    # Analyze Security.evtx first (most likely to contain group creation events)
    security_log = "Security.evtx"
    
    print(f"\n📂 Analyzing {security_log} for group creation events...")
    
    # Try XML parsing approach
    xml_events = parse_evtx_simple(security_log)
    
    if xml_events:
        group_names = extract_group_names(xml_events)
        if group_names:
            print(f"\n🏁 GROUP NAMES FOUND:")
            for name in group_names:
                print(f"  ✅ {name}")
    
    # Try binary analysis approach
    print(f"\n📂 Binary analysis of {security_log}...")
    binary_groups = analyze_binary_content(security_log)
    
    # Also check other log files
    other_logs = ["System.evtx", "Application.evtx", "Setup.evtx"]
    
    for log in other_logs:
        print(f"\n📂 Quick check of {log}...")
        groups = analyze_binary_content(log)
        if groups:
            print(f"Found {len(groups)} potential group names in {log}")
    
    print("\n💡 SUMMARY:")
    print("💡 Look for group names in the output above")
    print("💡 Common Windows group creation events use Event IDs 4727, 4731")
    print("💡 Group names are typically in TargetUserName or GroupName fields")

if __name__ == "__main__":
    main()
