import openai
import numpy as np
#from adafruit_ads1x15.ads1x15 import ADS1x15
#import adafruit_ads1x15.ads1115 as ADS
#from adafruit_ads1x15.ads1x15 import Mode
#from adafruit_ads1x15.analog_in import AnalogIn
#import board
#import busio
import scipy as sp
import time
from speech_tools import speech_to_text, text_to_speech
import speech_recognition as sr
import pyttsx3

def get_prompts(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=50,
        n=2,
        temperature=0.7,
        frequency_penalty=0.7,
        presence_penalty=0.3,
        stop='. '
    )
    time.sleep(1) 
    message1 = response.choices[0].text.strip()
    if ":" in message1:
        message1 = message1.split(":")[1].strip()
    if '\n' in message1:
        message1 = message1.split("\n", 1)[0].strip()
    if 'AI' in message1:
        message1 = message1.split("AI", 1)[0].strip()
    message2 = response.choices[1].text.strip()
    if ":" in message2:
        message2 = message2.split(":")[1].strip()
    if '\n' in message2:
        message2 = message2.split("\n", 1)[0].strip()
    if 'AI' in message2:
        message2 = message2.split("AI", 1)[0].strip()
    return message1, message2, "More Options", "Bye"



# Set OpenAI API key
openai.api_key = "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"

