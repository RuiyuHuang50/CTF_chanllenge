#!/usr/bin/env python3

"""
Create a ciphertext that will cause counter overflow
"""

def create_overflow_ciphertext():
    # Create a ciphertext with counter_length = 1 but 256 blocks
    # This should cause overflow when counter reaches 256 (can't fit in 1 byte)
    
    counter_length = 1
    num_blocks = 256
    
    # Each block is 16 bytes
    block = "deadbeefdeadbeef" * 2  # 32 hex chars = 16 bytes
    
    # Create ciphertext: counter_length + (num_blocks * 16 bytes)
    ciphertext = f"{counter_length:02x}"
    
    for i in range(num_blocks):
        ciphertext += block
    
    print(f"Ciphertext length: {len(ciphertext)} hex chars")
    print(f"Expected length: {1 + num_blocks * 16} bytes = {(1 + num_blocks * 16) * 2} hex chars")
    
    return ciphertext

def create_target_ciphertext():
    """
    Try a different approach: create a single block ciphertext with counter_length=0
    """
    
    # "open sesame" is 11 bytes, padded to 16 bytes
    # Let's try to find what the encrypted block would be
    
    # Start with a known encryption and modify it
    # We know "hello world" (11 bytes) encrypts to: 011c6c97546c91bcf8ffe96064f9c346e1
    # The encrypted block is: 1c6c97546c91bcf8ffe96064f9c346e1
    
    # Try with counter_length = 0
    target_ciphertext = "00" + "1c6c97546c91bcf8ffe96064f9c346e1"
    
    return target_ciphertext

if __name__ == "__main__":
    print("=== Overflow Ciphertext ===")
    overflow_ct = create_overflow_ciphertext()
    print(f"Overflow ciphertext: {overflow_ct[:100]}...")
    
    print("\n=== Target Ciphertext ===")
    target_ct = create_target_ciphertext()
    print(f"Target ciphertext: {target_ct}")
    
    print(f"\nTry these in the manual mode:")
    print(f"1. {target_ct}")
    print(f"2. {overflow_ct}")
