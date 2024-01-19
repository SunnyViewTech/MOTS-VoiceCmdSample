import requests
import random
import json
import keyboard
from pythonosc.udp_client import SimpleUDPClient
import azure.cognitiveservices.speech as speechsdk

# https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/SpeechServices
# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "", ""

def send_message(msg):
    ip = "127.0.0.1"
    port = 4999
    address = "/dollars/generate"
    client = SimpleUDPClient(ip, port)
    client.send_message(address, msg)

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

stop_recognition = False

def recognition_callback(event):
    if event.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(event.result.text))
        send_message(event.result.text)
    elif event.result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif event.result.reason == speechsdk.CancellationReason.Error:
        print("Error in speech recognition.")

speech_recognizer.recognized.connect(recognition_callback)
print("Say something...")

speech_recognizer.start_continuous_recognition()

try:
    while True:
        if keyboard.is_pressed('esc'):
            print("Esc key pressed, stopping recognition...")
            stop_recognition = True
            break

finally:
    speech_recognizer.stop_continuous_recognition()
    speech_recognizer.recognized.disconnect_all()
    print("Recognition stopped.")