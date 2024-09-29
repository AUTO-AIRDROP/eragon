import requests
from datetime import datetime
import time
import pytz
from colorama import Fore, Style, init

url = 'https://api-mainnet.eragon.gg'

def afterClaim(token):
    api_url = f"{url}/users/claimEra3MineSession"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {token}",
        "if-none-match": "W/\"2bf-FeeYcHBnwqm634PX5ZWvvlvcoIY\"",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://eragon.gg/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    response = requests.delete(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Gagal, status kode: {response.status_code}")
        return None

def claim_era3_mine_session(token, index):
    api_url = f"{url}/users/claimEra3MineSession"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {token}",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://eragon.gg/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    data = {"claimImmediate": True}  
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 201:
        response_data = response.json()
        era3 = response_data['data']['era3']

        session_rate = response_data['data']['sessionEra3Rate']  # Pastikan ini adalah float
        
        if isinstance(session_rate, str):
            session_rate = float(session_rate.replace(',', '.'))  # Ganti koma dengan titik jika perlu
        elif isinstance(session_rate, float):
            session_rate = session_rate  # Sudah dalam bentuk float
        
        session_rate = f"{session_rate:.10f}"

        # Mengambil waktu dari respons
        time_str = response_data['time']
        dt = datetime.fromisoformat(time_str[:-1])  # Menghilangkan 'Z'
        
        # Mengonversi ke WIB
        utc_time = pytz.utc.localize(dt)  # Mengatur zona waktu ke UTC
        wib_time = utc_time.astimezone(pytz.timezone('Asia/Jakarta'))  # Mengonversi ke WIB
        
        formatted_time = wib_time.strftime("%d-%m-%Y %H:%M")  # Format waktu
        
        # Menampilkan output klaim
        print(f"[{Fore.WHITE}{formatted_time}{Style.RESET_ALL}] User ke-{index} +{Fore.GREEN}{session_rate}{Style.RESET_ALL} Total: {Fore.YELLOW}{era3}{Style.RESET_ALL}")
    else:
        print(f"Gagal klaim coin, status kode: {response.status_code}")
        print(response.text)
        return None, 0  # Mengembalikan None dan 0 jika gagal

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        print(f"Waktu tersisa: {timer}", end='\r')
        time.sleep(1)
        seconds -= 1

def main():
    # Membaca token dari file token.txt
    with open("token.txt", "r") as file:
        tokens = [line.strip() for line in file.readlines()]

    while True:
        for index, token in enumerate(tokens, start=1):
            claim_era3_mine_session(token, index)
        countdown_timer(1 * 5)  # Menghitung mundur selama 10 menit

if __name__ == "__main__":
    main()
