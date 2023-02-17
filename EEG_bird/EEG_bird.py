"""
EEG_bird is a game modeled after the popular flappy bird game, but adjusted to take EEG brain waves as input. In general, the more concentrated the higher bird flies, 
the more relaxed/eye closed the lower bird flies. To make the bird motion smoother, we make the concentration level correspond not directly to the height of the bird, but the 
velocity of the bird (velocity positive when bird concentrated, negative when relaxed). More detailed description: the concentration level concentration voltage - CUTOFF, 
normalized by the calibration up-low level, multiplied by some factor, is the velocity of the bird 
(this is given by the line of code: bird_rect.centery += 512 * VELOCITY * (1/sps) * ((rms_value-CUTOFF)/(high-low))

Even though the original flappy bird game is hard, using EEG signal as input makes the game even harder. There are many parameters one can change to adjust the difficulty 
level and make the game playable. These parameters are basically everything that is captalized (CUTOFF and everything under "Parameters related to game difficulty")

Ruining Zhang
6/4/2021
"""

import matplotlib.pyplot as plt
import pygame,sys,random
import time
import numpy as np
from adafruit_ads1x15.ads1x15 import ADS1x15
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn
import collections
import os
import board
import busio
import scipy as sp
from scipy import signal

sys.path.insert(1, os.path.dirname(os.getcwd()))
from analysis_tools import get_power_spectrum, get_rms_voltage


"""
Game parameters
"""
TOP_BOTTOM_SEP = 200 # how much one want the top and bottom pipe to be separated by
FLOOR_RATE = 1 # how fast floor moving left
PIPE_RATE = 1 # how fast pipe moving left
PIPE_HEIGHT = [200,300,400] # all the possible pipe heights
PIPE_INTERVAL = 3000 # time interval between pipes, unit ms
MAX_FRAME_RATE = 128 # Same as SPS, Caps the # frame/sample per second
SCORE_RATE = 0.01
INITIAL_BIRD_Y = 50 # initial y coordinate of the bird
VELOCITY = 0.5 # basically the proportionality factor between the eeg signal and bird velocity in game play

"""
ADC parameters
"""
sps = MAX_FRAME_RATE # Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300. Here, this is the same as frame rate
sinterval = 1.0/sps
sampletime = 0.5 # how long to look back in time for current alpha waves
time_series_len = int(sampletime * sps)
time_series = np.zeros(time_series_len)
freq = np.fft.fftfreq(time_series_len, d=1/sps) #Gets frequencies in Hz/sec
freq_min = 8 #minimum freq in Hz for alpha waves
freq_max = 12 #maximum freq in Hz for alpha waves
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
adc = ADS.ADS1115(i2c)
adc.mode = Mode.CONTINUOUS
adc.gain = 1
adc.data_rate = sps
calibration_time = 5

"""
Functions
"""
def calibration(calibration_time,sps,freq_min=8,freq_max=12):
    nsamples = calibration_time*sps
    interval = 1/sps
    time_series = np.zeros(nsamples)
    t0 = time.perf_counter()
    chan = AnalogIn(adc, ADS.P2, ADS.P3)
    
    #sos = sp.signal.butter(10, 60, 'lowpass', fs=860, output='sos')
    
    for i in range(nsamples): #Collects data every interval
        st = time.perf_counter()
        time_series[i] = chan.value*(4.096/32767)
        time_series[i] -= 3.3 #ADC ground is 3.3 volts above circuit ground
        while (time.perf_counter() - st) <= interval:
            pass
    #filtered = sp.signal.sosfilt(sos,time_series)
    t = time.perf_counter() - t0
    freq = np.fft.fftfreq(nsamples, d=1.0/sps)
    ps = get_power_spectrum(time_series)
    rms = get_rms_voltage(ps, freq_min, freq_max, freq, nsamples)

    plt.plot(time_series)
    plt.show()
    print('rms', rms)

    return rms

# function to draw 2 floor images next to each other
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos+288,450))

# create new pipe with random height in the pipe height list
def create_pipe():
    random_height = random.choice(PIPE_HEIGHT)
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_height))
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_height - TOP_BOTTOM_SEP))
    return bottom_pipe, top_pipe

# Take the pipe list as argument, move them to left (the same rate as floor?)
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= PIPE_RATE
    return pipes

# Draw pipes in pipe list
def draw_pipes(pipes):
    for pipe in pipes:
        # draw bottom pipe
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        # draw top pipe
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) # false flip in x direction True for flip in y direction
            screen.blit(flip_pipe,pipe)

# Check if bird_rect is colliding with any of the pipe_rect, also hit the window frame
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.bottom >= 450:
        return False
    return True

def score_display(game_state):
    if game_state == 'main_game':
        score_surface= game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface= game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
        
        high_score_surface= game_font.render(f'Best Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

input('Press Enter to start %.1f s calibration for relaxed data' % calibration_time)
print()
high = calibration(calibration_time,sps)

input('Press Enter to start %.1f s calibration for concentrated data' % calibration_time)
print()
low = calibration(calibration_time,sps)

mid = 0.5 * low+ 0.5 * high

"""
Game Section
"""
# initializing steps
pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',20)

# initialize game variables
game_active = True
# bird_movement = 0
score = 0
high_score = 0

# Load surfaces/images in the game
bg_surface = pygame.image.load('assets/background-day.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center = (INITIAL_BIRD_Y,256))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = [] # a list of pipes that pop up every second
SPAWNPIPE = pygame.USEREVENT # an event triggered by timer
pygame.time.set_timer(SPAWNPIPE, PIPE_INTERVAL) # the event is triggered every PIPE_INTERVAL second

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144, 256))


"""
Game Loop
"""

input('Press Enter to start the game')

chan = AnalogIn(adc, ADS.P2, ADS.P3)
CUTOFF = 0.75* low+ 0.25 * high

while True:

    # data taking + calculate RMS
    time_series = np.roll(time_series, -1) #rolls all voltage values back 1.
    time_series[-1] = chan.value*(4.096/32767)
    ps = get_power_spectrum(time_series)
    rms_value = get_rms_voltage(ps, freq_min, freq_max, freq, time_series_len)
    
    # game part
    for event in pygame.event.get(): # all events that pygame can detect
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # press space key to restart the game
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (INITIAL_BIRD_Y,256)
                score = 0
        
        #every PIPE_INTERVAL second, the event is triggered to create a new pipe
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) # extend allows list to include whatever that is in the tuple
    
    # display background
    screen.blit(bg_surface,(0,0))
    
    # display and create continuously moving floor effect
    floor_x_pos -= FLOOR_RATE
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
        
    if game_active:
        bird_rect.centery += 512 * VELOCITY * (1/sps) * ((rms_value-CUTOFF)/(high-low))
        screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)
    
        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += SCORE_RATE
        score_display('main_game')
        
    else: # game over state
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
        bird_rect.centery = 512 * mid/(high-low)
        
    pygame.display.update()
    
    clock.tick(MAX_FRAME_RATE)
