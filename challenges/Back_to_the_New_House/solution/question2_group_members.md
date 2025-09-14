# Back to the New House - Question 2 Solution

## Question: "Who is in the group identified earlier? (separate multiple answers with commas and sort them alphabetically: e.g. alpha, beta, gamma, omega)."

## Answer: **colin, ed, jonny, philip, thom**

## Analysis Process

### 1. Previous Context
- Group identified in Question 1: `thesmiths`
- Need to find members of this group

### 2. Method Used
- Analyzed Windows Security Event Logs (Security.evtx)
- Looked for Event ID 4732 (member added to security-enabled local group)
- Mapped Security Identifiers (SIDs) to usernames using Event ID 4720 (user created)

### 3. Key Evidence

**Group Membership SIDs Found:**
- `S-1-5-21-2584721208-1353900670-1627748517-1003` → **thom**
- `S-1-5-21-2584721208-1353900670-1627748517-1004` → **jonny** 
- `S-1-5-21-2584721208-1353900670-1627748517-1005` → **colin**
- `S-1-5-21-2584721208-1353900670-1627748517-1006` → **philip**
- `S-1-5-21-2584721208-1353900670-1627748517-1007` → **ed**

**Event Details:**
- **Event IDs**: 4732 (member added to group)
- **Target Group**: `thesmiths`
- **Domain**: `DESKTOP-P5L8521`
- **Added by**: User `agent`

### 4. SID to Username Mapping Process

1. **Step 1**: Extracted MemberSid values from Event ID 4732 events related to `thesmiths` group
2. **Step 2**: Found corresponding usernames using Event ID 4720 (user creation events)
3. **Step 3**: Mapped each SID to its associated username
4. **Step 4**: Sorted alphabetically as requested

### 5. Event Log Evidence
```xml
<!-- Example of group membership event -->
<EventID>4732</EventID>
<Data Name="MemberSid">S-1-5-21-2584721208-1353900670-1627748517-1003</Data>
<Data Name="TargetUserName">thesmiths</Data>

<!-- Corresponding user creation event -->
<EventID>4720</EventID>
<Data Name="TargetUserName">thom</Data>
<Data Name="TargetSid">S-1-5-21-2584721208-1353900670-1627748517-1003</Data>
```

### 6. Verification
- All 5 members were successfully mapped from SID to username
- Names were sorted alphabetically as requested
- Cross-referenced with user creation events to ensure accuracy

### 7. Tools Used
- `evtx_dump` - Windows Event Log parser
- Custom Python script for SID-to-username mapping
- grep and text processing tools

## Final Answer Format
As requested: **colin, ed, jonny, philip, thom**
