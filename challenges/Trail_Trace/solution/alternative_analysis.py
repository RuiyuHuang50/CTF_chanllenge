#!/usr/bin/env python3
"""
Alternative Analysis for Trail Trace Challenge
Look for patterns in coordinate values, time stamps, or other hidden data
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

def analyze_coordinate_deltas(coordinates):
    """Look for patterns in coordinate changes"""
    print("🔍 Analyzing coordinate deltas for hidden patterns...")
    
    deltas = []
    for i in range(1, len(coordinates)):
        lat_delta = coordinates[i]['lat'] - coordinates[i-1]['lat']
        lon_delta = coordinates[i]['lon'] - coordinates[i-1]['lon']
        deltas.append((lat_delta, lon_delta))
    
    # Look for significant moves
    significant_deltas = []
    for i, (lat_d, lon_d) in enumerate(deltas):
        if abs(lat_d) > 0.0001 or abs(lon_d) > 0.0001:
            significant_deltas.append((i+1, lat_d, lon_d))
    
    print(f"📊 Found {len(significant_deltas)} significant movements")
    
    # Show significant movements
    for i, (idx, lat_d, lon_d) in enumerate(significant_deltas[:20]):
        print(f"  Move {i+1}: Point {idx} - Lat: {lat_d:+.6f}, Lon: {lon_d:+.6f}")
    
    return significant_deltas

def analyze_time_patterns(coordinates):
    """Look for patterns in timestamps"""
    print("\n🕐 Analyzing timestamp patterns...")
    
    times = [float(coord['time']) for coord in coordinates]
    time_deltas = []
    
    for i in range(1, len(times)):
        delta = times[i] - times[i-1]
        time_deltas.append(delta)
    
    # Look for unique time intervals
    unique_deltas = list(set(time_deltas))
    unique_deltas.sort()
    
    print(f"📊 Unique time intervals: {len(unique_deltas)}")
    for i, delta in enumerate(unique_deltas[:10]):
        print(f"  Interval {i+1}: {delta:.3f} seconds")
    
    # Check if time intervals encode something
    if len(unique_deltas) <= 26:  # Could be letters
        print("💡 Time intervals might encode letters (A-Z)!")
        delta_to_letter = {}
        for i, delta in enumerate(unique_deltas):
            delta_to_letter[delta] = chr(ord('A') + i)
        
        # Decode message
        message = ""
        for delta in time_deltas[:50]:  # First 50 intervals
            if delta in delta_to_letter:
                message += delta_to_letter[delta]
            else:
                message += "?"
        
        print(f"🔤 Potential message from time intervals: {message}")

def analyze_coordinate_precision(coordinates):
    """Look for patterns in coordinate precision/last digits"""
    print("\n🎯 Analyzing coordinate precision patterns...")
    
    # Extract last digits of coordinates
    lat_last_digits = []
    lon_last_digits = []
    
    for coord in coordinates:
        # Get last digit of latitude (after decimal)
        lat_str = f"{coord['lat']:.6f}"
        lon_str = f"{coord['lon']:.6f}"
        
        # Extract digits after decimal
        lat_decimal = lat_str.split('.')[1]
        lon_decimal = lon_str.split('.')[1]
        
        lat_last_digits.append(lat_decimal[-1])
        lon_last_digits.append(lon_decimal[-1])
    
    print(f"📊 Latitude last digits: {''.join(lat_last_digits[:50])}")
    print(f"📊 Longitude last digits: {''.join(lon_last_digits[:50])}")
    
    # Check if digits spell something
    lat_chars = ''.join(lat_last_digits)
    lon_chars = ''.join(lon_last_digits)
    
    # Look for flag pattern in digit sequences
    for name, chars in [("Latitude", lat_chars), ("Longitude", lon_chars)]:
        if 'flag' in chars.lower():
            print(f"🏁 Found 'flag' in {name} digits!")
        if any(pattern in chars for pattern in ['123', '456', '789']):
            print(f"🔢 Found sequential pattern in {name} digits")

def search_coordinate_ascii(coordinates):
    """Convert coordinate values to ASCII characters"""
    print("\n🔤 Converting coordinates to ASCII characters...")
    
    # Try different approaches to extract ASCII values
    for coord in coordinates[:20]:
        lat_int = int(abs(coord['lat'] * 100000) % 128)
        lon_int = int(abs(coord['lon'] * 100000) % 128)
        
        if 32 <= lat_int <= 126:  # Printable ASCII range
            lat_char = chr(lat_int)
        else:
            lat_char = '?'
            
        if 32 <= lon_int <= 126:  # Printable ASCII range
            lon_char = chr(lon_int)
        else:
            lon_char = '?'
        
        print(f"  Lat: {coord['lat']:.6f} -> {lat_int} -> '{lat_char}' | Lon: {coord['lon']:.6f} -> {lon_int} -> '{lon_char}'")

def look_for_hex_patterns(coordinates):
    """Look for hexadecimal patterns in coordinates"""
    print("\n🔢 Looking for hexadecimal patterns...")
    
    # Convert coordinate parts to hex
    hex_values = []
    for coord in coordinates:
        # Take fractional part and convert to hex-like values
        lat_frac = abs(coord['lat']) - int(abs(coord['lat']))
        lon_frac = abs(coord['lon']) - int(abs(coord['lon']))
        
        # Scale and convert to integers
        lat_hex = int(lat_frac * 1000000) % 16
        lon_hex = int(lon_frac * 1000000) % 16
        
        hex_values.append(f"{lat_hex:X}{lon_hex:X}")
    
    hex_string = ''.join(hex_values[:50])
    print(f"📊 Hex pattern from coordinates: {hex_string}")
    
    # Look for patterns
    if 'FLAG' in hex_string:
        print("🏁 Found 'FLAG' in hex pattern!")

def main():
    print("🔍 Alternative Trail Trace Analysis")
    print("=" * 50)
    
    try:
        coordinates = load_coordinates('gps_coordinates.txt')
        print(f"📍 Loaded {len(coordinates)} GPS coordinates")
        
        # Try different analysis methods
        analyze_coordinate_deltas(coordinates)
        analyze_time_patterns(coordinates)
        analyze_coordinate_precision(coordinates)
        search_coordinate_ascii(coordinates)
        look_for_hex_patterns(coordinates)
        
        # Show some raw data for manual inspection
        print("\n📊 First 10 coordinates for manual analysis:")
        for i, coord in enumerate(coordinates[:10]):
            print(f"  {i+1:2}: {coord['lat']:.6f}, {coord['lon']:.6f}, {coord['time']}")
        
        print("\n💡 Try looking at the GPS trail on a mapping service!")
        print("💡 Copy coordinates to Google Earth or similar tool")
        print("💡 The flag might be visible when plotted on a real map")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
