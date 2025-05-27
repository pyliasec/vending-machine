import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform # 시스템의 정보를 가져오는 신기한 친구
import os

system_name = platform.system()
if system_name == "Windows":
    font_path = "C:/Windows/Fonts/malgun.ttf"
elif system_name == "Darwin":
    font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
else:
    font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

if not os.path.exists(font_path):
    raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {font_path}")

font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

def load_stats(file_path="data.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def plot_bar(data_dict, title, xlabel, ylabel):
    items = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure(figsize=(10,6))
    plt.bar(items, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_pie(data_dict, title):
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())

    plt.figure(figsize=(8,8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(title)
    plt.axis("equal")
    plt.show()

def plot_sales_over_time(sales_by_datetime):
    dates = sorted(sales_by_datetime.keys())
    sales = [sales_by_datetime[date]["sales"] for date in dates]
    revenue = [sales_by_datetime[date]["revenue"] for date in dates]

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel("Date")
    ax1.set_ylabel("판매량", color="blue")
    ax1.plot(dates, sales, marker="o", color="blue", label="판매량")
    ax1.tick_params(axis='y', labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("매출액", color="red")
    ax2.plot(dates, revenue, marker="s", color="red", label="매출액")
    ax2.tick_params(axis='y', labelcolor="red")

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    plt.title("Sales and Revenue Over Time")
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()


def main():
    stats = load_stats()

    print(f"총 매출: {stats['total_revenue']}")
    print(f"총 판매량: {stats['total_sales']}")

    plot_bar(stats["sales_by_item"], "상품별 판매 개수", "상품명", "판매 수량")
    plot_bar(stats["revenue_by_item"], "상품별 매출", "상품명", "매출액")
    plot_pie(stats["sales_by_manufacturer"], "제조사별 판매 비율")
    plot_pie(stats["sales_by_payment_method"], "결제 수단별 판매 비율")
    plot_sales_over_time(stats["sales_by_datetime"])

if __name__ == "__main__":
    main()
