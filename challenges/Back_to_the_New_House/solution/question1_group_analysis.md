# Back to the New House - Question 1 Solution

## Question: "What group has been made on the Windows machine?"

## Answer: **thesmiths**

## Analysis Process

### 1. Files Analyzed
- `Security.evtx` - Windows Security Event Log
- Location: `/challenges/Back_to_the_New_House/logs (2).zip`

### 2. Method Used
- Extracted Windows Event Logs from zip file
- Used `evtx_dump` tool to parse binary .evtx files
- Searched for Event ID 4731 (security-enabled local group creation)

### 3. Key Evidence

**Event Details:**
- **Event ID**: 4731 (A security-enabled local group was created)
- **Group Name**: `thesmiths`
- **Target Domain**: `DESKTOP-P5L8521`
- **Created By**: User `agent`
- **Process**: `mmc.exe` (Microsoft Management Console)
- **Timestamp**: 2025-07-02 (multiple related events)

**Event Log Entry:**
```xml
<Data Name="TargetUserName">thesmiths</Data>
<Data Name="TargetDomainName">DESKTOP-P5L8521</Data>
<Data Name="TargetSid">S-1-5-21-2584721208-1353900670-1627748517-1008</Data>
<Data Name="SubjectUserName">agent</Data>
<Data Name="SubjectDomainName">DESKTOP-P5L8521</Data>
```

### 4. Context
While the Security log showed creation of many built-in Windows groups (Remote Desktop Users, Network Configuration Operators, etc.), `thesmiths` was the only custom/non-standard group created, making it the clear answer to the question.

### 5. Tools Used
- `evtx_dump` - Windows Event Log parser
- `grep` - Text filtering
- Custom Python analysis script

## Verification
The group creation was followed by multiple member addition events (Event ID 4732), confirming that `thesmiths` was actively used and populated with users.
