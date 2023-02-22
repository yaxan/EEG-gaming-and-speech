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
from analysis_data import rms_voltage_power_spectrum

"""
ADC parameters
"""
sps = 250 # Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300. Here, this is the same as frame rate
sinterval = 1.0/sps
sampletime = 0.25 # how long to look back in time for current alpha waves
raw_signal_len = int(sampletime * sps)
raw_signal = np.zeros(raw_signal_len)
min_freq = 8 #minimum freq in Hz for alpha waves
max_freq = 12 #maximum freq in Hz for alpha waves
#i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
#adc = ADS.ADS1115(i2c)
#adc.mode = Mode.CONTINUOUS
#adc.gain = 1
#adc.data_rate = sps
calibration_time = 5

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
        temperature=0.5,
        frequency_penalty=0.7,
        presence_penalty=0.7,
        stop='. '
    )
    message1 = response.choices[0].text.strip().split(":")[1].strip()
    message1 = message1.split("\n")[0].strip()
    message2 = response.choices[1].text.strip().split(":")[1].strip()
    message2 = message2.split("\n")[0].strip()
    
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
    print(response.choices[0].text.strip())
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
        print("what do you want to say to the AI?")
        #add user's choice as prompt to ask the ai
        prompt += message1
        #generate conversation to AI
        user_choice, prompt = generate_conversation_toAI(prompt)
        
        if user_choice == "4":
            print("Bot: Goodbye!")
            break
        else:
            AI_response = generate_user_response(prompt) 
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
            AI_response = generate_user_response(prompt) 
            print("Bot: " + AI_response)
            prompt = AI_response
    elif user_choice == "4":
        print("Bot: Goodbye!")
        break