#!/usr/bin/env python3
"""
GPS Art Reader - Final attempt to read the flag from GPS coordinates
Looking at the grid pattern more carefully for readable text
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

def create_readable_grid(coordinates):
    """Create a high resolution grid that might show readable text"""
    print("🎨 Creating high-resolution GPS art grid...")
    
    lats = [c['lat'] for c in coordinates]
    lons = [c['lon'] for c in coordinates]
    
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Use very high resolution
    width, height = 120, 40
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Map coordinates to grid
    for coord in coordinates:
        if max_lat != min_lat and max_lon != min_lon:
            x = int(((coord['lon'] - min_lon) / (max_lon - min_lon)) * (width - 1))
            y = int(((coord['lat'] - min_lat) / (max_lat - min_lat)) * (height - 1))
            y = height - 1 - y  # Flip Y axis
            
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = '#'
    
    return grid

def analyze_grid_for_text(grid):
    """Analyze grid for readable text patterns"""
    print("🔍 Analyzing grid for readable text...")
    
    height = len(grid)
    width = len(grid[0]) if grid else 0
    
    # Print grid with line numbers for analysis
    print("\n📍 High Resolution Grid:")
    for i, row in enumerate(grid):
        line = ''.join(row)
        if '#' in line:  # Only show lines with content
            print(f"{i:2}: {line}")
    
    # Look for letter-like patterns by analyzing sections
    print(f"\n🔤 Looking for letter patterns in {width}x{height} grid...")
    
    # Divide grid into potential character sections
    chars_per_line = 8  # Estimate 8 characters wide
    char_width = width // chars_per_line
    
    for char_pos in range(chars_per_line):
        start_x = char_pos * char_width
        end_x = min(start_x + char_width, width)
        
        print(f"\n🔤 Character position {char_pos + 1} (x: {start_x}-{end_x}):")
        
        # Extract this character's pattern
        char_pattern = []
        for y in range(height):
            char_line = ''.join(grid[y][start_x:end_x])
            if '#' in char_line:
                char_pattern.append(char_line)
        
        if char_pattern:
            for line in char_pattern[-10:]:  # Show last 10 lines of pattern
                print(f"    {line}")
            
            # Try to identify the character
            analyze_character_pattern(char_pattern)

def analyze_character_pattern(pattern):
    """Try to identify what character this pattern represents"""
    if not pattern:
        return
    
    # Count filled positions
    total_filled = sum(line.count('#') for line in pattern)
    
    # Look for characteristic patterns
    if total_filled == 0:
        print(f"      -> Empty/Space")
        return
    
    # Check for common letter patterns
    pattern_str = '\n'.join(pattern)
    
    # Look for specific letter characteristics
    if pattern_str.count('#') > 20:
        print(f"      -> Dense pattern (possibly M, W, N, or similar)")
    elif any('###' in line for line in pattern):
        print(f"      -> Has horizontal lines (possibly E, F, T, L)")
    elif any(line.startswith('#') and line.endswith('#') for line in pattern):
        print(f"      -> Vertical sides (possibly O, D, B, P)")
    else:
        print(f"      -> {total_filled} filled positions")

def try_different_orientations(coordinates):
    """Try rotating/flipping the coordinates to read text"""
    print("\n🔄 Trying different orientations...")
    
    # Original
    print("\n📍 Original orientation:")
    grid = create_readable_grid(coordinates)
    analyze_grid_for_text(grid)
    
    # Flip horizontally
    print("\n📍 Horizontally flipped:")
    flipped_coords = []
    lons = [c['lon'] for c in coordinates]
    max_lon = max(lons)
    for coord in coordinates:
        flipped_coords.append({
            'lat': coord['lat'],
            'lon': max_lon - coord['lon'],
            'time': coord['time']
        })
    
    grid_flipped = create_readable_grid(flipped_coords)
    
    # Print compact version
    print("📍 Flipped grid (compact):")
    for i, row in enumerate(grid_flipped):
        line = ''.join(row)
        if '#' in line:
            print(f"{i:2}: {line}")

def extract_flag_from_visual(coordinates):
    """Final attempt to extract flag by visual analysis"""
    print("\n🏁 Final Flag Extraction Attempt")
    print("=" * 50)
    
    # Create the most readable grid possible
    grid = create_readable_grid(coordinates)
    
    # Focus on areas with dense patterns (likely text)
    dense_areas = []
    for y in range(len(grid)):
        line = ''.join(grid[y])
        if line.count('#') >= 5:  # Lines with at least 5 marks
            dense_areas.append((y, line))
    
    print(f"📊 Found {len(dense_areas)} dense pattern lines:")
    for y, line in dense_areas:
        print(f"  Line {y:2}: {line}")
    
    # Manual pattern recognition
    print("\n🎯 Manual Pattern Analysis:")
    print("Looking for [REDACTED] pattern in the grid...")
    
    # Try to read the grid as text by looking at the overall pattern
    print("\n📍 Attempting to read text from GPS art:")
    
    # Compact view of entire trail
    compact_grid = [[' ' for _ in range(40)] for _ in range(15)]
    
    lats = [c['lat'] for c in coordinates]
    lons = [c['lon'] for c in coordinates]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    for coord in coordinates:
        if max_lat != min_lat and max_lon != min_lon:
            x = int(((coord['lon'] - min_lon) / (max_lon - min_lon)) * 39)
            y = int(((coord['lat'] - min_lat) / (max_lat - min_lat)) * 14)
            y = 14 - y  # Flip Y
            
            if 0 <= x < 40 and 0 <= y < 15:
                compact_grid[y][x] = '#'
    
    print("📍 Compact trail view:")
    for i, row in enumerate(compact_grid):
        print(f"{i:2}: {''.join(row)}")

def main():
    print("🎨 GPS Art Reader - Final Flag Decoder")
    print("=" * 60)
    
    try:
        coordinates = load_coordinates('gps_coordinates.txt')
        print(f"📍 Loaded {len(coordinates)} GPS coordinates")
        
        # Final comprehensive analysis
        extract_flag_from_visual(coordinates)
        try_different_orientations(coordinates)
        
        print("\n🎯 CONCLUSION:")
        print("🏁 The GPS coordinates form a visual pattern that should spell out the flag")
        print("🏁 Use the generated trail.kml file in Google Earth to see the actual shape")
        print("🏁 The criminal's path spells out text when viewed from above!")
        
        # Provide final hint
        print("\n💡 FINAL HINT:")
        print("💡 Open trail.kml in Google Earth or plot coordinates on a mapping service")
        print("💡 Zoom out to see the complete text formed by the GPS trail")
        print("💡 The flag format should be [REDACTED] spelled out by the path")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
