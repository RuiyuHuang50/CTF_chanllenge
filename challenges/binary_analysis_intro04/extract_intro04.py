#!/usr/bin/env python3
import zipfile
import os

# Extract the intro04 zip file
zip_path = "/Users/mac/VirtualBox VMs/CTF_chanllenge/intro04/intro04 (1).zip"
extract_path = "/Users/mac/VirtualBox VMs/CTF_chanllenge/intro04/"

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        print("✅ Successfully extracted intro04.zip")
        
        # List extracted files
        print("\nExtracted files:")
        for root, dirs, files in os.walk(extract_path):
            for file in files:
                if file != "intro04 (1).zip":  # Skip the original zip
                    file_path = os.path.join(root, file)
                    print(f"📁 {file_path}")
                    
except Exception as e:
    print(f"❌ Error extracting file: {e}")
