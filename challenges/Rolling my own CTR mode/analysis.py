#!/usr/bin/env python3

"""
Analysis of the Rolling my own CTR mode challenge

The vulnerability is in how the counter is used:
- AES key = (counter_bytes + KEY)[:32]
- This means each block uses a different key
- We can exploit this by manipulating the counter length and values
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets

def analyze_vulnerability():
    """
    Analyze the custom CTR implementation
    """
    
    # Simulate the encryption with a known key for analysis
    KEY = b"A" * 32  # Known key for testing
    
    def encrypt_local(plaintext: bytes) -> bytes:
        plaintext = pad(plaintext, AES.block_size)
        plaintext_blocks = [plaintext[i:i+AES.block_size] for i in range(0, len(plaintext), AES.block_size)]

        counter = 0
        counter_length = (len(plaintext_blocks).bit_length() + 7) // 8
        
        ciphertext = bytearray([counter_length])

        for block in plaintext_blocks:
            counter_bytes = counter.to_bytes(counter_length, "big")
            print(f"Block {counter}: counter_bytes = {counter_bytes.hex()}")
            print(f"AES key = {(counter_bytes + KEY)[:32].hex()}")

            cipher = AES.new((counter_bytes + KEY)[:32], AES.MODE_ECB)
            ciphertext_block = cipher.encrypt(block)
            ciphertext += ciphertext_block

            counter += 1

        return bytes(ciphertext)
    
    # Test with different inputs
    test_plaintext = b"open sesame"
    print("Analyzing encryption of target plaintext:")
    print(f"Target: {test_plaintext}")
    
    ciphertext = encrypt_local(test_plaintext)
    print(f"Ciphertext: {ciphertext.hex()}")
    print(f"Counter length: {ciphertext[0]}")
    
    return ciphertext

def exploit_strategy():
    """
    Strategy to exploit the vulnerability:
    
    1. The counter length is determined by the number of blocks
    2. Different counter lengths will result in different key derivations
    3. We can potentially control the effective key by manipulating counter_length
    """
    
    print("\n=== EXPLOIT STRATEGY ===")
    print("1. The key derivation is: (counter_bytes + KEY)[:32]")
    print("2. If we can control counter_length, we can manipulate the effective key")
    print("3. Key insight: counter_length is stored as the first byte of ciphertext")
    print("4. We might be able to craft a ciphertext with a specific counter_length")
    
    # The vulnerability: if we can set counter_length to a specific value,
    # we might be able to make the encryption key predictable or exploitable
    
    print("\n=== ATTACK VECTOR ===")
    print("Option 1: Manipulate the counter_length by crafting ciphertext")
    print("Option 2: Use the fact that each block uses a different key")
    print("Option 3: Find a collision in the key space")

if __name__ == "__main__":
    print("=== Rolling my own CTR mode Analysis ===")
    
    analyze_vulnerability()
    exploit_strategy()
    
    print("\n=== NEXT STEPS ===")
    print("1. Try connecting to the server")
    print("2. Encrypt various plaintexts to understand the pattern")
    print("3. Craft a malicious ciphertext that decrypts to 'open sesame'")
