
import sys
import os
sys.path.insert(1, os.path.dirname(os.getcwd())) #Allows importing files from parent folder
import time
import pickle
import threading
import multiprocessing
import numpy as np
import scipy as sp
from scipy import signal
from scipy.signal import butter, sosfilt
import matplotlib.pyplot as plt

from openai_application import get_prompts


if __name__ == "__main__":

	while True:
		
		speech = 'How are you?'
		# get_prompts function to get 4 prompts 
		prompt_1, prompt_2, prompt_3, prompt_4 = get_prompts(speech)
		
		print("1. " + prompt_1)
		print("2. " + prompt_2)
		print("3. " + prompt_3)



	


	





