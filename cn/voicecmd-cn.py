#pip install baidu-aip
from aip import AipSpeech
import speech_recognition as sr
import requests
import random
import json
from pythonosc.udp_client import SimpleUDPClient
import time

# 代码参考
# https://blog.csdn.net/zcs2632008/article/details/123334807
# https://ai.baidu.com/ai-doc/MT/4kqryjku9

# https://console.bce.baidu.com/ai/?fromai=1#/ai/speech/overview/index
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

# https://cloud.baidu.com/product/mt/text_trans
client_id = ""
client_secret = ""

def get_text(wav_bytes):
    result = AipSpeech(APP_ID, API_KEY, SECRET_KEY).asr(wav_bytes, 'wav', 16000, {'dev_pid': 1537,})
    try:
        text = result['result'][0]
    except Exception as e:
        print(e)
        text = ""
    return text

def get_token():
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
    
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    return response_json.get("access_token", None)

def translate_text(text, token, from_lang='zh', to_lang='en'):
    url = f'https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token={token}'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'q': text, 'from': from_lang, 'to': to_lang})

    try:
        response = requests.post(url, data=payload, headers=headers)
        result = response.json()
        return result["result"]["trans_result"][0]["dst"]
    except Exception as e:
        print(f"Error in translate_text: {e}")
        return ""

def send_message(msg):
    # OSC服务器的IP地址和端口
    ip = "127.0.0.1"  # 替换为目标IP地址
    port = 4999       # 替换为目标端口号
    address = "/dollars/generate"
    # 创建OSC客户端
    client = SimpleUDPClient(ip, port)
    # 发送OSC消息
    client.send_message(address, msg)


while True:
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("请说话...")
     
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
     
    audio_data = audio.get_wav_data(convert_rate=16000)
    print("正在分析...")
     
    text = get_text(audio_data)
    print(text)
    token = get_token()
    msg = translate_text(text, token)
    print(msg)

    send_message(msg)
    time.sleep(1)

        