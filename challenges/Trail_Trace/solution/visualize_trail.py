#!/usr/bin/env python3
"""
Enhanced GPS Visualization for Trail Trace Challenge
Creates a better visualization of the GPS path to reveal hidden text/flag
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

def create_ascii_map(coordinates, width=80, height=25):
    """Create an ASCII art representation of the GPS path"""
    if not coordinates:
        return []
    
    lats = [c['lat'] for c in coordinates]
    lons = [c['lon'] for c in coordinates]
    
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Create grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Map each coordinate to grid position
    for coord in coordinates:
        if max_lat != min_lat and max_lon != min_lon:
            # Normalize coordinates to grid
            x = int(((coord['lon'] - min_lon) / (max_lon - min_lon)) * (width - 1))
            y = int(((coord['lat'] - min_lat) / (max_lat - min_lat)) * (height - 1))
            
            # Flip Y axis to match normal orientation
            y = height - 1 - y
            
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = '*'
    
    return grid

def print_ascii_map(grid):
    """Print the ASCII map"""
    for row in grid:
        print(''.join(row))

def analyze_text_pattern(coordinates):
    """Try to detect if the path spells out text"""
    print("🔍 Advanced Pattern Analysis")
    print("=" * 50)
    
    # Create a higher resolution ASCII map
    high_res_grid = create_ascii_map(coordinates, width=120, height=40)
    
    print("\n📍 High Resolution GPS Trail Map:")
    print_ascii_map(high_res_grid)
    
    # Try different orientations
    print("\n🔄 Trying different orientations...")
    
    # Create multiple views with different aspect ratios
    views = [
        (60, 20, "Wide view"),
        (40, 30, "Tall view"),
        (80, 25, "Standard view"),
        (100, 30, "Extra wide view")
    ]
    
    for width, height, desc in views:
        print(f"\n📺 {desc} ({width}x{height}):")
        grid = create_ascii_map(coordinates, width, height)
        print_ascii_map(grid)

def extract_potential_flag_patterns(coordinates):
    """Look for patterns that might be flag characters"""
    print("\n🏁 Flag Pattern Detection")
    print("=" * 50)
    
    # Look for rectangular regions that might be letters
    lats = [c['lat'] for c in coordinates]
    lons = [c['lon'] for c in coordinates]
    
    # Group coordinates by similar latitude (horizontal lines)
    lat_groups = {}
    for coord in coordinates:
        lat_key = round(coord['lat'], 5)  # Round to group similar latitudes
        if lat_key not in lat_groups:
            lat_groups[lat_key] = []
        lat_groups[lat_key].append(coord)
    
    print(f"📊 Found {len(lat_groups)} horizontal line groups")
    
    # Group coordinates by similar longitude (vertical lines)
    lon_groups = {}
    for coord in coordinates:
        lon_key = round(coord['lon'], 5)  # Round to group similar longitudes
        if lon_key not in lon_groups:
            lon_groups[lon_key] = []
        lon_groups[lon_key].append(coord)
    
    print(f"📊 Found {len(lon_groups)} vertical line groups")
    
    # Look for segments that might be characters
    sorted_lons = sorted(lon_groups.keys())
    
    print("\n🔤 Potential character segments:")
    for i, lon in enumerate(sorted_lons[:10]):  # Show first 10 segments
        points = len(lon_groups[lon])
        print(f"  Segment {i+1}: Longitude {lon:.5f} - {points} points")

def main():
    print("🎨 Enhanced GPS Trail Visualization")
    print("=" * 50)
    
    try:
        coordinates = load_coordinates('gps_coordinates.txt')
        print(f"📍 Loaded {len(coordinates)} GPS coordinates")
        
        # Create ASCII visualization
        analyze_text_pattern(coordinates)
        
        # Look for flag patterns
        extract_potential_flag_patterns(coordinates)
        
        # Create a detailed character-by-character map
        print("\n🔍 Detailed Character Map Analysis:")
        
        # Create very high resolution view
        ultra_grid = create_ascii_map(coordinates, width=160, height=50)
        
        print("\n📍 Ultra High Resolution Map:")
        for i, row in enumerate(ultra_grid):
            print(f"{i:2}: {''.join(row)}")
        
        print("\n💡 HINT: Look for patterns that might spell out '[REDACTED]'")
        print("💡 The path should form readable text when viewed from above!")
        
    except FileNotFoundError:
        print("❌ Could not find gps_coordinates.txt")
        print("💡 Run analyze_gps.py first to generate coordinates")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
