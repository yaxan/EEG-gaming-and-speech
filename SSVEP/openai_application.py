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
from speech.py import speech_to_text, text_to_speech
import speech_recognition as sr
import pyttsx3

def get_prompts(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50,
        n=2,
        temperature=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.7,
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

# Set the initial prompt
ice_breaker = "Hello, how are you doing today?"
prompt = f'AI: {ice_breaker}\n'

#generate responses using OpenAI Text Completion API
def generate_user_response(prompt):
    '''
    temperature: controls randomness of the generated responses
    max_tokens: limits length of response
    n = possible responses
    frequency_penalty: higher decreases the likelihood of generating the same words multiple times -> controls diversity
    presence_penalty: higher presence penalty decreases the likelihood of generating the same phreases across multiple responses -> diversity
    stop: tells the code to stop printing at a value given (makes sure output is a one line output with one response)
    '''
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50,
        n=2,
        temperature=0.8,
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
    
    return message1, message2

def generate_AI_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=50,
        n=1,
        temperature=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.7,
        stop='.'
    )
    time.sleep(1) 
    return response.choices[0].text.strip()


def generate_conversation_toAI(prompt):
    #generate conversation to AI
    message1, message2 = generate_user_response(prompt)
        
    print("1. " + message1)
    print("2. " + message2)
    print("3. Give me more options")
    print("4. Quit")
    user_choice = input("> ")
        
    while user_choice == '3':
        #generate responses
        message1, message2 = generate_user_response(prompt)
        print("Bot: Here are two more options:")
        print("1. " + message1)
        print("2. " + message2)
        print("3. Give me more options")
        print("4. Quit")
        user_choice = input("You: ")
    
    if user_choice == '1':
        print("You: " + message1)
        return user_choice, message1
    elif user_choice == '2':
        print("You: " + message2)
        return user_choice, message2
    elif user_choice == '4':
        return user_choice, ""

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.7)

recognizer = sr.Recognizer()
prompt = speech_to_text(recognizer)
        
while True:
    print(prompt)
    
    #generate responses
    message1, message2 = generate_user_response(prompt)
    
    print("1. " + message1)
    print("2. " + message2)
    print("3. Give me more options")
    print("4. Quit")
    
    #CHANGE THIS FOR USER INPUT USING FREQUENCY
    '''
    pesudo code: 
    user_choice = input using frequency
    input = list of 4 frequency with certain percentage value
    highest = input[whatever is wanted at what frequency]
    user_choice = highest
    '''
    
    user_choice = input("> ")

    # generate two more responses if option 3 is chosen
    while user_choice == '3':
        #generate responses
        message1, message2 = generate_user_response(prompt)
        print("Bot: Here are two more options:")
        print("1. " + message1)
        print("2. " + message2)
        print("3. Give me more options")
        print("4. Quit")
        user_choice = input("You: ")

    # generate response based on user choice
    if user_choice == "1":
        print("You: " + message1)
        text_to_speech(engine, message1)
        print("what do you want to say now?")
        #add user's choice as prompt to ask the ai
        prompt += message1
        #generate conversation to AI
        user_choice, prompt = generate_conversation_toAI(prompt)
        
        if user_choice == "4":
            print("Bot: Goodbye!")
            break
        else:
            AI_response = speech_to_text(prompt) 
            print("Bot: " + AI_response)
            prompt = AI_response
    elif user_choice == "2":
        print("You: " + message2)
        print("what do you want to say to the AI?")
        #add user's choice as prompt to ask the ai
        prompt += message2
        #generate conversation to AI
        user_choice, prompt = generate_conversation_toAI(prompt)
        
        if user_choice == "4":
            print("Bot: Goodbye!")
            break
        else:
            AI_response = generate_AI_response(prompt) 
            print("Bot: " + AI_response)
            prompt = AI_response
    elif user_choice == "4":
        print("Bot: Goodbye!")
        break