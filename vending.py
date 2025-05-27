import json
import time
import random
import hashlib
import sys
import select
from datetime import datetime

def load_menu():
    with open("menu.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["menu"]

def save_stats(stats):
    with open("data.json", "w", encoding = "utf-8") as f:
        json.dump(stats, f, ensure_ascii = False, indent = 4)

def save_menu(menu):
    with open("menu.json", "w", encoding = "utf-8") as f:
        json.dump({"menu" : menu}, f, ensure_ascii = False, indent = 4)

def load_stats():
    try:
        with open("data.json", "r", encoding = "utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {
            "total_revenue" : 0,
            "total_sales" : 0,
            "sales_by_item" : {},
            "revenue_by_item" : {},
            "sales_by_manufacturer" : {},
            "revenue_by_manufacturer" : {},
            "sales_by_payment_method" : {},
            "sales_by_datetime" : {}
        }

def show_menu(menu):
    print("자판기 메뉴")
    for item in menu:
        print(f"{item['Id']}. {item['Name']} : {item['Price']}원")

def check_admin_password(input_pw):
    saved_hash = "ac9689e2272427085e35b9d3e3e8bed88cb3434828b43b86fc0596cad4c6e270"
    input_hash = hashlib.sha256(input_pw.encode('utf-8')).hexdigest()
    return input_hash == saved_hash

def admin(menu):
    print("관리자 모드 진입")
    while True:
        print("\n1. 메뉴 출력 2. 메뉴 수정 3. 종료")
        choice = input("선택: ").strip()
        if choice == "1":
            show_menu(menu)
        elif choice == "2":
            show_menu(menu)
            try:
                item_id = int(input("수정할 메뉴 번호 입력: ").strip())
                item = next((i for i in menu if i["Id"] == item_id), None)
                if item:
                    new_price = int(input(f"{item['Name']}의 새 가격 입력: ").strip())
                    item["Price"] = new_price
                    save_menu(menu)
                    print(f"{item['Name']} 가격이 {new_price}원으로 변경되었습니다.")
                else:
                    print("해당 번호의 메뉴가 없습니다.")
            except ValueError:
                print("유효한 숫자를 입력하세요.")
        elif choice == "3":
            print("관리자 모드 종료")
            break
        else:
            print("잘못된 선택입니다.")

def cash(required_price):
    valid = [100, 500, 1000, 5000, 10000]
    total_cash = 0
    print("현금 결제를 선택하셨습니다.")
    print(f"사용 가능한 금액: {', '.join(str(i) + '원' for i in valid)}")
    print("※ 50,000원권은 사용할 수 없습니다. 종료하려면 0원을 입력하세요.")

    while total_cash < required_price:
        try:
            user_input = input(f"금액을 투입해주세요 (필요 금액: {required_price - total_cash}원): ").strip()
            user_cash = int(user_input)
            if user_cash == 0:
                break
            elif user_cash < 100:
                print("100원 미만 금액은 투입할 수 없습니다.\n")
            elif user_cash in valid:
                total_cash += user_cash
                print(f"{user_cash:,}원 투입됨. 현재까지 총 {total_cash:,}원.\n")
                if total_cash >= required_price:
                    print("필요 금액 이상 투입 완료.")
                    break
            elif user_cash == 50000:
                print("50,000원권은 사용할 수 없습니다.\n")
            else:
                print("유효하지 않은 금액입니다. 다시 시도해주세요.\n")
        except ValueError:
            print("숫자만 입력해주세요.\n")

    print(f"총 투입 금액: {total_cash:,}원")
    return total_cash

def input_with_timeout(prompt, timeout = 10):
    print(prompt, end = '', flush = True)
    start_time = time.time()
    last_remain = timeout + 1
    
    while True:
        elapsed = time.time() - start_time
        remain = int(timeout - elapsed)

        if elapsed >= timeout:
            print('\r' + ' ' * 100 + '\r', end = '', flush = True)
            print()
            return None
        
        if remain != last_remain and remain >= 0:
            print(f'\r{prompt} ({remain}초)', end = '', flush = True)
            last_remain = remain

        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            line = sys.stdin.readline()
            print('\r' + ' ' * 100 + '\r', end = '', flush = True)
            print()
            return line.strip()
        
def process_payment(payment_type):
    print(f"{payment_type} 결제를 선택하셨습니다.")
    entered = input_with_timeout(f"{payment_type} 결제를 진행하려면 엔터를 눌러주세요:", 10)
    if entered is None:
        print("입력 시간 초과. 처음으로 돌아갑니다.\n")
        return False
    
    print("\n결제 처리 중입니다...")
    for _ in range(3):
        print(".", end = '', flush = True)
        time.sleep(1)

    if random.random() < 0.9:
        print(f"\n{payment_type} 결제가 성공적으로 완료되었습니다.\n")
        return True
    else:
        print(f"\n결제에 실패했습니다. 다시 시도해주세요.\n")
        return False
    
def update_stats(stats, item, payment_method):
    price = item["Price"]
    manufacturer = item.get("Manufacturer", "알수없음")
    item_name = item ["Name"]

    # 총 매출 및 판매량
    stats["total_revenue"] = stats.get("total_revenue", 0) + price
    stats["total_sales"] = stats.get("total_sales", 0) + 1

    # 아이템별 판매량/매출
    stats["sales_by_item"][item_name] = stats["sales_by_item"].get(item_name, 0) + 1
    stats["revenue_by_item"][item_name] = stats["revenue_by_item"].get(item_name, 0) + price

    # 제조사별 판매량/매출
    stats["sales_by_manufacturer"][manufacturer] = stats["sales_by_manufacturer"].get(manufacturer, 0) + 1
    stats["revenue_by_manufacturer"][manufacturer] = stats["revenue_by_manufacturer"].get(manufacturer, 0) + price
    
    # 결제 수단별 판매량
    stats["sales_by_payment_method"][payment_method] = stats["sales_by_payment_method"].get(payment_method, 0) + 1

    # 날짜별 판매량/매출 (YYYY-MM-DD, HH)
    now = datetime.now()
    date_key = now.strftime("%Y-%m-%d")
    hour_key = now.strftime("%H")

    if date_key not in stats["sales_by_datetime"]:
        stats["sales_by_datetime"][date_key] = {"sales": 0, "revenue": 0, "hours": {}}
    stats["sales_by_datetime"][date_key]["sales"] += 1
    stats["sales_by_datetime"][date_key]["revenue"] += price

    if hour_key not in stats["sales_by_datetime"][date_key]["hours"]:
        stats["sales_by_datetime"][date_key]["hours"][hour_key] = {"sales": 0, "revenue": 0}
    stats["sales_by_datetime"][date_key]["hours"][hour_key]["sales"] += 1
    stats["sales_by_datetime"][date_key]["hours"][hour_key]["revenue"] += price

def user(menu):
    stats = load_stats()
    show_menu(menu)

    while True:
        choice = input("음료 번호를 선택하세요 (종료: 0): ").strip()

        if check_admin_password(choice):
            print("관리자 비밀번호 확인됨. 관리자 모드 진입")
            admin(menu)
            show_menu(menu)
            continue

        if choice == "0":
            print("사용자 모드 종료")
            break

        try:
            choice_num = int(choice)
            item = next((item for item in menu if item["Id"] == choice_num), None)
            
            if item:
                print(f"{item['Name']}을(를) 선택하셨습니다. 가격은 {item['Price']}원 입니다.")
                print("결제 방법을 선택하세요.\n1. 현금 2. 카드 3. 비접촉 결제 0. 종료")
                payment = input().strip()
                
                if payment == "1":
                    cash_amount = cash(item["Price"])
                    if cash_amount >= item["Price"]:
                        print(f"잔돈 {cash_amount - item['Price']}원 반환. 음료가 나왔습니다.")
                        update_stats(stats, item, "cash")
                        save_stats(stats)
                        exit()
                    else:
                        print("금액이 부족합니다. 결제 실패.")
                elif payment == "2":
                    if process_payment("카드"):
                        print("음료가 나왔습니다.")
                        update_stats(stats, item, "card")
                        save_stats(stats)
                        exit()
                elif payment == "3":
                    if process_payment("비접촉 결제"):
                        print("음료가 나왔습니다.")
                        update_stats(stats, item, "contactless")
                        save_stats(stats)
                        exit()
                elif payment == "0":
                    print("사용자 모드 종료")
                    break
                else:
                    print("잘못된 결제 수단입니다.")
            else:
                print("해당 번호의 메뉴가 없습니다.")
        except ValueError:
            print("유효한 숫자를 입력하세요.")

def main():
    menu = load_menu()
    print("자판기 프로그램 시작")
    user(menu)
    print("안녕히가세요.")

if __name__ == "__main__":
    main()
