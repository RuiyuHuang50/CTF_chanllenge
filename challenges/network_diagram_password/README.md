# Network Diagram Password

**Challenge Type:** Steganography / Visual Cryptography
**Date Solved:** 2025-09-12
**Difficulty:** Medium

## Challenge Description
We managed to get this redacted network diagram. The password appears to be covered/blocked out, but we need to extract it from the file.

## Solution Process
1. **Initial Analysis**: Received a draw.io network diagram saved as PNG with visually redacted password
2. **String Extraction**: Used `strings` command to extract embedded data from PNG file
3. **XML Analysis**: Found that draw.io files contain XML data embedded in PNG format
4. **Hidden Text Discovery**: Located scattered text elements positioned under redaction blocks
5. **Flag Assembly**: Reassembled the text fragments in correct order

## Technical Details
- Draw.io files embedded in PNG contain full XML source code
- Visual redaction only covers text elements but doesn't remove them from XML
- Text was split into multiple small elements: `mn`, `e{`, `le`, `aky`, `_s`, `tu`, `ff`, `_in`, `_thi`, `s_fi`, `le}`
- Elements were positioned sequentially and covered by gray redaction rectangles

## Flag
[REDACTED - Submit solution to competition organizers]

## Files
- `solution/solve.py` - Automated solution script
- `files/classified network.drawio.png` - Original challenge file
- `notes/analysis.md` - Detailed analysis notes

## Lessons Learned
- Visual redaction ≠ data removal - always check source data
- Draw.io PNG files contain full XML, making them vulnerable to data leakage
- String extraction is often the first step in analyzing embedded file formats
- CTF flags often have contextual meaning ("leaky stuff in this file" - very meta!)

## Alternative Methods
- Could also open the PNG in a hex editor and search for XML content
- Draw.io files can sometimes be directly imported/opened to reveal source
- OCR might work on unredacted portions but wouldn't help with covered text
