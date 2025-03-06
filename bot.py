import datetime  # 날짜 관련 기능
import pytz  # 시간대 설정을 위한 라이브러리
import random  # 랜덤값 생성
import requests  # Telegram API에 요청을 보내기 위한 라이브러리
import time  # 시간을 다루기 위한 모듈 추가
import json  # JSON 데이터를 처리하기 위한 모듈 추가
from fastapi import FastAPI  # FastAPI 추가
import uvicorn  # Uvicorn 추가 (FastAPI 실행용)
import threading  # 쓰레드를 사용하기 위한 모듈

# 한국 시간(KST) 기준으로 날짜 가져오기
def get_kst_date():
    tz = pytz.timezone('Asia/Seoul')
    kst_time = datetime.datetime.now(tz)
    return kst_time.strftime('%B %d, %Y')  # 'March 05, 2025' 형식

# 봇의 API 토큰 및 채널 설정
bot_token = '7517066350:AAG1tqomFYoygL_SljeWuJO2MMHoMxI4wFs'
channel_id = '@crademaster_ch'  # 채널 ID

# 이메일 랜덤 생성 함수
def generate_random_email():
    prefix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=2))  # 2글자 랜덤 생성
    domain = random.choice(['com', 'net', 'co.kr'])  # 도메인 랜덤 선택
    email = f"{prefix}*****@*****.{domain}"  # 두 글자 랜덤 영문 소문자와 함께 이메일 생성
    return email

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
    referral_email = generate_random_email()  # 랜덤 추천인 이메일
    current_date = get_kst_date()  # 한국 시간으로 현재 날짜 가져오기
    return f"✔️{current_date}\nSgin : {email}\nReferral : {referral_email}\n💰First Deposit : {amount:,} USDT💰\n🎉🎉🎉Congratulations on Joining CradeMaster!🎉🎉🎉"

# 출금 메시지 생성 함수
def generate_withdrawal_message():
    withdrawal_amount = random.randint(100, 3000) // 100 * 100  # 100~3000 사이 랜덤, 100단위
    email = generate_random_email()
    current_date = get_kst_date()  # 한국 시간으로 현재 날짜 가져오기
    return f"✔️{current_date}\nSgin : {email}\n💵Withdrawal : {withdrawal_amount:,} USDT💵\n💲Withdrawal has been successfully processed from CradeMaster💲"

# 텔레그램 메시지 전송 함수
def send_telegram_message(message):
    global channel_id  # 채널 ID 변수 사용

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": message,
        "parse_mode": "HTML"  # HTML 형식으로 메시지 전송
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        print(f"메시지 전송 성공: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"에러 발생: {e}")
        print(f"에러 응답 내용: {response.text}")
        return None

# 메시지 랜덤 전송 함수 (입금/출금 메시지 랜덤 선택)
def random_send_message():
    transaction_type = random.choices(['deposit', 'withdraw'], [0.7, 0.3])[0]  # 입금: 70%, 출금: 30%
    
    if transaction_type == 'deposit':
        message = generate_message_1() if random.choice([True, False]) else generate_message_2()
    else:
        message = generate_withdrawal_message()
    
    send_telegram_message(message)

# 메시지 전송 주기 설정 (1분에서 12분 사이 랜덤 시간)
def send_message_with_random_delay():
    while True:
        wait_time = random.randint(60, 180)
        print(f"다음 메시지는 {wait_time}초 후에 전송됩니다...")
        time.sleep(wait_time)
        random_send_message()

# FastAPI 웹 서버 생성
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Telegram bot is running!"}

# 텔레그램 봇을 별도의 쓰레드에서 실행
def start_bot():
    send_message_with_random_delay()

# Koyeb은 8000번 포트에서 실행되어야 함
if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()  # 텔레그램 봇 쓰레드 시작

    # FastAPI 서버 실행 (포트 8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)

