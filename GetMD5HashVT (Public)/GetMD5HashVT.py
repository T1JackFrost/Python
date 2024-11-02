import requests
import pandas as pd

APIkey = "Your-VirusTotal-account-API-key"

def process_csv(input_file, output_file): 
    df = pd.read_csv(input_file)
    md5_hashes = []
    if 'Indicator Value' in df.columns and 'Type' in df.columns:
        for id in df['Indicator Value']:

            #Call API để lấy data
            api_url = f'https://www.virustotal.com/api/v3/files/{id}'
            #Dùng key API được cấp khi creat account trên Virustotal gán vào headers
            headers = {"accept": "application/json", 
                    "x-apikey": APIkey
            }
            response = requests.get(api_url, headers=headers)

            #Kiểm tra nếu có kết quả => return về MD5 Hash, trích xuất data và biến đổi danh sách
            if response.status_code == 200:
                json_data = response.json()
                # Kiểm tra key MD5 có tồn tại trong object attributes không:
                if 'md5' in json_data["data"]["attributes"]:
                    md5 = json_data["data"]["attributes"]["md5"]
                    md5_hashes.append(md5)
                else:
                    md5_hashes.append('N/A')
            #Không có kết quả => return về N/A
            else: 
                md5_hashes.append('N/A')

        #Add list kết quả MD5 vào cột mới tên MD5 Hash
        df['MD5 Hash'] = md5_hashes
        #Ghi data vào file mới
        df.to_csv(output_file, index=False)

input_file = r'C:\Users\YourName\Downloads\IOCHASH_29_09_2024.csv'
output_file = r'C:\Users\YourName\Downloads\newIOCs.csv'

process_csv(input_file, output_file)