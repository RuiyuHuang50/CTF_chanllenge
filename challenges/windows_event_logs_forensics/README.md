# Windows Event Logs Forensics

**Challenge Type:** Forensics
**Date Solved:** 2025-09-12
**Difficulty:** Medium

## Challenge Description

Our newly created server was compromised. We suspect that the attacker had some stolen credentials lying around and was able to connect to the machine using a well known protocol. We have gathered some Windows Event logs from the server from around the time we suspect the attacker first got access.

Can you find the hostname of the machine the attacker used to login?

Flag format: [REDACTED] (all upper case)

Our forensics personnel suddenly left on holiday, but mumbled something about 'Security' on the way out of the door.

## Key Information

- **Hint**: "Security" - refers to Security.evtx log file
- **Attack method**: Stolen credentials + well-known protocol (likely RDP/SMB)
- **Goal**: Find attacker's machine hostname
- **Flag format**: [REDACTED] in uppercase

## Solution Process

1. **Log Analysis**: Focus on Security.evtx as hinted by "Security" comment
2. **Event Types**: Look for Windows logon events (Event ID 4624, 4625, 4648)
3. **Hostname Extraction**: Find WorkstationName field in logon events
4. **Pattern Analysis**: Identify non-system hostnames that appear in login contexts

## Technical Approach

### Windows Event IDs of Interest:

- **4624**: Successful logon
- **4625**: Failed logon attempt
- **4648**: Logon using explicit credentials
- **4776**: Domain controller credential validation

### Key Fields to Examine:

- `WorkstationName`: Name of the machine connecting
- `TargetDomainName`: Domain being accessed
- `LogonType`: Type of logon (2=Interactive, 3=Network, 10=RemoteInteractive)
- `SourceNetworkAddress`: IP address of connecting machine

## Files

- `solution/solve.py` - Main automated solution script
- `solution/advanced_analysis.py` - Advanced pattern analysis script
- `files/logs/` - Windows Event Log files (.evtx format)
  - `Windows Logs/Security.evtx` - Primary log for analysis
  - `Windows Logs/System.evtx` - System events
  - `Application and Services Logs/` - Additional service logs

## Flag

```
[REDACTED]
```

**Solution Found**: Through string extraction and frequency analysis, "NOTA" was identified as the most frequently appearing non-system hostname in Security.evtx (7 occurrences), indicating it's likely the attacker's machine hostname.

## Tools Used

- `strings` command for text extraction from binary EVTX files
- `python-evtx` library for proper EVTX parsing (if available)
- Custom Python scripts for pattern analysis
- Regular expressions for hostname identification

## Analysis Notes

Windows EVTX files are binary format containing XML event data. Common approaches:

1. **Native parsing**: Use libraries like python-evtx or libevtx
2. **String extraction**: Use `strings` command as fallback
3. **Windows tools**: Event Viewer, wevtutil (if on Windows)

The attacker likely used:

- **RDP (Remote Desktop Protocol)**: LogonType 10
- **SMB/Network logon**: LogonType 3
- **Stolen credentials**: Valid username/password

## Lessons Learned

- Windows Event Logs are crucial for forensic analysis
- Event ID 4624 contains valuable logon information
- WorkstationName field reveals source machine identity
- EVTX parsing requires specialized tools or string extraction
- Frequency analysis helps identify anomalous hostnames

## Alternative Methods

- Use Windows Event Viewer if available
- PowerShell Get-WinEvent cmdlet for parsing
- Log analysis tools like Splunk or ELK stack
- Timeline analysis to correlate multiple events
