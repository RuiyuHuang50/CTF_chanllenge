# Admin Access Web Challenge

## Challenge Description
I found this website, i need to get admin access to it. Can you help?
Website: https://nm01.bootupctf.net:8081/

## Analysis
The website has a login form with hardcoded credentials in HTML comments:
```html
<!-- Hardcoded credentials for testing: test / test -->
```

## Solution
1. Login with credentials found in HTML comment:
   - Username: test
   - Password: test
2. After login, notice the `user_level=user` cookie
3. Change cookie to `user_level=admin` to escalate privileges
4. Access `/home.php` with admin cookie to get the flag

## Flag
[REDACTED - Submit solution to competition organizers]
