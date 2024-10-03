import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import json
from datetime import datetime
from datetime import datetime, timedelta
from docx import Document

input_file_path = r'C:\Users\YourUsername\Downloads\Reference set template.docx'

# Đọc file Word
doc = Document(input_file_path)
# Duyệt qua tất cả các bảng trong tài liệu
table_index = 0
table = doc.tables[table_index]

# Duyệt qua từng hàng trong bảng

for row in table.rows[1:]:
    for cell in row.cells:
        cell_value = row.cells[0].text
    username = 'yourusename'
    password = 'yourpassword'

    while True:
        name = cell_value
        
        # Mã hóa tên hai lần để tạo thành mã hóa kép (Do API yêu cầu mã hoá kép)
        encoded_name = urllib.parse.quote(urllib.parse.quote(name))

        # URL cho API, sử dụng f-string để chèn biến `name` vào
        api_url = f'https://x.x.x.x/api/reference_data/sets/{name}?fields=data(value%2C%20first_seen)'

        # Gửi yêu cầu HTTP với xác thực cơ bản và bỏ qua SSL verification
        response = requests.get(api_url, auth=HTTPBasicAuth(username, password), verify=False)

        # Kiểm tra mã trạng thái phản hồi
        if response.status_code == 200:
            json_data = response.json()

            # Trích xuất dữ liệu và biến đổi thành danh sách
            result = []
            for item in json_data["data"]:
                value = item["value"]
                timestamp = item["first_seen"] / 1000  # Chuyển miligiây thành giây
                first_seen_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                result.append({"value": value, "first_seen": first_seen_time})

            current_time = datetime.now()
        # Trích xuất dữ liệu và biến đổi thành danh sách, và lưu vào tệp
            with open(r'D:\iocs.txt', "w") as file:
                count = 0
                for item in json_data["data"]:
                    value = item["value"]
                    timestamp = item["first_seen"] / 1000  # Chuyển miligiây thành giây
                    first_seen_time = datetime.fromtimestamp(timestamp)

                    # Tính khoảng thời gian giữa thời điểm hiện tại và first_seen_time
                    time_difference = current_time - first_seen_time
                        # So sánh với 30 ngày
                    if time_difference <= timedelta(days=30):
                        result = f"Value: {value}, First Seen: {first_seen_time.strftime('%Y-%m-%d %H:%M:%S')}"
                        file.write(result + "\n")
                        count += 1
            print(f"Số kết quả đã được lưu đối với reference set '{name}': {count}") 
            row.cells[1].text = str(count) # Gán giá trị của count vào ô thứ hai của hàng hiện tại
            break  # Thoát khỏi vòng lặp khi nhận được phản hồi thành công
        else:
            # In mã lỗi nếu request không thành công và yêu cầu nhập lại
            print(f"Lỗi {response.status_code}: Không tìm thấy reference set '{name}'. Vui lòng thử lại.")
            break
        
              
# Lưu tài liệu sau khi thực hiện các thao tác
output_file_path = r'C:\Users\YourUsername\Downloads\Refset Count.docx'  # Thay đổi đường dẫn ở đây
doc.save(output_file_path)
