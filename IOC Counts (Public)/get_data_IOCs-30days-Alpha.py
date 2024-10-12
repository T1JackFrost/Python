import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import json
from datetime import datetime
from datetime import datetime, timedelta
import pandas as pd

# information
username = 'yourusename'
password = 'yourpassword'

all_data = [] #giữ lại danh sách để không bị ghi đè sau mỗi lần lặp

while True:
    # Yêu cầu người dùng nhập tên reference set
    name = input("Nhập tên reference set (Hoặc nhập c để thoát): ").strip()

    if name.lower() == 'c':
        print("Thoát chương trình.")
        break
        
    # Mã hóa tên hai lần để tạo thành mã hóa kép (API yêu cầu mã hoá kép)
    encoded_name = urllib.parse.quote(urllib.parse.quote(name))

    # URL cho API, sử dụng f-string để chèn biến `name` vào
    api_url = f'https://x.x.x.x/api/reference_data/sets/{encoded_name}?fields=data(value%2C%20first_seen)'

    # Gửi yêu cầu HTTP với xác thực cơ bản và bỏ qua SSL verification
    response = requests.get(api_url, auth=HTTPBasicAuth(username, password), verify=False)

    # Kiểm tra mã trạng thái phản hồi
    if response.status_code == 200:
        json_data = response.json()

        # Trích xuất dữ liệu và biến đổi thành danh sách
        result = []
        count = 0
        current_time = datetime.now()
        for item in json_data["data"]:
            first_seen_time = datetime.fromtimestamp(item["first_seen"] / 1000) # Chuyển miligiây thành giây
            time_difference = current_time - first_seen_time
            if time_difference <= timedelta(days=30):
                value = item["value"]
                result.append(f"Value: {value}, First Seen: {first_seen_time.strftime('%Y-%m-%d %H:%M:%S')}")
                count+=1
                all_data.append({"Reference Set Name": name, "Value": value, "First Seen": first_seen_time.strftime('%Y-%m-%d %H:%M:%S')})

        # Trích xuất dữ liệu và biến đổi thành danh sách, và lưu vào tệp
        if result:
            output_file = r'D:\iocs.txt'
            with open(output_file, "w", encoding = "utf-8") as file:
                for line in result:
                    file.write(line + "\n")
        print(f"Số kết quả đã được lưu đối với reference set '{name}' trong vòng 30 ngày: {count}")
        break  # Thoát khỏi vòng lặp khi nhận được phản hồi thành công
    else:
        # In mã lỗi nếu request không thành công và yêu cầu nhập lại
        print(f"Lỗi {response.status_code}: Không tìm thấy reference set '{name}'. Vui lòng thử lại.")
        break
        
output_file_xlxs = fr"C:\Users\YourName\Downloads\IOCs-{name}-From-The-Last-30days.xlsx"
#Ghi data vào file xlsx
if all_data:
    combined_df = pd.DataFrame(all_data)
    combined_df.to_excel(output_file_xlxs, index=False, engine = "openpyxl")

print(f"Tất cả dữ liệu đã được lưu vào file: {output_file_xlxs}")