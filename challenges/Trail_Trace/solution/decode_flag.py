#!/usr/bin/env python3
"""
GPS Flag Decoder for Trail Trace Challenge
Advanced analysis to detect text spelled by GPS coordinates
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

def create_detailed_map(coordinates):
    """Create a detailed character-readable map"""
    if not coordinates:
        return []
    
    lats = [c['lat'] for c in coordinates]
    lons = [c['lon'] for c in coordinates]
    
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Use very high resolution for text detection
    width, height = 200, 80
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Map each coordinate to grid position
    for coord in coordinates:
        if max_lat != min_lat and max_lon != min_lon:
            # Normalize coordinates to grid
            x = int(((coord['lon'] - min_lon) / (max_lon - min_lon)) * (width - 1))
            y = int(((coord['lat'] - min_lat) / (max_lat - min_lat)) * (height - 1))
            
            # Flip Y axis to match normal orientation (North up)
            y = height - 1 - y
            
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = '#'
    
    return grid

def analyze_for_flag_text(grid):
    """Analyze grid for [REDACTED] pattern"""
    print("🔍 Searching for [REDACTED] pattern in GPS trail...")
    
    # Convert grid to string for pattern matching
    text_lines = []
    for row in grid:
        text_lines.append(''.join(row))
    
    # Look for potential letters by analyzing connected components
    height = len(grid)
    width = len(grid[0]) if grid else 0
    
    # Find all marked positions
    marked_positions = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '#':
                marked_positions.append((x, y))
    
    print(f"📍 Found {len(marked_positions)} marked positions")
    
    # Group positions by x-coordinate ranges (potential letters)
    if marked_positions:
        min_x = min(pos[0] for pos in marked_positions)
        max_x = max(pos[0] for pos in marked_positions)
        
        # Divide into potential character segments
        char_width = (max_x - min_x) // 10  # Assuming ~10 characters
        if char_width == 0:
            char_width = 10
        
        print(f"📏 Character width estimate: {char_width} pixels")
        
        # Extract potential characters
        for i in range(10):  # Look for up to 10 characters
            start_x = min_x + i * char_width
            end_x = start_x + char_width
            
            # Get positions in this x range
            char_positions = [(x, y) for x, y in marked_positions if start_x <= x < end_x]
            
            if char_positions:
                print(f"\n🔤 Character {i+1} positions: {len(char_positions)} points")
                print(f"   X range: {start_x} to {end_x}")
                
                # Create mini-grid for this character
                char_min_x = min(pos[0] for pos in char_positions)
                char_max_x = max(pos[0] for pos in char_positions)
                char_min_y = min(pos[1] for pos in char_positions)
                char_max_y = max(pos[1] for pos in char_positions)
                
                char_height = char_max_y - char_min_y + 1
                char_width_actual = char_max_x - char_min_x + 1
                
                if char_height > 0 and char_width_actual > 0:
                    char_grid = [[' ' for _ in range(char_width_actual)] for _ in range(char_height)]
                    
                    for x, y in char_positions:
                        rel_x = x - char_min_x
                        rel_y = y - char_min_y
                        if 0 <= rel_x < char_width_actual and 0 <= rel_y < char_height:
                            char_grid[rel_y][rel_x] = '#'
                    
                    print(f"   Character pattern ({char_width_actual}x{char_height}):")
                    for row in char_grid:
                        print(f"   {''.join(row)}")

def print_rotated_views(coordinates):
    """Try different orientations to find readable text"""
    print("\n🔄 Trying different orientations for text readability...")
    
    # Original view
    print("\n📍 Original orientation:")
    grid = create_detailed_map(coordinates)
    for i, row in enumerate(grid[30:50]):  # Show middle section
        print(f"{i+30:2}: {''.join(row[:100])}")  # Show first 100 chars
    
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
    
    grid_flipped = create_detailed_map(flipped_coords)
    for i, row in enumerate(grid_flipped[30:50]):
        print(f"{i+30:2}: {''.join(row[:100])}")

def search_for_flag_pattern(coordinates):
    """Direct search for flag-like patterns"""
    print("\n🏁 Direct Flag Pattern Search")
    print("=" * 50)
    
    # Create high-resolution map
    grid = create_detailed_map(coordinates)
    
    # Look for common flag patterns
    flag_patterns = [
        'FLAG',
        'flag',
        'CTF',
        'UKCT',
        '{',
        '}',
        'TRAIL',
        'TRACE'
    ]
    
    # Convert grid to searchable text
    grid_text = '\n'.join(''.join(row) for row in grid)
    
    print("🔍 Searching for flag-related text patterns...")
    for pattern in flag_patterns:
        if pattern.lower() in grid_text.lower():
            print(f"✅ Found potential pattern: {pattern}")
        else:
            print(f"❌ Pattern not found: {pattern}")

def main():
    print("🏁 GPS Flag Decoder - Trail Trace Challenge")
    print("=" * 60)
    
    try:
        coordinates = load_coordinates('gps_coordinates.txt')
        print(f"📍 Loaded {len(coordinates)} GPS coordinates")
        
        # Create detailed map and analyze
        grid = create_detailed_map(coordinates)
        
        # Print compact view
        print("\n📍 High Resolution GPS Map (showing every 2nd row):")
        for i in range(0, len(grid), 2):
            row_text = ''.join(grid[i])
            if '#' in row_text:  # Only show rows with data
                print(f"{i:2}: {row_text}")
        
        # Analyze for flag text
        analyze_for_flag_text(grid)
        
        # Try different orientations
        print_rotated_views(coordinates)
        
        # Direct pattern search
        search_for_flag_pattern(coordinates)
        
        print("\n💡 ANALYSIS COMPLETE")
        print("💡 Look for patterns that spell out letters when viewed from above")
        print("💡 The criminal's path should form readable text: [REDACTED]")
        
    except FileNotFoundError:
        print("❌ Could not find gps_coordinates.txt")
        print("💡 Run analyze_gps.py first to generate coordinates")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
