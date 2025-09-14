#!/usr/bin/env python3
"""
Web CTF Challenge Analyzer
Comprehensive analysis of web challenges for hidden flags
"""

import requests
import re
import base64
import binascii
from urllib.parse import urljoin, urlparse
import time

class WebCTFAnalyzer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def analyze_main_page(self):
        """Analyze the main page for flags and hints"""
        print(f"🔍 Analyzing main page: {self.base_url}")
        print("=" * 60)
        
        try:
            response = self.session.get(self.base_url)
            print(f"Status Code: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"Content-Length: {len(response.content)} bytes")
            
            # Check response headers for flags
            self.check_headers(response.headers)
            
            # Analyze HTML content
            html_content = response.text
            print(f"\n📄 HTML Content Analysis:")
            print("-" * 30)
            
            # Look for flags in various formats
            flags = self.find_flags_in_text(html_content)
            if flags:
                print(f"🚩 POTENTIAL FLAGS FOUND IN HTML:")
                for flag in flags:
                    print(f"   {flag}")
            
            # Look for comments
            comments = re.findall(r'<!--(.*?)-->', html_content, re.DOTALL)
            if comments:
                print(f"\n💬 HTML Comments found:")
                for i, comment in enumerate(comments, 1):
                    print(f"   Comment {i}: {comment.strip()}")
                    comment_flags = self.find_flags_in_text(comment)
                    if comment_flags:
                        print(f"   🚩 FLAG IN COMMENT: {comment_flags}")
            
            # Look for hidden inputs
            hidden_inputs = re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*>', html_content, re.IGNORECASE)
            if hidden_inputs:
                print(f"\n🔒 Hidden inputs found:")
                for inp in hidden_inputs:
                    print(f"   {inp}")
            
            # Look for JavaScript
            js_content = re.findall(r'<script[^>]*>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE)
            if js_content:
                print(f"\n📜 JavaScript found:")
                for i, js in enumerate(js_content, 1):
                    if js.strip():
                        print(f"   Script {i}: {js.strip()[:200]}...")
                        js_flags = self.find_flags_in_text(js)
                        if js_flags:
                            print(f"   🚩 FLAG IN JS: {js_flags}")
            
            # Look for base64 encoded content
            self.check_base64_content(html_content)
            
            return response, html_content
            
        except Exception as e:
            print(f"❌ Error analyzing main page: {e}")
            return None, None
    
    def check_headers(self, headers):
        """Check HTTP headers for flags or hints"""
        print(f"\n📋 HTTP Headers Analysis:")
        print("-" * 30)
        
        for header, value in headers.items():
            print(f"   {header}: {value}")
            
            # Look for flags in headers
            flags = self.find_flags_in_text(value)
            if flags:
                print(f"   🚩 FLAG IN HEADER {header}: {flags}")
    
    def find_flags_in_text(self, text):
        """Find potential flags in text using common CTF flag patterns"""
        flag_patterns = [
            r'[a-zA-Z0-9]+\{[^}]+\}',  # General flag format
            r'flag\{[^}]+\}',          # [REDACTED]
            r'ctf\{[^}]+\}',           # [REDACTED]
            r'bootup\{[^}]+\}',        # [REDACTED]
            r'mne\{[^}]+\}',           # [REDACTED]
            r'FLAG\{[^}]+\}',          # [REDACTED]
            r'CTF\{[^}]+\}',           # [REDACTED]
        ]
        
        flags = []
        for pattern in flag_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            flags.extend(matches)
        
        return list(set(flags))  # Remove duplicates
    
    def check_base64_content(self, text):
        """Look for base64 encoded content that might contain flags"""
        print(f"\n🔐 Base64 Analysis:")
        print("-" * 30)
        
        # Look for base64-like strings
        base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
        potential_b64 = re.findall(base64_pattern, text)
        
        for b64_str in potential_b64:
            try:
                decoded = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
                if decoded.isprintable() and len(decoded) > 3:
                    print(f"   B64: {b64_str[:50]}...")
                    print(f"   Decoded: {decoded}")
                    
                    flags = self.find_flags_in_text(decoded)
                    if flags:
                        print(f"   🚩 FLAG IN BASE64: {flags}")
            except:
                continue
    
    def check_common_paths(self):
        """Check common paths that might contain flags"""
        print(f"\n🗂️  Common Paths Analysis:")
        print("-" * 30)
        
        common_paths = [
            '/robots.txt',
            '/sitemap.xml',
            '/.htaccess',
            '/flag.txt',
            '/flag',
            '/admin',
            '/hidden',
            '/secret',
            '/source',
            '/backup',
            '/debug',
            '/test',
            '/dev',
            '/.git',
            '/.env',
            '/config',
            '/api',
            '/flag.php',
            '/flag.html',
            '/index.php',
            '/source.php',
            '/view-source',
        ]
        
        for path in common_paths:
            try:
                url = urljoin(self.base_url, path)
                response = self.session.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"   ✅ {path} - Status: {response.status_code}")
                    
                    # Check content for flags
                    flags = self.find_flags_in_text(response.text)
                    if flags:
                        print(f"   🚩 FLAG FOUND at {path}: {flags}")
                        return flags
                    
                    # Show snippet of content
                    content_preview = response.text[:200].replace('\n', ' ').strip()
                    if content_preview:
                        print(f"      Content: {content_preview}...")
                        
                elif response.status_code in [301, 302]:
                    print(f"   🔄 {path} - Redirect: {response.status_code}")
                    location = response.headers.get('Location', 'N/A')
                    print(f"      Location: {location}")
                    
            except requests.exceptions.Timeout:
                print(f"   ⏰ {path} - Timeout")
            except Exception as e:
                # Don't print errors for expected 404s
                pass
        
        return None
    
    def analyze_images(self, html_content):
        """Analyze images for steganography or metadata"""
        print(f"\n🖼️  Image Analysis:")
        print("-" * 30)
        
        # Find image URLs
        img_patterns = [
            r'<img[^>]*src=["\']([^"\']+)["\']',
            r'background-image:\s*url\(["\']?([^)"\']+)["\']?\)',
        ]
        
        images = []
        for pattern in img_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            images.extend(matches)
        
        for img_url in images:
            try:
                full_url = urljoin(self.base_url, img_url)
                print(f"   📸 Found image: {full_url}")
                
                # Download and check image
                response = self.session.get(full_url, timeout=10)
                if response.status_code == 200:
                    print(f"      Size: {len(response.content)} bytes")
                    print(f"      Content-Type: {response.headers.get('Content-Type', 'N/A')}")
                    
                    # Save image for further analysis
                    filename = img_url.split('/')[-1]
                    if not filename:
                        filename = 'image.bin'
                    
                    filepath = f"/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/web_challenge_01/{filename}"
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"      Saved to: {filepath}")
                    
            except Exception as e:
                print(f"      ❌ Error downloading {img_url}: {e}")
    
    def run_full_analysis(self):
        """Run complete analysis of the web challenge"""
        print("🕸️  WEB CTF CHALLENGE ANALYZER")
        print("=" * 60)
        
        # Analyze main page
        response, html_content = self.analyze_main_page()
        
        if html_content:
            # Check common paths
            path_flags = self.check_common_paths()
            if path_flags:
                return path_flags
            
            # Analyze images
            self.analyze_images(html_content)
        
        print(f"\n🔍 Analysis complete. Check downloaded files for further investigation.")
        return None

def main():
    url = "https://2-we01.bootupctf.net/"
    
    analyzer = WebCTFAnalyzer(url)
    flags = analyzer.run_full_analysis()
    
    if flags:
        print(f"\n🎉 FLAGS FOUND:")
        for flag in flags:
            print(f"   🚩 {flag}")
    else:
        print(f"\n🤔 No obvious flags found. Manual investigation may be required.")

if __name__ == "__main__":
    main()
