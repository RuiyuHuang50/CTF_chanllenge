#!/usr/bin/env python3
"""
JavaScript Arrays CTF Challenge Solver
Deobfuscates the JavaScript to reveal the flag
"""

def deobfuscate_js():
    print("🔍 JavaScript Arrays Challenge Solver")
    print("=" * 50)
    
    # First, let's calculate the password
    words = ["vary", "ends", "broccoli", "alike"]
    password = f"{words[1]}-{words[0]}-{words[3]}-{words[2]}"
    
    print(f"📝 Login Credentials:")
    print(f"   Username: admin")
    print(f"   Password: {password}")
    print()
    
    # Now let's deobfuscate the JavaScript flag
    print("🔓 Deobfuscating JavaScript flag...")
    print("-" * 30)
    
    # Part 1: (function(){var P=Array.prototype.slice.call(arguments),S=P.shift();return P.reverse().map(function(B,c){return String.fromCharCode(B-S-29-c)}).join('')})(6,155,145,116,150,140,72,97,141,134,144,105)
    def part1():
        args = [6, 155, 145, 116, 150, 140, 72, 97, 141, 134, 144, 105]
        S = args[0]  # shift() removes first element (6)
        P = args[1:]  # remaining elements
        P.reverse()  # reverse the array
        
        result = ""
        for c, B in enumerate(P):
            char_code = B - S - 29 - c
            result += chr(char_code)
        return result
    
    # Part 2: (10).toString(36).toLowerCase().split('').map(function(f){return String.fromCharCode(f.charCodeAt()+(-13))}).join('')
    def part2():
        base36 = str(10)  # "10" in base 10 is "a" in base 36
        base36_char = chr(ord('a') + 10 - 10)  # Convert 10 to base 36 = 'a'
        result = ""
        for char in 'a':  # (10).toString(36) = 'a'
            char_code = ord(char) + (-13)
            result += chr(char_code)
        return result
    
    # Part 3: (35).toString(36).toLowerCase().split('').map(function(q){return String.fromCharCode(q.charCodeAt()+(-39))}).join('')
    def part3():
        # 35 in base 36 is 'z'
        result = ""
        for char in 'z':
            char_code = ord(char) + (-39)
            result += chr(char_code)
        return result
    
    # Part 4: (function(){var U=Array.prototype.slice.call(arguments),W=U.shift();return U.reverse().map(function(T,B){return String.fromCharCode(T-W-49-B)}).join('')})(54,214,211,218,182,174,204,208)
    def part4():
        args = [54, 214, 211, 218, 182, 174, 204, 208]
        W = args[0]  # shift() removes first element (54)
        U = args[1:]  # remaining elements
        U.reverse()  # reverse the array
        
        result = ""
        for B, T in enumerate(U):
            char_code = T - W - 49 - B
            result += chr(char_code)
        return result
    
    # Part 5: (30).toString(36).toLowerCase().split('').map(function(e){return String.fromCharCode(e.charCodeAt()+(-39))}).join('')
    def part5():
        # 30 in base 36 is 'u'
        result = ""
        for char in 'u':
            char_code = ord(char) + (-39)
            result += chr(char_code)
        return result
    
    # Part 6: (1).toString(36).toLowerCase()
    def part6():
        # 1 in base 36 is '1'
        return '1'
    
    # Part 7: (function(){var H=Array.prototype.slice.call(arguments),k=H.shift();return H.reverse().map(function(I,N){return String.fromCharCode(I-k-14-N)}).join('')})(29,92)
    def part7():
        args = [29, 92]
        k = args[0]  # shift() removes first element (29)
        H = args[1:]  # remaining elements [92]
        H.reverse()  # reverse the array [92]
        
        result = ""
        for N, I in enumerate(H):
            char_code = I - k - 14 - N
            result += chr(char_code)
        return result
    
    # Part 8: (324).toString(36).toLowerCase()
    def part8():
        # 324 in base 36 is '90'
        return format(324, 'x')  # hex representation
    
    # Let's calculate each part
    try:
        p1 = part1()
        print(f"Part 1: '{p1}'")
        
        # Recalculate part 2 properly
        # (10).toString(36) in JavaScript gives 'a'
        p2_char = 'a'
        p2 = chr(ord(p2_char) - 13)  # 'a' - 13 = 'T'
        print(f"Part 2: '{p2}'")
        
        # Recalculate part 3 properly  
        # (35).toString(36) in JavaScript gives 'z'
        p3_char = 'z'
        p3 = chr(ord(p3_char) - 39)  # 'z' - 39 = 'H'
        print(f"Part 3: '{p3}'")
        
        p4 = part4()
        print(f"Part 4: '{p4}'")
        
        # Recalculate part 5 properly
        # (30).toString(36) in JavaScript gives 'u'  
        p5_char = 'u'
        p5 = chr(ord(p5_char) - 39)  # 'u' - 39 = 'L'
        print(f"Part 5: '{p5}'")
        
        p6 = '1'  # (1).toString(36) = '1'
        print(f"Part 6: '{p6}'")
        
        p7 = part7()
        print(f"Part 7: '{p7}'")
        
        # (324).toString(36) in JavaScript
        p8 = ''
        n = 324
        if n == 0:
            p8 = '0'
        else:
            digits = '0123456789abcdefghijklmnopqrstuvwxyz'
            result = ''
            while n:
                result = digits[n % 36] + result
                n //= 36
            p8 = result
        print(f"Part 8: '{p8}'")
        
        # Combine all parts
        flag = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8
        print(f"\n🚩 DEOBFUSCATED FLAG: {flag}")
        
        return flag, password
        
    except Exception as e:
        print(f"❌ Error deobfuscating: {e}")
        return None, password

def main():
    flag, password = deobfuscate_js()
    
    print(f"\n📋 Summary:")
    print(f"   Login with: admin / {password}")
    if flag:
        print(f"   Flag: {flag}")
    else:
        print(f"   Flag: [Manual login required to see obfuscated result]")

if __name__ == "__main__":
    main()
