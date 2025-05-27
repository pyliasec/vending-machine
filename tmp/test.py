import hashlib

# pwd = input("비밀번호 입력: ")
# print("입력한 문자들 아스키 코드:")
# for c in pwd:
#     print(c, ord(c))

# ================

# password = "admin1234"
# hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
# print(hashed)

# ================

print(hashlib.sha256("admin1234".encode('utf-8')).hexdigest())
# ac9689e2272427085e35b9d3e3e8bed88cb3434828b43b86fc0596cad4c6e270

# ================

def check_admin_password():
    saved_hash = "ac9689e2272427085e35b9d3e3e8bed88cb3434828b43b86fc0596cad4c6e270"
    pw = input("관리자 비밀번호를 입력하세요: ").strip()
    print(f"입력된 문자열: [{pw}]")
    print(f"문자열 길이: {len(pw)}")
    input_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    print(f"입력한 비밀번호 해시: {input_hash}")
    print(f"저장된 해시: {saved_hash}")
    if input_hash == saved_hash:
        print("비밀번호 일치")
        return True
    else:
        print("비밀번호 틀림")
        return False

check_admin_password()