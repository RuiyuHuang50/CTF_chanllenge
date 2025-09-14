#!/usr/bin/env python3
"""
Group Member Analyzer for Back to the New House Challenge
Extract usernames of members in the thesmiths group
"""

import re
import xml.etree.ElementTree as ET

def extract_group_members():
    """Extract members of thesmiths group from Security log"""
    print("🔍 Analyzing thesmiths group membership...")
    
    # First, let's find the SIDs of group members
    member_sids = [
        "S-1-5-21-2584721208-1353900670-1627748517-1003",
        "S-1-5-21-2584721208-1353900670-1627748517-1006", 
        "S-1-5-21-2584721208-1353900670-1627748517-1004",
        "S-1-5-21-2584721208-1353900670-1627748517-1007",
        "S-1-5-21-2584721208-1353900670-1627748517-1005"
    ]
    
    print(f"📊 Found {len(member_sids)} member SIDs in thesmiths group")
    
    # Read the security dump and find username mappings
    try:
        with open("security_dump.xml", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Find user creation events (Event ID 4720) to map SIDs to usernames
        usernames = {}
        
        # Look for Event ID 4720 patterns
        events = content.split("<Event xmlns=")
        
        for event in events:
            if "EventID>4720<" in event:
                # Extract TargetUserName and TargetSid
                username_match = re.search(r'<Data Name="TargetUserName">([^<]+)</Data>', event)
                sid_match = re.search(r'<Data Name="TargetSid">([^<]+)</Data>', event)
                
                if username_match and sid_match:
                    username = username_match.group(1)
                    sid = sid_match.group(1)
                    usernames[sid] = username
        
        print(f"📊 Found {len(usernames)} username-to-SID mappings")
        
        # Map the member SIDs to usernames
        group_members = []
        
        for sid in member_sids:
            if sid in usernames:
                member_name = usernames[sid]
                group_members.append(member_name)
                print(f"  ✅ {sid} -> {member_name}")
            else:
                print(f"  ❌ SID not found: {sid}")
        
        # Sort alphabetically as requested
        group_members.sort()
        
        print(f"\n🏁 THESMITHS GROUP MEMBERS:")
        print(f"  {', '.join(group_members)}")
        
        return group_members
        
    except FileNotFoundError:
        print("❌ security_dump.xml not found")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def verify_with_direct_search():
    """Verify by directly searching the security dump"""
    print("\n🔍 Verification by direct search...")
    
    try:
        with open("security_dump.xml", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Look for all usernames in the content
        usernames = re.findall(r'<Data Name="TargetUserName">([^<]+)</Data>', content)
        unique_usernames = list(set(usernames))
        
        print(f"📊 All unique usernames found: {len(unique_usernames)}")
        
        # Filter for likely group member names (exclude system accounts)
        likely_members = []
        for username in unique_usernames:
            if username.lower() not in ['administrator', 'guest', 'wdagutilityaccount', 'agent', 'thesmiths']:
                if len(username) > 2 and username.isalpha():
                    likely_members.append(username)
        
        likely_members.sort()
        print(f"📊 Likely user accounts (excluding system): {likely_members}")
        
        return likely_members
        
    except Exception as e:
        print(f"❌ Error in verification: {e}")
        return []

def main():
    print("🕵️  Group Member Analyzer")
    print("=" * 50)
    
    # Extract group members using SID mapping
    members = extract_group_members()
    
    # Verify with direct search
    verify_with_direct_search()
    
    if members:
        print(f"\n🏁 FINAL ANSWER:")
        print(f"  {', '.join(members)}")
    else:
        print("\n❌ No group members identified")

if __name__ == "__main__":
    main()
