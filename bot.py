import datetime  # 날짜 관련 기능
import pytz  # 시간대 설정을 위한 라이브러리
import random  # 랜덤값 생성
import requests  # Telegram API에 요청을 보내기 위한 라이브러리
import time  # 시간 지연을 위해 사용
import json  # JSON 데이터 처리
import threading  # 별도 스레드에서 메시지 전송
from flask import Flask  # Koyeb 실행을 위해 Flask 사용

app = Flask(__name__)  # Flask 앱 생성

# 한국 시간(KST) 기준으로 날짜 가져오기
def get_kst_date():
    tz = pytz.timezone('Asia/Seoul')
    kst_time = datetime.datetime.now(tz)
    return kst_time.strftime('%B %d, %Y')  # 'March 07, 2025' 형식

# 봇의 API 토큰 및 채널 설정
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'  # 여기에 실제 텔레그램 봇 토큰 입력
channel_id = '@crademaster_ch'  # 채널 ID

# 이메일 랜덤 생성 함수
def generate_random_email():
    prefix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=2))  # 2글자 랜덤 생성
    domain = random.choice(['com', 'net', 'co.kr'])  # 도메인 랜덤 선택
    return f"{prefix}*****@*****.{domain}"

# 첫 번째 메시지 생성 함수 (고정된 레퍼럴)
def generate_message_1():
    amount = random.choices(
        [random.randint(100, 1000), random.randint(1100, 10000), random.randint(10100, 20000), random.randint(20100, 40000), random.randint(40100, 50000)],
        [0.5, 0.4, 0.08, 0.015, 0.005]
    )[0]
    email = generate_random_email()
    referral_email = "Event code"
    event_referral = "Event Referral Experience USDT Reward : 250 USDT"
    current_date = get_kst_date()
    return f"✔️{current_date}\nSgin : {email}\nReferral : {referral_email}\n💰First Deposit : {amount:,} USDT💰\n💰{event_referral}💰\n🎉🎉🎉Congratulations on Joining CradeMaster!🎉🎉🎉"

# 두 번째 메시지 생성 함수 (랜덤 레퍼럴 이메일)
def generate_message_2():
    amount = random.choices(
        [random.randint(100, 1000), random.randint(1100, 10000), random.randint(10100, 20000), random.randint(20100, 40000), random.randint(40100, 50000)],
        [0.5, 0.4, 0.08, 0.015, 0.005]
    )[0]
    email = generate_random_email()
    referral_email = generate_random_email()
    current_date = get_kst_date()
    return f"✔️{current_date}\nSgin : {email}\nReferral : {referral_email}\n💰First Deposit : {amount:,} USDT💰\n🎉🎉🎉Congratulations on Joining CradeMaster!🎉🎉🎉"

# 출금 메시지 생성 함수
def generate_withdrawal_message():
    withdrawal_amount = random.randint(100, 3000) // 100 * 100
    email = generate_random_email()
    current_date = get_kst_date()
    return f"✔️{current_date}\nSgin : {email}\n💵Withdrawal : {withdrawal_amount:,} USDT💵\n💲Withdrawal has been successfully processed from CradeMaster💲"

# 텔레그램 메시지 전송 함수
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": message,
        "parse_mode": "HTML"
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"메시지 전송 성공: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")

# 메시지 랜덤 전송 함수 (입금/출금 메시지 랜덤 선택)
def random_send_message():
    transaction_type = random.choices(['deposit', 'withdraw'], [0.7, 0.3])[0]
    if transaction_type == 'deposit':
        message = generate_message_1() if random.choice([True, False]) else generate_message_2()
    else:
        message = generate_withdrawal_message()
    send_telegram_message(message)

# 무한 루프 실행 (별도 스레드)
def send_message_loop():
    while True:
        wait_time = random.randint(60, 180)
        print(f"다음 메시지는 {wait_time}초 후에 전송됩니다...")
        time.sleep(wait_time)
        random_send_message()

# VPN 연결 상태 테스트 함수
def test_vpn_connection():
    test_url = f"https://api.telegram.org/bot{bot_token}/getMe"
    try:
        response = requests.get(test_url, timeout=60)
        if response.status_code == 200:
            print("VPN이 정상적으로 연결되었습니다. 텔레그램 봇이 작동합니다.")
        else:
            print(f"에러 발생: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")

# Flask 서버 엔드포인트 설정
@app.route('/')
def home():
    return "CradeMaster Telegram Bot is running."

# Koyeb에서 실행할 메인 함수
if __name__ == '__main__':
    test_vpn_connection()  # VPN 상태 확인 후 실행
    thread = threading.Thread(target=send_message_loop, daemon=True)  # 백그라운드에서 실행
    thread.start()
    app.run(host='0.0.0.0', port=5000)  # Flask 서버 실행
