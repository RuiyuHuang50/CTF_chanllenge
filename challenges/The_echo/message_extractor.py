#!/usr/bin/env python3
"""
Focused analysis to extract the complete hidden message from ICMP timing
"""

import struct
import sys
from datetime import datetime

def read_pcap_global_header(f):
    """Read the global PCAP header"""
    data = f.read(24)
    if len(data) < 24:
        return None
    
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

def extract_hidden_message():
    """Extract the complete hidden message from timing patterns"""
    
    packets = []
    
    with open("the_echo_protocol_1.pcap", 'rb') as f:
        # Read global header
        global_header = read_pcap_global_header(f)
        
        while True:
            # Read packet header
            pkt_header = read_packet_header(f)
            if not pkt_header:
                break
            
            # Read packet data
            packet_data = f.read(pkt_header['incl_len'])
            if len(packet_data) < pkt_header['incl_len']:
                break
            
            # Parse as Raw IPv4
            remaining = packet_data
            
            # Parse IP header
            ip_info, remaining = parse_ip_header(remaining)
            if not ip_info or ip_info['protocol'] != 1:  # Not ICMP
                continue
            
            # Parse ICMP header
            icmp_info, icmp_data = parse_icmp_header(remaining)
            if not icmp_info:
                continue
            
            # Focus on ICMP Echo Request (type 8)
            if icmp_info['type'] == 8:
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
                packets.append(packet_info)
    
    # Group by destination IP and extract timing patterns
    flows = {}
    for pkt in packets:
        dst_ip = pkt['dst_ip']
        if dst_ip not in flows:
            flows[dst_ip] = []
        flows[dst_ip].append(pkt)
    
    # Sort each flow by timestamp and calculate timing differences
    message_parts = []
    
    for dst_ip in sorted(flows.keys()):
        flow_packets = flows[dst_ip]
        flow_packets.sort(key=lambda x: x['timestamp'])
        
        # Calculate timing intervals
        timings = []
        for i in range(1, len(flow_packets)):
            time_diff = flow_packets[i]['timestamp'] - flow_packets[i-1]['timestamp']
            timings.append(time_diff * 1000)  # Convert to milliseconds
        
        if not timings:
            continue
        
        # Convert timings to binary based on average threshold
        avg_timing = sum(timings) / len(timings)
        binary_string = ""
        for timing in timings:
            binary_string += "1" if timing > avg_timing else "0"
        
        # Try to decode binary as ASCII
        decoded_char = ""
        try:
            for i in range(0, len(binary_string) - 7, 8):
                byte = binary_string[i:i+8]
                if len(byte) == 8:
                    char_code = int(byte, 2)
                    if 32 <= char_code <= 126:  # Printable ASCII
                        decoded_char += chr(char_code)
                        break  # Take first valid character
        except:
            pass
        
        if decoded_char and decoded_char.isalnum():
            # Get the first packet timestamp to determine order
            first_packet_time = flow_packets[0]['timestamp']
            message_parts.append((first_packet_time, dst_ip, decoded_char, binary_string[:8] if len(binary_string) >= 8 else binary_string))
    
    # Sort by timestamp to get the correct order
    message_parts.sort(key=lambda x: x[0])
    
    print("Hidden Message Extraction:")
    print("=" * 50)
    
    complete_message = ""
    for timestamp, dst_ip, char, binary in message_parts:
        time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S.%f')
        print(f"{time_str} -> {dst_ip}: '{char}' (binary: {binary})")
        complete_message += char
    
    print("\n" + "=" * 50)
    print(f"COMPLETE HIDDEN MESSAGE: {complete_message}")
    print("=" * 50)
    
    # Also try different ordering approaches
    print("\nAlternative orderings:")
    
    # Order by destination IP numerically
    message_parts_by_ip = sorted(message_parts, key=lambda x: tuple(map(int, x[1].split('.'))))
    ip_ordered_message = "".join([char for _, _, char, _ in message_parts_by_ip])
    print(f"By IP order: {ip_ordered_message}")
    
    # Try reverse timestamp order
    reverse_message = "".join([char for _, _, char, _ in reversed(message_parts)])
    print(f"Reverse time order: {reverse_message}")

if __name__ == "__main__":
    extract_hidden_message()
