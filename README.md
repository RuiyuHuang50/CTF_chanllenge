# CTF Challenge Collection 🏆

A comprehensive collection of Capture The Flag (CTF) challenges covering multiple cybersecurity domains including web exploitation, cryptography, forensics, binary analysis, and steganography.
<img width="772" height="259" alt="image" src="https://github.com/user-attachments/assets/586ec8a6-c762-4768-b9fc-75db37eb32dd" />

## 📁 Challenge Catalog

### 🌐 Web Exploitation Challenges

#### 1. **Admin Access Web** (`admin_access_web/`)
- **Type**: Cookie Manipulation
- **Target**: https://nm01.bootupctf.net:8081/
- **Vulnerability**: Privilege escalation via cookie modification
- **Solution**: Change `user_level=user` to `user_level=admin`
- **Flag**: [REDACTED - Challenge Solved]
- **Status**: ✅ SOLVED

#### 2. **Arrays JavaScript** (`arrays_javascript/`)
- **Type**: Client-side Logic / JavaScript Analysis
- **Target**: https://1-wm01.bootupctf.net/
- **Vulnerability**: Hardcoded password construction from array elements
- **Solution**: Password = `ends-vary-alike-broccoli` (array manipulation)
- **Flag**: [REDACTED - Challenge Solved]
- **Status**: ✅ SOLVED

#### 3. **Fastest Robot Web** (`fastest_robot_web/`)
- **Type**: ReDoS (Regular Expression Denial of Service)
- **Target**: https://cpp.bootupctf.net:8088/
- **Vulnerability**: Catastrophic backtracking in regex `(a+)+$`
- **Solution**: Exploit regex with pattern causing exponential time complexity
- **Flag**: [REDACTED - Challenge Solved]
- **Status**: ✅ SOLVED

#### 4. **Lower Numbers Web** (`lower_numbers_web/`)
- **Type**: JWT Token Manipulation / Integer Overflow
- **Vulnerability**: JWT token with numeric payload manipulation
- **Techniques**: Cookie analysis, JWT decoding, integer overflow exploitation
- **Status**: 🔄 IN PROGRESS

#### 5. **SSTI Web Exploitation** (`ssti_web_exploitation/`)
- **Type**: Server-Side Template Injection (Jinja2)
- **Target**: https://cpp.bootupctf.net:8095/
- **Vulnerability**: Template injection allowing file system access
- **Solution**: Jinja2 payload to read flag file
- **Flag**: [REDACTED - Challenge Solved]
- **Status**: ✅ SOLVED

#### 6. **Web Challenge 01** (`web_challenge_01/`)
- **Type**: Web Application Security
- **Analysis**: HTTP header analysis, response inspection
- **Status**: 🔍 ANALYZED

#### 7. **Web Directory Traversal** (`web_directory_traversal/`)
- **Type**: Path Traversal / Directory Traversal
- **Vulnerability**: Improper input validation allowing file system access
- **Status**: 📝 DOCUMENTED

### 🔐 Cryptography Challenges

#### 8. **Crypto Tunes** (`crypto_tunes/`)
- **Type**: Musical Cipher / Substitution Cipher
- **Key**: "Boys Don't Cry" song reference
- **Ciphertext**: "irpflfpqcbgbx"
- **Status**: 🔄 ATTEMPTED

#### 9. **Rolling My Own CTR Mode** (`Rolling my own CTR mode/`)
- **Type**: Custom Cryptographic Implementation
- **Vulnerability**: Flawed Counter (CTR) mode implementation
- **Files**: Custom encryption/decryption scripts
- **Status**: 📋 ANALYZED

### 🔍 Digital Forensics & Analysis

#### 10. **Back to the New House** (`Back_to_the_New_House/`)
- **Type**: Windows Event Log Forensics
- **Evidence**: Multiple EVTX files (Security, System, PowerShell, etc.)
- **Files**: 
  - Windows Event Logs (Application.evtx, Security.evtx, System.evtx)
  - Network capture (server.pcap)
  - System dumps (security_dump.xml, taskscheduler_dump.xml)
- **Status**: 🔄 IN PROGRESS

#### 11. **Unwanted Visitor 2** (`unwanted_visitor_2/`)
- **Type**: PowerShell Forensics / Log Analysis
- **Evidence**: Compressed log files containing potential backdoor evidence
- **Focus**: PowerShell script block logging analysis
- **Status**: 🔄 IN PROGRESS

#### 12. **Windows Event Logs Forensics** (`windows_event_logs_forensics/`)
- **Type**: Windows Security Event Analysis
- **Focus**: Incident response and threat hunting
- **Status**: 📋 AVAILABLE

#### 13. **The Echo** (`The_echo/`)
- **Type**: Network Protocol Analysis
- **Evidence**: PCAP file (the_echo_protocol_1.pcap)
- **Focus**: ICMP protocol analysis and hidden message extraction
- **Status**: 🔍 ANALYZED

#### 14. **Trail Trace** (`Trail_Trace/`)
- **Type**: Geospatial Forensics / GPS Analysis
- **Evidence**: 
  - GPS coordinates (gps_coordinates.txt)
  - KML mapping file (trail.kml)
  - Network capture (log.pcap)
- **Status**: 📊 DATA AVAILABLE

### 🔧 Binary Analysis & Reverse Engineering

#### 15. **Binary Analysis Intro04** (`binary_analysis_intro04/`)
- **Type**: Linux ELF Binary Analysis
- **Technique**: String extraction from compiled binary
- **Solution**: Cross-platform string analysis
- **Flag**: [REDACTED - Challenge Solved]
- **Status**: ✅ SOLVED

#### 16. **Hex Decode Challenge** (`hex_decode_challenge/`)
- **Type**: Hexadecimal Data Analysis / Multi-layer Encoding
- **Challenge**: Large hex array containing encoded data with syntax errors
- **Techniques**: Hex-to-text conversion, XOR analysis, compression detection
- **Key Finding**: Contains readable string `BasicALlYStrINgZ-1001`
- **Skills**: Python bytes manipulation, pattern recognition, data forensics
- **Status**: 🔍 ANALYZED

### 🖼️ Steganography & Visual Cryptography

#### 17. **Network Diagram Password** (`network_diagram_password/`)
- **Type**: Draw.io Steganography
- **File**: classified network.drawio.png
- **Vulnerability**: XML data embedded in PNG with visual redaction
- **Solution**: Extract hidden text elements from embedded XML
- **Flag**: [REDACTED - Challenge Solved]
- **Status**: ✅ SOLVED

#### 18. **Wrong QR** (`Wrong_QR/`)
- **Type**: QR Code Analysis / Image Steganography
- **Evidence**: Multiple QR code images (qr1.png, qr2.png, binary variants)
- **Techniques**: QR decoding, binary analysis, steganographic extraction
- **Status**: 🔍 EXTENSIVELY ANALYZED

### 🚀 Special Challenges

#### 19. **Starship Infiltration** (`starship_infiltration/`)
- **Type**: Multi-stage Challenge
- **Status**: 📁 AVAILABLE

## 📊 Challenge Statistics

| Category | Total | Solved | In Progress | Available |
|----------|-------|--------|-------------|-----------|
| **Web Exploitation** | 7 | 4 | 1 | 2 |
| **Cryptography** | 2 | 0 | 1 | 1 |
| **Digital Forensics** | 6 | 0 | 2 | 4 |
| **Binary Analysis** | 2 | 1 | 0 | 1 |
| **Steganography** | 2 | 1 | 0 | 1 |
| **Special** | 1 | 0 | 0 | 1 |
| **TOTAL** | **20** | **6** | **4** | **10** |

## 🏆 Confirmed Flags Found

[REDACTED - 6 flags successfully found during competition]

## 🛠️ Technical Skills Demonstrated

### Web Security
- Server-Side Template Injection (SSTI)
- JWT Token Manipulation
- Cookie-based Authentication Bypass
- Regular Expression Denial of Service (ReDoS)
- Client-side Logic Exploitation
- Directory Traversal

### Cryptography
- Substitution Ciphers
- Custom Encryption Analysis
- Counter Mode Cryptography

### Digital Forensics
- Windows Event Log Analysis (EVTX)
- PowerShell Script Block Logging
- Network Traffic Analysis (PCAP)
- GPS/Geospatial Data Analysis

### Binary Analysis
- Linux ELF Format Understanding
- String Extraction Techniques
- Cross-platform Binary Analysis
- Hexadecimal Data Analysis
- Multi-layer Encoding Detection
- Python Bytes Manipulation

### Steganography
- Image-based Hidden Data
- XML Embedded in Binary Formats
- QR Code Analysis
- Visual Cryptography

## 🗂️ Workspace Organization

```
CTF_chanllenge/
├── challenges/                    # 🎯 All challenge files (20 challenges)
│   ├── admin_access_web/         # ✅ Cookie manipulation
│   ├── arrays_javascript/        # ✅ JS array password
│   ├── Back_to_the_New_House/    # 🔄 Windows forensics
│   ├── binary_analysis_intro04/  # ✅ ELF binary analysis
│   ├── crypto_tunes/             # 🔄 Musical cipher
│   ├── fastest_robot_web/        # ✅ ReDoS attack
│   ├── hex_decode_challenge/     # 🔍 Hex data analysis
│   ├── lower_numbers_web/        # 🔄 JWT manipulation
│   ├── network_diagram_password/ # ✅ Draw.io steganography
│   ├── Rolling my own CTR mode/  # 📋 Custom crypto
│   ├── ssti_web_exploitation/    # ✅ Template injection
│   ├── The_echo/                 # 🔍 ICMP analysis
│   ├── Trail_Trace/              # 📊 GPS forensics
│   ├── unwanted_visitor_2/       # 🔄 PowerShell forensics
│   ├── web_challenge_01/         # 🔍 Web app security
│   ├── web_directory_traversal/  # 📝 Path traversal
│   ├── windows_event_logs_forensics/ # 📋 Event log analysis
│   ├── Wrong_QR/                 # 🔍 QR steganography
│   └── starship_infiltration/    # 📁 Multi-stage challenge
├── solved_challenges/            # 🏆 Successfully completed challenges
├── redacted.pdf                  # 📄 Challenge documentation
├── screenshot.png                # 🖼️ Reference image
└── README.md                     # 📖 This comprehensive guide
```

## 🎯 Success Rate: 30% (6/20 challenges solved)

This CTF collection demonstrates proficiency across multiple cybersecurity domains with a focus on practical exploitation techniques and forensic analysis methodologies.

## Usage
- Add new challenges in the `challenges/` folder.
- Place your solution scripts in the `scripts/` folder.
- See `.github/copilot-instructions.md` for workflow and contribution guidelines.
