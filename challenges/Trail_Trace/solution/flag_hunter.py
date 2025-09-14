#!/usr/bin/env python3
"""
Flag Hunter for Trail Trace Challenge
Look for the actual flag in the data using different decoding methods
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

def search_flag_in_timestamp_message(coordinates):
    """Search for flag pattern in timestamp-decoded message"""
    print("🏁 Searching for flag in timestamp message...")
    
    times = [float(coord['time']) for coord in coordinates]
    time_deltas = []
    
    for i in range(1, len(times)):
        delta = times[i] - times[i-1]
        time_deltas.append(delta)
    
    # Get unique intervals and sort them
    unique_deltas = sorted(list(set(time_deltas)))
    
    # Try different letter mappings
    mappings = [
        {0.0: 'A', 0.001: 'B', 0.001: 'C', 0.002: 'D', 0.003: 'E'},  # Default
        {0.0: ' ', 0.001: 'F', 0.001: 'L', 0.002: 'A', 0.003: 'G'},  # FLAG focused
        {0.0: 'F', 0.001: 'L', 0.001: 'A', 0.002: 'G', 0.003: '{'},  # Direct FLAG
    ]
    
    for i, mapping in enumerate(mappings):
        print(f"\n🔤 Mapping {i+1}: {mapping}")
        
        # Decode message with this mapping
        message = ""
        for delta in time_deltas:
            # Find closest matching delta
            closest_delta = min(mapping.keys(), key=lambda x: abs(x - delta))
            message += mapping[closest_delta]
        
        print(f"📝 Message snippet: {message[:100]}...")
        
        # Search for flag patterns
        flag_patterns = ['FLAG', 'flag', 'UKCT', 'CTF', '{', '}']
        for pattern in flag_patterns:
            if pattern in message:
                print(f"🏁 Found '{pattern}' in message!")
                # Extract context around the pattern
                for match in re.finditer(pattern, message):
                    start = max(0, match.start() - 20)
                    end = min(len(message), match.end() + 20)
                    context = message[start:end]
                    print(f"   Context: ...{context}...")

def decode_coordinates_as_text(coordinates):
    """Try to decode coordinates as text in various ways"""
    print("\n🔤 Decoding coordinates as text...")
    
    # Method 1: Use coordinate differences as ASCII
    print("📊 Method 1: Coordinate differences as ASCII")
    for i in range(1, min(50, len(coordinates))):
        lat_diff = coordinates[i]['lat'] - coordinates[i-1]['lat']
        lon_diff = coordinates[i]['lon'] - coordinates[i-1]['lon']
        
        # Scale and convert to ASCII range
        lat_ascii = int(abs(lat_diff * 1000000)) % 128
        lon_ascii = int(abs(lon_diff * 1000000)) % 128
        
        if 32 <= lat_ascii <= 126:
            lat_char = chr(lat_ascii)
        else:
            lat_char = '?'
            
        if 32 <= lon_ascii <= 126:
            lon_char = chr(lon_ascii)
        else:
            lon_char = '?'
        
        if i <= 20:
            print(f"  {i:2}: Lat diff {lat_diff:.6f} -> {lat_ascii} -> '{lat_char}' | Lon diff {lon_diff:.6f} -> {lon_ascii} -> '{lon_char}'")
    
    # Method 2: Use fractional parts as character codes
    print("\n📊 Method 2: Fractional parts as character indices")
    text_from_coords = ""
    for coord in coordinates[:100]:
        lat_frac = abs(coord['lat']) - int(abs(coord['lat']))
        # Scale fractional part to 0-25 range for A-Z
        char_index = int(lat_frac * 1000000) % 26
        text_from_coords += chr(ord('A') + char_index)
    
    print(f"📝 Text from lat fractions: {text_from_coords[:50]}...")
    
    # Look for flag patterns
    if 'FLAG' in text_from_coords:
        print(f"🏁 Found 'FLAG' in coordinate text!")
        flag_start = text_from_coords.find('FLAG')
        potential_flag = text_from_coords[flag_start:flag_start+50]
        print(f"🏁 Potential flag: {potential_flag}")

def analyze_coordinate_clusters(coordinates):
    """Look for clusters of coordinates that might form letters"""
    print("\n🎯 Analyzing coordinate clusters...")
    
    lats = [c['lat'] for c in coordinates]
    lons = [c['lon'] for c in coordinates]
    
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Divide coordinate space into a grid to look for letter-like patterns
    grid_size = 20
    lat_step = (max_lat - min_lat) / grid_size
    lon_step = (max_lon - min_lon) / grid_size
    
    # Count points in each grid cell
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    for coord in coordinates:
        lat_idx = int((coord['lat'] - min_lat) / lat_step)
        lon_idx = int((coord['lon'] - min_lon) / lon_step)
        
        # Ensure we don't go out of bounds
        lat_idx = min(lat_idx, grid_size - 1)
        lon_idx = min(lon_idx, grid_size - 1)
        
        grid[lat_idx][lon_idx] += 1
    
    # Convert to binary (has points or not)
    print("📍 Grid pattern (# = has GPS points):")
    for row in reversed(grid):  # Reverse to match map orientation
        line = ""
        for cell in row:
            line += '#' if cell > 0 else ' '
        print(line)

def brute_force_flag_search(coordinates):
    """Brute force search for flag patterns in all possible encodings"""
    print("\n🔍 Brute force flag search...")
    
    # Collect all numeric data
    all_numbers = []
    
    for coord in coordinates:
        # Add various numeric representations
        all_numbers.extend([
            int(coord['lat'] * 1000000) % 256,
            int(coord['lon'] * 1000000) % 256,
            int(float(coord['time']) * 1000) % 256,
        ])
    
    # Convert to characters and search for flag
    text_data = ""
    for num in all_numbers:
        if 32 <= num <= 126:  # Printable ASCII
            text_data += chr(num)
        else:
            text_data += '?'
    
    print(f"📝 Generated text data: {text_data[:100]}...")
    
    # Search for flag patterns
    flag_patterns = ['[REDACTED]' in brute force search!")
            flag_start = text_data.find(pattern)
            potential_flag = text_data[flag_start:flag_start+50]
            print(f"🏁 Potential flag: {potential_flag}")

def main():
    print("🕵️  Flag Hunter - Trail Trace Challenge")
    print("=" * 60)
    
    try:
        coordinates = load_coordinates('gps_coordinates.txt')
        print(f"📍 Loaded {len(coordinates)} GPS coordinates")
        
        # Try all possible flag extraction methods
        search_flag_in_timestamp_message(coordinates)
        decode_coordinates_as_text(coordinates)
        analyze_coordinate_clusters(coordinates)
        brute_force_flag_search(coordinates)
        
        print("\n🎯 FINAL ATTEMPT - Manual pattern recognition:")
        print("💡 The trail might spell out text when viewed on an actual map")
        print("💡 Try copying coordinates to Google Earth or similar mapping tool")
        print("💡 Look for letter-like shapes formed by the GPS path")
        
        # Create a KML file for Google Earth
        with open('trail.kml', 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            f.write('<Document>\n')
            f.write('<Placemark>\n')
            f.write('<name>Criminal Trail</name>\n')
            f.write('<LineString>\n')
            f.write('<coordinates>\n')
            for coord in coordinates:
                f.write(f"{coord['lon']},{coord['lat']},0\n")
            f.write('</coordinates>\n')
            f.write('</LineString>\n')
            f.write('</Placemark>\n')
            f.write('</Document>\n')
            f.write('</kml>\n')
        
        print("📁 Created trail.kml for Google Earth visualization")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
