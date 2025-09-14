#!/usr/bin/env python3
"""
Final Trail Trace Solver
Focus on the most promising patterns found
"""

import csv

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

def decode_timestamp_message(coordinates):
    """Decode message from timestamp intervals"""
    print("🕐 Decoding message from timestamp intervals...")
    
    times = [float(coord['time']) for coord in coordinates]
    time_deltas = []
    
    for i in range(1, len(times)):
        delta = times[i] - times[i-1]
        time_deltas.append(delta)
    
    # Get unique intervals and sort them
    unique_deltas = sorted(list(set(time_deltas)))
    print(f"📊 Unique time intervals: {unique_deltas}")
    
    # Map intervals to letters
    delta_to_letter = {}
    for i, delta in enumerate(unique_deltas):
        delta_to_letter[delta] = chr(ord('A') + i)
    
    print("🔤 Interval to letter mapping:")
    for delta, letter in delta_to_letter.items():
        count = time_deltas.count(delta)
        print(f"  {delta:.3f}s -> '{letter}' (appears {count} times)")
    
    # Decode full message
    message = ""
    for delta in time_deltas:
        if delta in delta_to_letter:
            message += delta_to_letter[delta]
    
    print(f"\n📝 Full decoded message ({len(message)} chars): {message}")
    
    # Look for flag pattern in message
    if 'FLAG' in message:
        print(f"🏁 Found 'FLAG' in message!")
        flag_start = message.find('FLAG')
        potential_flag = message[flag_start:flag_start+50]
        print(f"🏁 Potential flag: {potential_flag}")
    
    # Try reverse decoding
    reverse_message = message[::-1]
    print(f"📝 Reversed message: {reverse_message[:100]}...")
    if 'FLAG' in reverse_message:
        print(f"🏁 Found 'FLAG' in reversed message!")
        flag_start = reverse_message.find('FLAG')
        potential_flag = reverse_message[flag_start:flag_start+50]
        print(f"🏁 Potential flag: {potential_flag}")

def create_compact_trail_map(coordinates):
    """Create a compact, readable trail map"""
    print("\n🗺️  Creating compact trail visualization...")
    
    if not coordinates:
        return
    
    lats = [c['lat'] for c in coordinates]
    lons = [c['lon'] for c in coordinates]
    
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Use moderate resolution for better readability
    width, height = 60, 20
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Map coordinates to grid with path ordering
    for i, coord in enumerate(coordinates):
        if max_lat != min_lat and max_lon != min_lon:
            x = int(((coord['lon'] - min_lon) / (max_lon - min_lon)) * (width - 1))
            y = int(((coord['lat'] - min_lat) / (max_lat - min_lat)) * (height - 1))
            y = height - 1 - y  # Flip Y axis
            
            if 0 <= x < width and 0 <= y < height:
                # Use different characters to show path direction
                if i < len(coordinates) // 3:
                    grid[y][x] = '.'  # Start of path
                elif i < 2 * len(coordinates) // 3:
                    grid[y][x] = '*'  # Middle of path
                else:
                    grid[y][x] = '#'  # End of path
    
    print("📍 Trail map (. = start, * = middle, # = end):")
    for row in grid:
        print(''.join(row))

def analyze_coordinate_movements(coordinates):
    """Analyze the sequence of movements for patterns"""
    print("\n🧭 Analyzing movement patterns...")
    
    movements = []
    for i in range(1, len(coordinates)):
        lat_diff = coordinates[i]['lat'] - coordinates[i-1]['lat']
        lon_diff = coordinates[i]['lon'] - coordinates[i-1]['lon']
        
        # Classify movement direction
        if abs(lat_diff) > abs(lon_diff):
            if lat_diff > 0:
                direction = 'N'  # North
            else:
                direction = 'S'  # South
        else:
            if lon_diff > 0:
                direction = 'E'  # East
            else:
                direction = 'W'  # West
        
        movements.append(direction)
    
    # Look for patterns in movement sequence
    movement_str = ''.join(movements)
    print(f"📊 Movement sequence (first 100): {movement_str[:100]}")
    
    # Look for repeated patterns
    for pattern_len in [3, 4, 5]:
        patterns = {}
        for i in range(len(movement_str) - pattern_len + 1):
            pattern = movement_str[i:i+pattern_len]
            patterns[pattern] = patterns.get(pattern, 0) + 1
        
        # Show most common patterns
        common_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"📊 Most common {pattern_len}-char patterns: {common_patterns}")

def try_base64_decode(coordinates):
    """Try to decode coordinates as base64"""
    print("\n🔐 Trying base64 decoding approaches...")
    
    # Extract decimal parts and try to form base64
    lat_decimals = []
    lon_decimals = []
    
    for coord in coordinates:
        lat_str = f"{coord['lat']:.6f}"
        lon_str = f"{coord['lon']:.6f}"
        
        lat_decimal = lat_str.split('.')[1]
        lon_decimal = lon_str.split('.')[1]
        
        lat_decimals.append(lat_decimal)
        lon_decimals.append(lon_decimal)
    
    # Try different approaches
    print(f"📊 First 10 lat decimals: {lat_decimals[:10]}")
    print(f"📊 First 10 lon decimals: {lon_decimals[:10]}")

def main():
    print("🏁 Final Trail Trace Solver")
    print("=" * 50)
    
    try:
        coordinates = load_coordinates('gps_coordinates.txt')
        print(f"📍 Loaded {len(coordinates)} GPS coordinates")
        
        # Focus on most promising approaches
        decode_timestamp_message(coordinates)
        create_compact_trail_map(coordinates)
        analyze_coordinate_movements(coordinates)
        try_base64_decode(coordinates)
        
        print("\n💡 SUMMARY OF FINDINGS:")
        print("💡 1. Timestamp intervals form a coded message")
        print("💡 2. GPS coordinates might form text when plotted")
        print("💡 3. Movement patterns could encode information")
        print("💡 Try plotting coordinates on Google Maps/Earth for visual flag!")
        
        # Generate Google Maps URL
        center_lat = sum(c['lat'] for c in coordinates) / len(coordinates)
        center_lon = sum(c['lon'] for c in coordinates) / len(coordinates)
        
        print(f"\n🌐 Google Maps Center: {center_lat:.6f}, {center_lon:.6f}")
        print(f"🌐 URL: https://www.google.com/maps/@{center_lat},{center_lon},18z")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
