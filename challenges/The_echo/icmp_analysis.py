#!/usr/bin/env python3
"""
ICMP Echo Analysis for The_echo Challenge
Focus on timing between consecutive packets and data patterns
"""

import struct
import sys
from datetime import datetime

def read_pcap_global_header(f):
    """Read the global PCAP header"""
    data = f.read(24)
    if len(data) < 24:
        return None
    
    # PCAP global header format
    magic, version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack('IHHIIII', data)
    return {
        'magic': magic,
        'version_major': version_major,
        'version_minor': version_minor,
        'network': network
    }

def read_packet_header(f):
    """Read a packet header"""
    data = f.read(16)
    if len(data) < 16:
        return None
    
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', data)
    timestamp = ts_sec + ts_usec / 1000000.0
    return {
        'timestamp': timestamp,
        'incl_len': incl_len,
        'orig_len': orig_len
    }

def parse_ethernet_header(data):
    """Parse Ethernet header"""
    if len(data) < 14:
        return None, data
    
    eth_header = struct.unpack('!6s6sH', data[:14])
    eth_type = eth_header[2]
    return eth_type, data[14:]

def parse_ip_header(data):
    """Parse IP header"""
    if len(data) < 20:
        return None, data
    
    ip_header = struct.unpack('!BBHHHBBH4s4s', data[:20])
    version_ihl = ip_header[0]
    ihl = version_ihl & 0xF
    header_length = ihl * 4
    protocol = ip_header[6]
    src_ip = '.'.join(map(str, ip_header[8]))
    dst_ip = '.'.join(map(str, ip_header[9]))
    
    return {
        'protocol': protocol,
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'header_length': header_length
    }, data[header_length:]

def parse_icmp_header(data):
    """Parse ICMP header"""
    if len(data) < 8:
        return None, data
    
    icmp_header = struct.unpack('!BBHHH', data[:8])
    icmp_type = icmp_header[0]
    icmp_code = icmp_header[1]
    checksum = icmp_header[2]
    identifier = icmp_header[3]
    sequence = icmp_header[4]
    
    return {
        'type': icmp_type,
        'code': icmp_code,
        'identifier': identifier,
        'sequence': sequence
    }, data[8:]

def analyze_pcap(filename):
    """Analyze the PCAP file for ICMP Echo packets"""
    packets = []
    
    try:
        with open(filename, 'rb') as f:
            # Read global header
            global_header = read_pcap_global_header(f)
            if not global_header:
                print("Failed to read PCAP global header")
                return
            
            print(f"PCAP Version: {global_header['version_major']}.{global_header['version_minor']}")
            print(f"Network type: {global_header['network']}")
            print("-" * 50)
            
            packet_count = 0
            icmp_packets = []
            
            while True:
                # Read packet header
                pkt_header = read_packet_header(f)
                if not pkt_header:
                    break
                
                # Read packet data
                packet_data = f.read(pkt_header['incl_len'])
                if len(packet_data) < pkt_header['incl_len']:
                    break
                
                packet_count += 1
                
                # Check if this is Raw IPv4 (no Ethernet header)
                if global_header['network'] == 228:  # Raw IPv4
                    remaining = packet_data
                else:
                    # Parse Ethernet header
                    eth_type, remaining = parse_ethernet_header(packet_data)
                    if eth_type != 0x0800:  # Not IPv4
                        continue
                
                # Parse IP header
                ip_info, remaining = parse_ip_header(remaining)
                if not ip_info or ip_info['protocol'] != 1:  # Not ICMP
                    continue
                
                # Parse ICMP header
                icmp_info, icmp_data = parse_icmp_header(remaining)
                if not icmp_info:
                    continue
                
                # Focus on ICMP Echo Request (type 8) and Echo Reply (type 0)
                if icmp_info['type'] in [0, 8]:
                    packet_info = {
                        'timestamp': pkt_header['timestamp'],
                        'src_ip': ip_info['src_ip'],
                        'dst_ip': ip_info['dst_ip'],
                        'icmp_type': icmp_info['type'],
                        'icmp_id': icmp_info['identifier'],
                        'icmp_seq': icmp_info['sequence'],
                        'data': icmp_data,
                        'data_length': len(icmp_data)
                    }
                    icmp_packets.append(packet_info)
            
            print(f"Total packets: {packet_count}")
            print(f"ICMP Echo packets: {len(icmp_packets)}")
            print("-" * 50)
            
            # Analyze ICMP packets
            analyze_icmp_patterns(icmp_packets)
            
    except Exception as e:
        print(f"Error analyzing PCAP: {e}")

def analyze_icmp_patterns(packets):
    """Analyze patterns in ICMP packets"""
    if not packets:
        print("No ICMP packets found")
        return
    
    print("ICMP Packet Analysis:")
    print("=" * 60)
    
    # Group by source/destination pairs
    flows = {}
    for pkt in packets:
        flow_key = f"{pkt['src_ip']} -> {pkt['dst_ip']}"
        if flow_key not in flows:
            flows[flow_key] = []
        flows[flow_key].append(pkt)
    
    print(f"Found {len(flows)} different flows:")
    for flow, flow_packets in flows.items():
        print(f"\nFlow: {flow}")
        print(f"  Packets: {len(flow_packets)}")
        
        # Sort by timestamp
        flow_packets.sort(key=lambda x: x['timestamp'])
        
        # Analyze timing between consecutive packets
        timings = []
        for i in range(1, len(flow_packets)):
            time_diff = flow_packets[i]['timestamp'] - flow_packets[i-1]['timestamp']
            timings.append(time_diff)
        
        if timings:
            print(f"  Timing intervals (seconds):")
            for i, timing in enumerate(timings[:10]):  # Show first 10
                print(f"    Packet {i+1}->{i+2}: {timing:.6f}s")
            
            # Look for patterns in timing
            timing_analysis(timings, flow)
        
        # Show packet details
        print(f"  First few packets:")
        for i, pkt in enumerate(flow_packets[:5]):
            pkt_type = "Echo Request" if pkt['icmp_type'] == 8 else "Echo Reply"
            print(f"    {i+1}: {datetime.fromtimestamp(pkt['timestamp']).strftime('%H:%M:%S.%f')} - {pkt_type} ID:{pkt['icmp_id']} Seq:{pkt['icmp_seq']} DataLen:{pkt['data_length']}")

def timing_analysis(timings, flow_name):
    """Analyze timing patterns for potential hidden data"""
    print(f"  Timing Analysis for {flow_name}:")
    
    # Convert timings to milliseconds for easier analysis
    ms_timings = [t * 1000 for t in timings]
    
    # Look for patterns - could be ASCII values, binary encoding, etc.
    print(f"    Timings in ms: {[f'{t:.2f}' for t in ms_timings[:20]]}")
    
    # Try to decode as ASCII (assuming timing represents character values)
    try:
        # Round timings and see if they form readable text
        rounded_timings = [round(t) for t in ms_timings]
        ascii_attempt = ""
        for timing in rounded_timings:
            if 32 <= timing <= 126:  # Printable ASCII range
                ascii_attempt += chr(timing)
            else:
                ascii_attempt += "?"
        
        if any(c.isalpha() for c in ascii_attempt):
            print(f"    Possible ASCII interpretation: '{ascii_attempt[:50]}'")
    except:
        pass
    
    # Look for timing intervals that might represent binary data
    # Convert to binary based on threshold
    if ms_timings:
        avg_timing = sum(ms_timings) / len(ms_timings)
        binary_string = ""
        for timing in ms_timings:
            binary_string += "1" if timing > avg_timing else "0"
        
        print(f"    Binary pattern (>avg=1): {binary_string[:50]}")
        
        # Try to decode binary as ASCII
        try:
            decoded_text = ""
            for i in range(0, len(binary_string) - 7, 8):
                byte = binary_string[i:i+8]
                if len(byte) == 8:
                    char_code = int(byte, 2)
                    if 32 <= char_code <= 126:
                        decoded_text += chr(char_code)
                    else:
                        decoded_text += "?"
            
            if any(c.isalpha() for c in decoded_text):
                print(f"    Binary->ASCII: '{decoded_text[:30]}'")
        except:
            pass

if __name__ == "__main__":
    analyze_pcap("the_echo_protocol_1.pcap")
