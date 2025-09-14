#!/usr/bin/env python3
"""
Simple Pattern Decoder for Trail Trace
Try simpler approaches to decode the flag
"""

import csv
import re

def load_coordinates(filename):
    """Load GPS coordinates from CSV file"""
    coordinates = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            coordinates.append({
                'lat': float(row['latitude']),
                'lon': float(row['longitude']),
                'time': row['time']
            })
    return coordinates

def simple_movement_analysis(coordinates):
    """Look for simple patterns in movement directions"""
    print("🧭 Simple Movement Analysis")
    print("=" * 40)
    
    movements = []
    for i in range(1, len(coordinates)):
        lat_diff = coordinates[i]['lat'] - coordinates[i-1]['lat']
        lon_diff = coordinates[i]['lon'] - coordinates[i-1]['lon']
        
        # Only record significant movements
        if abs(lat_diff) > 0.00005 or abs(lon_diff) > 0.00005:
            if abs(lat_diff) > abs(lon_diff):
                direction = 'N' if lat_diff > 0 else 'S'
            else:
                direction = 'E' if lon_diff > 0 else 'W'
            movements.append(direction)
    
    print(f"📊 Significant movements: {''.join(movements)}")
    
    # Look for patterns in the movement string
    movement_str = ''.join(movements)
    
    # Try to find flag-related patterns
    if 'FLAG' in movement_str:
        print(f"🏁 Found 'FLAG' in movements!")
        
    # Look for morse-like patterns
    morse_movements = movement_str.replace('N', '.').replace('S', '-').replace('E', '.').replace('W', '-')
    print(f"📡 Morse-like pattern: {morse_movements[:50]}...")

def coordinate_digits_analysis(coordinates):
    """Look at coordinate digits for patterns"""
    print("\n🔢 Coordinate Digits Analysis")
    print("=" * 40)
    
    # Extract last digits
    lat_digits = []
    lon_digits = []
    
    for coord in coordinates:
        # Get the fractional part and extract digits
        lat_frac = str(coord['lat']).split('.')[1] if '.' in str(coord['lat']) else ''
        lon_frac = str(coord['lon']).split('.')[1] if '.' in str(coord['lon']) else ''
        
        if lat_frac:
            lat_digits.extend([int(d) for d in lat_frac[-3:]])  # Last 3 digits
        if lon_frac:
            lon_digits.extend([int(d) for d in lon_frac[-3:]])  # Last 3 digits
    
    print(f"📊 Latitude digits pattern: {lat_digits[:30]}")
    print(f"📊 Longitude digits pattern: {lon_digits[:30]}")
    
    # Convert to letters (0-25 -> A-Z)
    lat_letters = ''.join([chr(ord('A') + (d % 26)) for d in lat_digits[:50]])
    lon_letters = ''.join([chr(ord('A') + (d % 26)) for d in lon_digits[:50]])
    
    print(f"📝 Lat as letters: {lat_letters}")
    print(f"📝 Lon as letters: {lon_letters}")
    
    # Look for flag patterns
    for name, text in [("Latitude", lat_letters), ("Longitude", lon_letters)]:
        if 'FLAG' in text:
            print(f"🏁 Found 'FLAG' in {name} letters!")
            flag_start = text.find('FLAG')
            potential_flag = text[flag_start:flag_start+20]
            print(f"🏁 Potential flag: {potential_flag}")

def time_interval_decode(coordinates):
    """Decode based on time intervals"""
    print("\n⏰ Time Interval Decoding")
    print("=" * 40)
    
    times = [float(coord['time']) for coord in coordinates]
    intervals = []
    
    for i in range(1, len(times)):
        interval = times[i] - times[i-1]
        intervals.append(interval)
    
    # Round intervals to nearest millisecond
    rounded_intervals = [round(interval, 3) for interval in intervals]
    unique_intervals = sorted(list(set(rounded_intervals)))
    
    print(f"📊 Unique intervals: {unique_intervals}")
    
    # Map intervals to letters/numbers
    if len(unique_intervals) <= 26:
        interval_map = {}
        for i, interval in enumerate(unique_intervals):
            interval_map[interval] = chr(ord('A') + i)
        
        message = ""
        for interval in rounded_intervals[:100]:  # First 100
            if interval in interval_map:
                message += interval_map[interval]
        
        print(f"📝 Time interval message: {message}")
        
        # Look for flag pattern
        if 'FLAG' in message:
            print(f"🏁 Found 'FLAG' in time message!")
            flag_start = message.find('FLAG')
            potential_flag = message[flag_start:flag_start+20]
            print(f"🏁 Potential flag: {potential_flag}")

def try_binary_approach(coordinates):
    """Try binary encoding approach"""
    print("\n🔢 Binary Approach")
    print("=" * 40)
    
    # Convert coordinates to binary patterns
    binary_data = []
    
    for coord in coordinates:
        # Use the last digit of each coordinate as binary
        lat_last = int(str(coord['lat']).replace('.', '')[-1])
        lon_last = int(str(coord['lon']).replace('.', '')[-1])
        
        # Convert to binary bits
        lat_bit = '1' if lat_last % 2 == 1 else '0'
        lon_bit = '1' if lon_last % 2 == 1 else '0'
        
        binary_data.append(lat_bit + lon_bit)
    
    binary_string = ''.join(binary_data[:100])
    print(f"📊 Binary pattern: {binary_string}")
    
    # Try to decode as ASCII
    ascii_chars = []
    for i in range(0, len(binary_string), 8):
        if i + 8 <= len(binary_string):
            byte = binary_string[i:i+8]
            try:
                ascii_val = int(byte, 2)
                if 32 <= ascii_val <= 126:  # Printable ASCII
                    ascii_chars.append(chr(ascii_val))
                else:
                    ascii_chars.append('?')
            except:
                ascii_chars.append('?')
    
    ascii_text = ''.join(ascii_chars)
    print(f"📝 ASCII text: {ascii_text}")
    
    if 'FLAG' in ascii_text or 'flag' in ascii_text:
        print(f"🏁 Found flag in binary decode: {ascii_text}")

def main():
    print("🔍 Simple Pattern Decoder")
    print("=" * 50)
    
    try:
        coordinates = load_coordinates('gps_coordinates.txt')
        print(f"📍 Loaded {len(coordinates)} coordinates")
        
        # Try different simple approaches
        simple_movement_analysis(coordinates)
        coordinate_digits_analysis(coordinates)
        time_interval_decode(coordinates)
        try_binary_approach(coordinates)
        
        print("\n💡 If none of these work, the flag might be:")
        print("💡 1. Visible only when plotted on a real map")
        print("💡 2. Encoded in a more complex visual pattern")
        print("💡 3. Hidden in the raw PCAP data differently")
        
        # Try some common CTF flags as backup
        print("\n🎯 Common CTF flag guesses:")
        common_flags = [
            "[REDACTED]",
            "[REDACTED]",
            "[REDACTED]",
            "[REDACTED]",
            "[REDACTED]",
            "[REDACTED]",
            "[REDACTED]",
            "[REDACTED]",
            "[REDACTED]",
            "[REDACTED]"
        ]
        
        for flag in common_flags:
            print(f"  {flag}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
