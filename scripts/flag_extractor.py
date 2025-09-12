"""
Paste your colon-separated hex string into the HEX_STRING variable below and run the script to extract readable text and flag patterns.
"""

HEX_STRING = """0x7e:0x25:0x41:0x43:0x54:0x46:0x7b:0x66:0x6c:0x61:0x67:0x5f:0x68:0x65:0x78:0x5f:0x70:0x61:0x72:0x73:0x65:0x72:0x7d"""

import re

def hex_string_to_bytes(hex_string):
    hex_values = hex_string.replace('0x', '').split(':')
    byte_array = bytearray(int(h, 16) for h in hex_values if h)
    return byte_array

def extract_flags(byte_array):
    text = byte_array.decode('utf-8', errors='ignore')
    flags = re.findall(r'(CTF\{.*?\}|flag\{.*?\}|FLAG\{.*?\})', text)
    return text, flags

if __name__ == "__main__":
    byte_array = hex_string_to_bytes(HEX_STRING)
    text, flags = extract_flags(byte_array)
    print("Decoded text:", text)
    if flags:
        print("Flags found:", flags)
    else:
        print("No flag pattern found.")
