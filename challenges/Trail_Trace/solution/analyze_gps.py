#!/usr/bin/env python3
"""
Trail Trace Challenge Solver
Parse NMEA GPS data from PCAP file to trace criminal's path

Challenge: "We've recovered data from a tracker planted on an elusive criminal, can you trace their steps?"
Hint: Study the NMEA protocol here: https://docs.arduino.cc/learn/communication/gps-nmea-data-101/
"""

import subprocess
import re
import sys
from datetime import datetime

def extract_nmea_from_pcap(pcap_file):
    """Extract NMEA sentences from PCAP file using tcpdump"""
    print("🔍 Extracting NMEA GPS data from PCAP...")
    
    try:
        # Use tcpdump to extract ASCII data
        result = subprocess.run(['tcpdump', '-r', pcap_file, '-A', '-n'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error running tcpdump: {result.stderr}")
            return []
        
        # Extract NMEA sentences
        nmea_sentences = []
        lines = result.stdout.split('\n')
        
        for line in lines:
            # Look for lines containing NMEA GPS sentences
            if '$GP' in line:
                # Extract the NMEA sentence part
                match = re.search(r'\$GP[A-Z]{3},[^*]*\*[0-9A-F]{2}', line)
                if match:
                    nmea_sentences.append(match.group(0))
        
        print(f"📊 Found {len(nmea_sentences)} NMEA sentences")
        return nmea_sentences
        
    except FileNotFoundError:
        print("❌ tcpdump not found. Please install tcpdump.")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def parse_nmea_coordinates(nmea_sentence):
    """Parse latitude and longitude from NMEA sentence"""
    
    if not nmea_sentence.startswith('$GPGGA'):
        return None
    
    # Split NMEA sentence by commas
    fields = nmea_sentence.split(',')
    
    if len(fields) < 6:
        return None
    
    try:
        # GPGGA format: $GPGGA,time,lat,lat_dir,lon,lon_dir,quality,...
        time_str = fields[1]
        lat_raw = fields[2]
        lat_dir = fields[3]
        lon_raw = fields[4]
        lon_dir = fields[5]
        
        if not all([lat_raw, lat_dir, lon_raw, lon_dir]):
            return None
        
        # Convert DDMM.MMMMM format to decimal degrees
        # Latitude: DDMM.MMMMM (DD = degrees, MM.MMMMM = minutes)
        lat_deg = int(lat_raw[:2])
        lat_min = float(lat_raw[2:])
        latitude = lat_deg + lat_min / 60.0
        if lat_dir == 'S':
            latitude = -latitude
        
        # Longitude: DDDMM.MMMMM (DDD = degrees, MM.MMMMM = minutes)
        lon_deg = int(lon_raw[:3])
        lon_min = float(lon_raw[3:])
        longitude = lon_deg + lon_min / 60.0
        if lon_dir == 'W':
            longitude = -longitude
        
        return {
            'time': time_str,
            'latitude': latitude,
            'longitude': longitude,
            'raw_sentence': nmea_sentence
        }
        
    except (ValueError, IndexError) as e:
        print(f"⚠️  Error parsing NMEA: {e}")
        return None

def analyze_gps_trail(coordinates):
    """Analyze the GPS trail to find patterns or hidden messages"""
    print("\n🗺️  GPS Trail Analysis")
    print("=" * 50)
    
    if not coordinates:
        print("❌ No coordinates to analyze")
        return
    
    print(f"📍 Total GPS points: {len(coordinates)}")
    
    # Show first and last coordinates
    first = coordinates[0]
    last = coordinates[-1]
    
    print(f"🚩 Starting position: {first['latitude']:.6f}, {first['longitude']:.6f}")
    print(f"🏁 Ending position: {last['latitude']:.6f}, {last['longitude']:.6f}")
    
    # Calculate basic statistics
    lats = [c['latitude'] for c in coordinates]
    lons = [c['longitude'] for c in coordinates]
    
    lat_range = max(lats) - min(lats)
    lon_range = max(lons) - min(lons)
    
    print(f"📊 Latitude range: {lat_range:.6f} degrees")
    print(f"📊 Longitude range: {lon_range:.6f} degrees")
    
    # Look for patterns in coordinates
    print("\n🔍 Looking for patterns...")
    
    # Check if coordinates form specific shapes or spell out letters/numbers
    # Convert coordinates to a more manageable grid system
    normalized_coords = []
    min_lat, min_lon = min(lats), min(lons)
    
    for coord in coordinates:
        norm_lat = int((coord['latitude'] - min_lat) * 100000)  # Scale for visibility
        norm_lon = int((coord['longitude'] - min_lon) * 100000)
        normalized_coords.append((norm_lat, norm_lon))
    
    # Print coordinate path for pattern analysis
    print(f"\n📍 First 10 coordinates (raw):")
    for i, coord in enumerate(coordinates[:10]):
        print(f"  {i+1:2}: {coord['latitude']:.6f}, {coord['longitude']:.6f}")
    
    print(f"\n📍 Last 10 coordinates (raw):")
    for i, coord in enumerate(coordinates[-10:], len(coordinates)-9):
        print(f"  {i:2}: {coord['latitude']:.6f}, {coord['longitude']:.6f}")
    
    # Look for potential flag patterns in coordinate differences
    analyze_coordinate_patterns(coordinates)
    
    # Generate map visualization hint
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    
    print(f"\n🗺️  Center point: {center_lat:.6f}, {center_lon:.6f}")
    print(f"🌐 Google Maps: https://www.google.com/maps/@{center_lat},{center_lon},15z")
    
    return coordinates

def analyze_coordinate_patterns(coordinates):
    """Look for patterns that might spell out text or form shapes"""
    print("\n🧩 Pattern Analysis:")
    
    # Calculate relative movements
    movements = []
    for i in range(1, len(coordinates)):
        lat_diff = coordinates[i]['latitude'] - coordinates[i-1]['latitude']
        lon_diff = coordinates[i]['longitude'] - coordinates[i-1]['longitude']
        movements.append((lat_diff, lon_diff))
    
    # Look for repeated patterns or significant direction changes
    significant_moves = [(lat, lon) for lat, lon in movements if abs(lat) > 0.0001 or abs(lon) > 0.0001]
    
    print(f"📈 Significant movements: {len(significant_moves)}")
    
    # Try to detect if coordinates form ASCII art or text
    # This is a simplified approach - real GPS art detection would be more complex
    lats = [c['latitude'] for c in coordinates]
    lons = [c['longitude'] for c in coordinates]
    
    # Normalize to a grid
    lat_range = max(lats) - min(lats)
    lon_range = max(lons) - min(lons)
    
    if lat_range > 0 and lon_range > 0:
        grid_size = 20  # 20x20 grid
        grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
        
        for coord in coordinates:
            # Map coordinate to grid position
            grid_lat = int(((coord['latitude'] - min(lats)) / lat_range) * (grid_size - 1))
            grid_lon = int(((coord['longitude'] - min(lons)) / lon_range) * (grid_size - 1))
            grid[grid_lat][grid_lon] = '*'
        
        print("\n🎨 GPS Trail Visualization (rough):")
        for row in reversed(grid):  # Reverse to match map orientation
            print(''.join(row))

def main():
    print("🕵️  Trail Trace Challenge Solver")
    print("=" * 50)
    
    pcap_file = "log.pcap"
    
    # Extract NMEA sentences from PCAP
    nmea_sentences = extract_nmea_from_pcap(pcap_file)
    
    if not nmea_sentences:
        print("❌ No NMEA sentences found")
        return
    
    # Parse coordinates from NMEA sentences
    coordinates = []
    for sentence in nmea_sentences:
        coord = parse_nmea_coordinates(sentence)
        if coord:
            coordinates.append(coord)
    
    print(f"✅ Parsed {len(coordinates)} valid GPS coordinates")
    
    # Analyze the trail
    analyze_gps_trail(coordinates)
    
    # Look for hidden messages
    print("\n🔍 Searching for hidden patterns or flag...")
    
    # The flag might be:
    # 1. Formed by the GPS path (GPS art)
    # 2. Hidden in the coordinate values themselves
    # 3. Encoded in the sequence of movements
    
    # Check if coordinates spell out text when plotted
    if coordinates:
        print("\n💡 Try plotting these coordinates on a map to see if they form letters/numbers!")
        print("💡 The path might spell out the flag when viewed from above!")
        
        # Save coordinates to file for external plotting
        with open('gps_coordinates.txt', 'w') as f:
            f.write("latitude,longitude,time\n")
            for coord in coordinates:
                f.write(f"{coord['latitude']:.6f},{coord['longitude']:.6f},{coord['time']}\n")
        
        print("📄 Coordinates saved to 'gps_coordinates.txt'")

if __name__ == "__main__":
    main()
