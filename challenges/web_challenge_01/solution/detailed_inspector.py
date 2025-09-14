#!/usr/bin/env python3
"""
Advanced Web Inspector for CTF
Look for hidden flags in various ways
"""

import requests
import re
from bs4 import BeautifulSoup

def inspect_page(url):
    print(f"🔍 Detailed inspection of: {url}")
    print("=" * 50)
    
    # Get the page
    response = requests.get(url)
    html = response.text
    
    print(f"HTML Content:")
    print("-" * 20)
    print(html)
    print()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check all text content (including hidden)
    print(f"All text content:")
    print("-" * 20)
    all_text = soup.get_text()
    print(repr(all_text))
    print()
    
    # Look for hidden elements
    print(f"Looking for potential hidden content...")
    print("-" * 20)
    
    # Check for elements with style attributes
    for element in soup.find_all(style=True):
        print(f"Element with style: {element}")
    
    # Check for elements with hidden class or attributes
    for element in soup.find_all(attrs={'hidden': True}):
        print(f"Hidden element: {element}")
    
    # Check for elements with display:none or visibility:hidden
    for element in soup.find_all():
        if element.get('style'):
            if 'display:none' in element.get('style').replace(' ', '') or 'visibility:hidden' in element.get('style').replace(' ', ''):
                print(f"Invisible element: {element}")
    
    # Check for any flag patterns in the raw HTML
    print(f"\nFlag pattern search:")
    print("-" * 20)
    flag_patterns = [
        r'[a-zA-Z0-9_]+\{[^}]+\}',
        r'bootup\{[^}]+\}',
        r'flag\{[^}]+\}',
        r'ctf\{[^}]+\}',
    ]
    
    for pattern in flag_patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            print(f"Found flags with pattern {pattern}: {matches}")

if __name__ == "__main__":
    inspect_page("https://2-we01.bootupctf.net/")
