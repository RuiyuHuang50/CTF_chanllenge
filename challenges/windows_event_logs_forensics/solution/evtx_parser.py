#!/usr/bin/env python3
"""
Proper EVTX Parser for Windows Event Logs
Parse Security.evtx to find attacker hostname from logon events
"""

try:
    import evtx
    import evtx.Evtx as Evtx
    import evtx.Views as e_views
    from xml.etree import ElementTree as ET
    EVTX_AVAILABLE = True
except ImportError:
    EVTX_AVAILABLE = False

import xml.etree.ElementTree as ET
import re
from collections import Counter

def parse_evtx_with_library(filename):
    """Parse EVTX using python-evtx library"""
    print("Parsing EVTX with python-evtx library...")
    
    try:
        with Evtx.Evtx(filename) as log:
            hostnames = []
            logon_events = []
            
            for record in log.records():
                try:
                    xml_content = record.xml()
                    root = ET.fromstring(xml_content)
                    
                    # Look for Event ID 4624 (successful logon)
                    event_id_elem = root.find('.//{http://schemas.microsoft.com/win/2004/08/events/event}EventID')
                    if event_id_elem is not None and event_id_elem.text == '4624':
                        
                        # Extract all data from the event
                        data_elems = root.findall('.//{http://schemas.microsoft.com/win/2004/08/events/event}Data')
                        event_data = {}
                        
                        for data in data_elems:
                            name = data.get('Name', '')
                            value = data.text or ''
                            event_data[name] = value
                        
                        logon_events.append(event_data)
                        
                        # Look for WorkstationName specifically
                        if 'WorkstationName' in event_data and event_data['WorkstationName']:
                            workstation = event_data['WorkstationName'].strip()
                            if workstation and workstation != '-':
                                hostnames.append(workstation)
                                print(f"Found WorkstationName: {workstation}")
                        
                        # Also check IpAddress for remote connections
                        if 'IpAddress' in event_data:
                            ip = event_data['IpAddress']
                            if ip and ip not in ['127.0.0.1', '::1', '-']:
                                print(f"Found remote IP: {ip}")
                
                except Exception as e:
                    continue
            
            print(f"\nTotal logon events (4624): {len(logon_events)}")
            
            if hostnames:
                hostname_counts = Counter(hostnames)
                print(f"\nWorkstation names found:")
                for hostname, count in hostname_counts.most_common():
                    print(f"  {hostname}: {count} times")
                
                most_common = hostname_counts.most_common(1)[0][0]
                flag = f"[REDACTED]}}"
                print(f"\n🚩 FLAG: {flag}")
                return flag
            else:
                print("No workstation names found in logon events")
                
                # Show sample event data
                if logon_events:
                    print("\nSample logon event data:")
                    for key, value in list(logon_events[0].items())[:10]:
                        print(f"  {key}: {value}")
                
                return None
                
    except Exception as e:
        print(f"Error parsing EVTX: {e}")
        return None

def manual_xml_extraction(filename):
    """Manual XML extraction as fallback"""
    print("Attempting manual XML extraction...")
    
    try:
        with open(filename, 'rb') as f:
            content = f.read()
        
        # Look for XML-like patterns
        xml_patterns = []
        
        # Search for Event elements
        for match in re.finditer(b'<Event[^>]*>.*?</Event>', content, re.DOTALL):
            xml_patterns.append(match.group(0))
        
        print(f"Found {len(xml_patterns)} potential XML patterns")
        
        if xml_patterns:
            for i, pattern in enumerate(xml_patterns[:3]):
                try:
                    # Try to decode as UTF-16 or UTF-8
                    xml_str = pattern.decode('utf-16le', errors='ignore')
                    print(f"\nXML Pattern {i+1}:")
                    print(xml_str[:500] + "..." if len(xml_str) > 500 else xml_str)
                except:
                    xml_str = pattern.decode('utf-8', errors='ignore')
                    print(f"\nXML Pattern {i+1} (UTF-8):")
                    print(xml_str[:500] + "..." if len(xml_str) > 500 else xml_str)
        
        return None
        
    except Exception as e:
        print(f"Error in manual extraction: {e}")
        return None

def main():
    filename = 'Security.evtx'
    
    print("Advanced EVTX Analysis for Hostname Detection")
    print("=" * 50)
    
    if EVTX_AVAILABLE:
        flag = parse_evtx_with_library(filename)
        if flag:
            return flag
    else:
        print("python-evtx library not available, trying manual extraction...")
    
    # Fallback to manual extraction
    manual_xml_extraction(filename)
    
    return None

if __name__ == "__main__":
    flag = main()
