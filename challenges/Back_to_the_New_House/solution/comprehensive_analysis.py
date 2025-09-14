#!/usr/bin/env python3
"""
Comprehensive Analysis Script for Back to the New House Challenge
Questions 4-13
"""

import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile
import os

def analyze_task_scheduler():
    """Analyze TaskScheduler events for created and deleted tasks"""
    tasks_created = []
    tasks_deleted = []
    
    try:
        with open('taskscheduler_dump.xml', 'r') as f:
            content = f.read()
        
        # Parse XML for task creation and deletion events
        import re
        
        # Find task creation events (TaskRegisteredEvent)
        creation_pattern = r'<EventData Name="TaskRegisteredEvent">.*?<Data Name="TaskName">([^<]+)</Data>'
        for match in re.finditer(creation_pattern, content, re.DOTALL):
            task_name = match.group(1)
            tasks_created.append(task_name)
            
        # Find task deletion events (TaskDeleted)
        deletion_pattern = r'<EventData Name="TaskDeleted">.*?<Data Name="TaskName">([^<]+)</Data>'
        for match in re.finditer(deletion_pattern, content, re.DOTALL):
            task_name = match.group(1)
            tasks_deleted.append(task_name)
            
    except Exception as e:
        print(f"❌ Error analyzing task scheduler: {e}")
    
    return tasks_created, tasks_deleted

def analyze_network_traffic():
    """Questions 6-8: Network analysis for OS, tools, ports"""
    print("\n🌐 Analyzing Network Traffic...")
    
    try:
        # Get basic traffic overview
        result = subprocess.run(['tcpdump', '-r', 'server.pcap', '-n'], 
                              capture_output=True, text=True)
        traffic = result.stdout
        
        # Question 6: OS Detection
        os_info = "Unknown"
        if "ubuntu" in traffic.lower():
            os_info = "Ubuntu"
        elif "debian" in traffic.lower():
            os_info = "Debian"
        elif "centos" in traffic.lower():
            os_info = "CentOS"
        elif "fedora" in traffic.lower():
            os_info = "Fedora"
        
        print(f"🐧 Detected OS: {os_info}")
        
        # Question 7: Downloaded tools
        tools = []
        if ".deb" in traffic:
            tools.append("apt/dpkg packages")
        if "wget" in traffic or "curl" in traffic:
            tools.append("wget/curl")
        if "nmap" in traffic:
            tools.append("nmap")
        
        # Question 8: Open ports analysis
        # Get SYN-ACK responses to identify open ports
        syn_ack_result = subprocess.run(['tcpdump', '-r', 'server.pcap', '-n', 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack != 0'], 
                                      capture_output=True, text=True)
        
        open_ports = set()
        for line in syn_ack_result.stdout.split('\n'):
            if '>' in line and 'Flags [S.]' in line:
                # Extract destination port from SYN-ACK
                port_match = re.search(r'\.(\d+):', line)
                if port_match:
                    open_ports.add(int(port_match.group(1)))
        
        print(f"🔌 Open ports detected: {sorted(open_ports)}")
        
        # Question 9: Browser detection
        browser = "Unknown"
        user_agent_result = subprocess.run(['tcpdump', '-r', 'server.pcap', '-A'], 
                                         capture_output=True, text=True)
        ua_traffic = user_agent_result.stdout
        
        if "Firefox" in ua_traffic:
            browser = "Firefox"
        elif "Chrome" in ua_traffic:
            browser = "Chrome"
        elif "curl" in ua_traffic:
            browser = "curl"
        elif "wget" in ua_traffic:
            browser = "wget"
        
        print(f"🌐 Browser/Tool: {browser}")
        
        return os_info, tools, sorted(open_ports), browser
        
    except Exception as e:
        print(f"❌ Error analyzing network: {e}")
        return "Unknown", [], [], "Unknown"

def analyze_word_document():
    """Question 13: Extract developer location from Word document"""
    print("\n📄 Analyzing Word Document...")
    
    try:
        # Extract all XML files from the Word document
        with zipfile.ZipFile('product_specs.docx', 'r') as zip_ref:
            zip_ref.extractall('temp_word')
        
        # Search through all extracted files for location information
        location_info = ""
        
        for root, dirs, files in os.walk('temp_word'):
            for file in files:
                if file.endswith('.xml'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            # Look for city/country patterns
                            city_country_patterns = [
                                r'([A-Z][a-z]+),\s*([A-Z][a-z]+)',
                                r'([A-Z][a-z]+)\s*,\s*([A-Z][a-z]+)',
                                r'from\s+([A-Z][a-z]+),?\s*([A-Z][a-z]+)',
                                r'located\s+in\s+([A-Z][a-z]+),?\s*([A-Z][a-z]+)',
                            ]
                            
                            for pattern in city_country_patterns:
                                matches = re.findall(pattern, content)
                                if matches:
                                    for match in matches:
                                        location_info = f"{match[0]}, {match[1]}"
                                        print(f"🌍 Found location: {location_info}")
                                        break
                            
                            if location_info:
                                break
                    except:
                        continue
                
                if location_info:
                    break
            if location_info:
                break
        
        # Clean up
        subprocess.run(['rm', '-rf', 'temp_word'], capture_output=True)
        
        return location_info
        
    except Exception as e:
        print(f"❌ Error analyzing Word document: {e}")
        return "Unknown"

def analyze_email_and_ports():
    """Questions 10, 11, 12: Email, ports, protocol analysis"""
    print("\n📧 Analyzing Email and Advanced Network Info...")
    
    try:
        # Get all HTTP traffic for email analysis
        http_result = subprocess.run(['tcpdump', '-r', 'server.pcap', '-A', 'port', '80', 'or', 'port', '443'], 
                                   capture_output=True, text=True)
        http_traffic = http_result.stdout
        
        # Question 10: Email address
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, http_traffic)
        unique_emails = list(set(emails))
        print(f"📧 Found emails: {unique_emails}")
        
        # Question 11: Port analysis - initially closed then opened
        # Get all traffic to analyze port states over time
        all_traffic_result = subprocess.run(['tcpdump', '-r', 'server.pcap', '-n'], 
                                          capture_output=True, text=True)
        all_traffic = all_traffic_result.stdout
        
        # Look for port scanning patterns and subsequent connections
        port_scan_ports = set()
        connected_ports = set()
        
        for line in all_traffic.split('\n'):
            # RST responses indicate closed ports during scanning
            if 'Flags [R.]' in line and '>' in line:
                port_match = re.search(r'\.(\d+):', line)
                if port_match:
                    port_scan_ports.add(int(port_match.group(1)))
            
            # Successful connections
            elif 'Flags [S.]' in line and '>' in line:
                port_match = re.search(r'\.(\d+):', line)
                if port_match:
                    connected_ports.add(int(port_match.group(1)))
        
        # Ports that were initially closed but later open
        new_ports = connected_ports - port_scan_ports
        print(f"🔌 Initially closed, later open: {sorted(new_ports)}")
        
        # Question 12: Protocol analysis
        # Look for acknowledgment requirements
        ack_info = "ACK" if "ACK" in all_traffic else "Unknown"
        
        return unique_emails, sorted(new_ports), ack_info
        
    except Exception as e:
        print(f"❌ Error analyzing email/ports: {e}")
        return [], [], "Unknown"

def main():
    print("🕵️  Comprehensive Forensics Analysis")
    print("=" * 60)
    
    # Change to the challenge directory
    os.chdir("/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/Back_to_the_New_House")
    
    # Questions 4 & 5: Task analysis
    created_tasks, deleted_tasks = analyze_task_scheduler()
    
    # Questions 6-9: Network analysis
    os_info, tools, open_ports, browser = analyze_network_traffic()
    
    # Questions 10-12: Advanced network analysis
    emails, new_ports, ack_info = analyze_email_and_ports()
    
    # Question 13: Word document analysis
    location = analyze_word_document()
    
    print("\n" + "="*60)
    print("🏁 FINAL ANSWERS:")
    print("="*60)
    print(f"4. Tasks no longer present: {', '.join(sorted(deleted_tasks))}")
    print(f"5. Task created: {', '.join(created_tasks)}")
    print(f"6. Operating system: {os_info}")
    print(f"7. Tool downloaded: {', '.join(tools) if tools else 'Unknown'}")
    print(f"8. Initially open ports: {', '.join(map(str, open_ports))}")
    print(f"9. Browser used: {browser}")
    print(f"10. Email address: {', '.join(emails) if emails else 'Unknown'}")
    print(f"11. Port brought up later: {', '.join(map(str, new_ports)) if new_ports else 'Unknown'}")
    print(f"12. What to send when message received: {ack_info}")
    print(f"13. Developer location: {location}")

if __name__ == "__main__":
    main()
