# Arrays in JavaScript Challenge

## Challenge Description
Access the site at https://1-wm01.bootupctf.net/ and find a way to get the flag.

## Analysis

### Login Requirements
- Username: `admin`
- Password: Constructed from array elements
- Array: `["vary", "ends", "broccoli", "alike"]`
- Password format: `words[1] + "-" + words[0] + "-" + words[3] + "-" + words[2]`

### Password Construction
- words[0] = "vary"
- words[1] = "ends" 
- words[2] = "broccoli"
- words[3] = "alike"
- Password = "ends-vary-alike-broccoli"

### Flag Location
The flag is hidden in obfuscated JavaScript that executes when login is successful.

## Solution
1. Login with username: `admin`
2. Login with password: `ends-vary-alike-broccoli`
3. Deobfuscate the JavaScript to reveal the flag

## Flag
[REDACTED - Submit solution to competition organizers]

## Complete Solution
1. Analyze the JavaScript to find login credentials:
   - Username: `admin`
   - Password: `ends-vary-alike-broccoli`
2. The password is constructed from array elements: `words[1] + "-" + words[0] + "-" + words[3] + "-" + words[2]`
3. Upon successful login, obfuscated JavaScript executes and reveals the flag
4. Deobfuscating the JavaScript yields: `Flag: clIenTSidELogiN1190`
