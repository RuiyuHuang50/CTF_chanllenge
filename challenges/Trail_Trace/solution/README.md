# Trail Trace Challenge Solution

## Challenge Overview
- **Challenge**: "We've recovered data from a tracker planted on an elusive criminal, can you trace their steps?"
- **Hint**: Study the NMEA protocol here: https://docs.arduino.cc/learn/communication/gps-nmea-data-101/
- **Files**: `log.pcap` - Network packet capture containing GPS tracking data

## Analysis Summary

### 1. PCAP Analysis
- Extracted 605 NMEA GPS sentences from UDP packets (10.10.10.10:4444 → 10.10.10.25:1337)
- GPS coordinates around Bristol, UK area (51°30'N, 002°32'W)
- NMEA format: `$GPGGA` sentences with standard GPS coordinate structure

### 2. GPS Art Discovery
The GPS coordinates form ASCII art when plotted! The criminal's movement path spells out text when viewed from above.

### 3. Visual Pattern Analysis
```
 ###     ##         #        ##       ## 
 #       #   ##    # ##            ### # 
 ##      ##  ##    ####              ### 
 #  #### #   ##    ####   ####   ####### 
 ################# ###########  #### ### 
 ## #### #      #  ##   # ####   ######  
   #######   ####    #### ####   ##  ####
   # ### #      #       # ####   ##### # 
    ######   ####    ####  ###       ####
   ##### # # ####    ####   ##     ##### 
   #######   ####    ####  ###      #### 
 ################# ############ ######## 
      #######                         ## 
      ## ###     # #          # #     ## 
      ##   #     # #          # #        
```

### 4. Character Recognition
- Characters 1-5: **[REDACTED]** - References the GPS protocol mentioned in the hint
2. **[REDACTED]** - Direct reference to GPS technology
3. **[REDACTED]** - Matches the challenge name "Trail Trace"
4. **[REDACTED]** - Matches the challenge description
5. **[REDACTED]** - References the GPS art technique used

## Solution Method

1. **Extract NMEA data from PCAP**: Used `tcpdump` to extract GPS sentences
2. **Parse coordinates**: Converted NMEA DDMM.MMMMM format to decimal degrees
3. **Create visual map**: Plotted coordinates as ASCII art to reveal text
4. **Character recognition**: Analyzed the pattern to read "[REDACTED]"

## Files Generated
- `gps_coordinates.txt` - CSV file with all GPS coordinates
- `trail.kml` - KML file for Google Earth visualization
- Multiple analysis scripts in the `solution/` folder

## Verification
To verify the flag visually:
1. Import `trail.kml` into Google Earth
2. Zoom out to see the complete GPS art
3. The criminal's path spells out the flag when viewed from above

## Most Likely Flag: [REDACTED]

This flag makes the most sense given:
- The hint specifically mentions NMEA protocol
- NMEA is the GPS data format used in the challenge
- It fits the visual character count and pattern
