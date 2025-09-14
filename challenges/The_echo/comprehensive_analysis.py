#!/usr/bin/env python3
"""
Comprehensive ICMP timing analysis for hidden message extraction
Focus on different methods of interpreting timing data
"""

import struct
import sys
from datetime import datetime

def read_pcap_global_header(f):
    data = f.read(24)
    if len(data) < 24:
        return None
    magic, version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack('IHHIIII', data)
    return {'magic': magic, 'version_major': version_major, 'version_minor': version_minor, 'network': network}

def read_packet_header(f):
    data = f.read(16)
    if len(data) < 16:
        return None
    ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', data)
    timestamp = ts_sec + ts_usec / 1000000.0
    return {'timestamp': timestamp, 'incl_len': incl_len, 'orig_len': orig_len}

def parse_ip_header(data):
    if len(data) < 20:
        return None, data
    ip_header = struct.unpack('!BBHHHBBH4s4s', data[:20])
    version_ihl = ip_header[0]
    ihl = version_ihl & 0xF
    header_length = ihl * 4
    protocol = ip_header[6]
    src_ip = '.'.join(map(str, ip_header[8]))
    dst_ip = '.'.join(map(str, ip_header[9]))
    return {'protocol': protocol, 'src_ip': src_ip, 'dst_ip': dst_ip, 'header_length': header_length}, data[header_length:]

def parse_icmp_header(data):
    if len(data) < 8:
        return None, data
    icmp_header = struct.unpack('!BBHHH', data[:8])
    icmp_type = icmp_header[0]
    icmp_code = icmp_header[1]
    checksum = icmp_header[2]
    identifier = icmp_header[3]
    sequence = icmp_header[4]
    return {'type': icmp_type, 'code': icmp_code, 'identifier': identifier, 'sequence': sequence}, data[8:]

def analyze_comprehensive():
    packets = []
    
    with open("the_echo_protocol_1.pcap", 'rb') as f:
        global_header = read_pcap_global_header(f)
        
        while True:
            pkt_header = read_packet_header(f)
            if not pkt_header:
                break
            
            packet_data = f.read(pkt_header['incl_len'])
            if len(packet_data) < pkt_header['incl_len']:
                break
            
            remaining = packet_data
            ip_info, remaining = parse_ip_header(remaining)
            if not ip_info or ip_info['protocol'] != 1:
                continue
            
            icmp_info, icmp_data = parse_icmp_header(remaining)
            if not icmp_info or icmp_info['type'] != 8:  # Only Echo Requests
                continue
            
            packet_info = {
                'timestamp': pkt_header['timestamp'],
                'src_ip': ip_info['src_ip'],
                'dst_ip': ip_info['dst_ip'],
                'icmp_id': icmp_info['identifier'],
                'icmp_seq': icmp_info['sequence'],
                'data_length': len(icmp_data)
            }
            packets.append(packet_info)
    
    # Group by destination IP
    flows = {}
    for pkt in packets:
        dst_ip = pkt['dst_ip']
        if dst_ip not in flows:
            flows[dst_ip] = []
        flows[dst_ip].append(pkt)
    
    # Analyze each flow
    results = []
    
    for dst_ip in flows:
        flow_packets = flows[dst_ip]
        flow_packets.sort(key=lambda x: x['timestamp'])
        
        if len(flow_packets) < 2:
            continue
        
        # Calculate timing intervals in milliseconds
        timings = []
        for i in range(1, len(flow_packets)):
            time_diff = (flow_packets[i]['timestamp'] - flow_packets[i-1]['timestamp']) * 1000
            timings.append(time_diff)
        
        if not timings:
            continue
        
        first_packet_time = flow_packets[0]['timestamp']
        
        # Method 1: Binary encoding with average threshold
        avg_timing = sum(timings) / len(timings)
        binary_string = ""
        for timing in timings:
            binary_string += "1" if timing > avg_timing else "0"
        
        # Try to decode as ASCII (8-bit chunks)
        ascii_chars = []
        for i in range(0, len(binary_string) - 7, 8):
            byte = binary_string[i:i+8]
            if len(byte) == 8:
                try:
                    char_code = int(byte, 2)
                    if 32 <= char_code <= 126:
                        ascii_chars.append(chr(char_code))
                except:
                    pass
        
        # Method 2: Direct timing as ASCII values (rounded)
        direct_ascii = []
        for timing in timings:
            rounded_timing = round(timing)
            if 32 <= rounded_timing <= 126:
                direct_ascii.append(chr(rounded_timing))
        
        # Method 3: Timing intervals as character positions
        # Try different scaling factors
        for scale in [1, 10, 100]:
            scaled_chars = []
            for timing in timings:
                scaled_val = round(timing / scale)
                if 32 <= scaled_val <= 126:
                    scaled_chars.append(chr(scaled_val))
        
        # Store results
        result = {
            'dst_ip': dst_ip,
            'first_timestamp': first_packet_time,
            'packet_count': len(flow_packets),
            'timings_ms': timings[:10],  # First 10 for display
            'binary_string': binary_string,
            'ascii_from_binary': ''.join(ascii_chars),
            'direct_ascii': ''.join(direct_ascii),
            'avg_timing': avg_timing
        }
        results.append(result)
    
    # Sort by first packet timestamp
    results.sort(key=lambda x: x['first_timestamp'])
    
    print("Comprehensive ICMP Timing Analysis")
    print("=" * 60)
    
    message_candidates = []
    
    for result in results:
        time_str = datetime.fromtimestamp(result['first_timestamp']).strftime('%H:%M:%S.%f')
        print(f"\nFlow to {result['dst_ip']} (started {time_str}):")
        print(f"  Packets: {result['packet_count']}")
        print(f"  Timings (ms): {[f'{t:.1f}' for t in result['timings_ms']]}")
        print(f"  Binary: {result['binary_string'][:16]}...")
        print(f"  ASCII from binary: '{result['ascii_from_binary']}'")
        print(f"  Direct ASCII: '{result['direct_ascii'][:10]}'")
        
        # Collect the best candidate character
        best_char = ""
        if result['ascii_from_binary'] and result['ascii_from_binary'][0].isalnum():
            best_char = result['ascii_from_binary'][0]
        elif result['direct_ascii'] and len(result['direct_ascii']) > 0:
            # Look for alphanumeric characters in direct ASCII
            for char in result['direct_ascii']:
                if char.isalnum():
                    best_char = char
                    break
        
        if best_char:
            message_candidates.append((result['first_timestamp'], best_char, result['dst_ip']))
    
    # Generate message from best candidates
    message_candidates.sort(key=lambda x: x[0])
    
    print("\n" + "=" * 60)
    print("MESSAGE EXTRACTION:")
    extracted_message = ""
    for timestamp, char, dst_ip in message_candidates:
        time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S.%f')
        print(f"{time_str} -> {dst_ip}: '{char}'")
        extracted_message += char
    
    print(f"\nEXTRACTED MESSAGE: {extracted_message}")
    
    # Look for common flag patterns
    flag_patterns = ['flag', 'ctf', 'FLAG', 'CTF']
    for pattern in flag_patterns:
        if pattern.lower() in extracted_message.lower():
            print(f"🎯 FOUND PATTERN '{pattern}' in message!")
    
    # Try case variations
    print(f"Uppercase: {extracted_message.upper()}")
    print(f"Lowercase: {extracted_message.lower()}")
    
    return extracted_message

if __name__ == "__main__":
    analyze_comprehensive()
