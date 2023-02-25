# EEG gaming and SSVEP Speech

## Projects Description
This project shows how you can build a Brain-Computer Interface with EEG to play games using alpha/beta waves as well as use steady state visually evoked potential (SSVEP) to communicate. The brain produces alpha waves in a relaxed state, like when your eyes are closed, in the 7.5-13 Hz range, and beta waves when you're concentrated in the 12-32 Hz range, at amplitudes less than 50 μV. We filter, amplify and process these waves originating from the occiptal lobe and classify between relaxed and concentrated states to play Flappy Bird. 

We also decided to take our hands at an SSVEP communication system. The SSVEP is the EEG response evoked by visual stimuli at a specific frequency, which results in an increase in the EEG at that same frequency. Using this information we've built a system that allows a person A to speak to person B connected to the EEG. Person A's speech is fed to OpenAI's [Text Completion](https://platform.openai.com/docs/guides/completion) API to generate appropriate responses for person B to choose from by looking at a strobe with a specific frequency corresponding with the desired response. Their desired response is then converted from text to speech to allow both parties to communicate verbally.

More details on how it works and how to replicate coming soon.

## Live Flappy-Bird Demo
https://user-images.githubusercontent.com/41130598/219846836-aeb79bd7-619f-477f-9fea-56bf63279e5b.mp4

## Live SSVEP Speech Demo
https://user-images.githubusercontent.com/41130598/219846836-aeb79bd7-619f-477f-9fea-56bf63279e5b.mp4

## Circuit

### Overview
  This circuit is designed to take the differntial input of the FP2 and O2 regions on the brain, amplify signals from ~8-32Hz, and send to the Raspberry Pi for processing. It uses a combination of instrument amplifiers, high pass, low pass, and notch filters to filter and amplify the signals before they are sent to the ADC to conver the signal from analog to digital which the Raspberry Pi can then process.

### Parts List
 * 2x AD623AN Instrument Amplifier
 * 4x LM471CN Operational Amplifier
 * 2x 150kΩ Resistor
 * 1x 1.1kΩ Resistor
 * 8x 220nF Capacitor
 * 4x 12kΩ Resistor
 * 4x 5.6kΩ Resistor
 * 2x 22kΩ Resistor
 * 2x 402Ω Resistor (Use 1x 200Ω Instead)
 * 1x 0-2kΩ Potentiometer
 * [3x OpenBCI Gold Cup Electrodes](https://shop.openbci.com/products/openbci-gold-cup-electrodes?_pos=1&_sid=645e136ca&_ss=r)
 * [Ten20 Conductive Neurodiagnostic Electrode Paste](https://shop.openbci.com/products/ten20-conductive-paste-8oz-jar)
 * Adafruit ADS1115 16-Bit ADC
 * Raspberry Pi 4 Model B 4GB RAM
 * Medical Tape (To stick on electrodes)
 * Keithley 2231A-30-3 Triple Channel DC Power Supply (Batteries work too)

### Schematic
![EEGSchematic](https://user-images.githubusercontent.com/41130598/221042409-423589c1-2b3c-4a02-94aa-657f63461b93.png)
Warning: Connecting electrodes to any part of your body can result in shock if anything goes wrong with the circuit, there are no safety features implemented to use at your own discretion.

  Three electrodes are used, one at the FP2 region (one inch up from the naison and one inch right), one at the O2 region (one inch up from the inion and one inch right), and one on the earlobe or mastoid which connects to 3.3V ground. It's important to note the voltage values for the IAs and Op-Amps are with respect to the RPI's 3.3V ground, while the ADC uses the RPI's 0V ground. This is to up-shift the signal from the brain because the ADC does not handle negative values well, it's then shifted back down in the code. If you are attempting to reconstruct this circuit, it's important to have access to an oscilloscope and wave-function generator to debug and test it works fine before connecting to electrodes/ADC/RPI.

Stage 1: Instrument Amplifier (Gain: ~92)

Stage 2: Notch Filter (Gain: 1, Cutoff frequency: ~60Hz)

Stage 3: High-Pass Filter (Gain: 1, Cutoff frequency: ~5Hz)

Stage 4: Low-Pass Filter (Gain: 1, Cutoff frequency: ~33Hz)

Stage 5: Instrument Amplifier (Gain: ~46-500)

Stage 6: Notch Filter (Gain: 1, Cutoff frequency: ~60Hz)


### Physical Circuit
![EEG-circuit](https://user-images.githubusercontent.com/41130598/219847191-df59c969-152d-49f6-9052-b21f6ea1c098.png)

## Data Collection & Analysis

### Data Collection

#### Imports

  1. [busio](https://docs.circuitpython.org/en/latest/shared-bindings/busio/index.html)
  2. [Ada Fruit as ADS](https://docs.circuitpython.org/projects/ads1x15/en/latest/index.html)
  3. [Ada Fruit AnalongIn](https://docs.circuitpython.org/projects/ads1x15/en/latest/api.html)
  4. [Scipy Signal SOS Filt](https://docs.scipy.org/doc/scipy/reference/signal.html)

Data collected as either **"relaxed.pickle"** or **"concentrated.pickle"**. Data Filtrered using sosfilt function from SciPy. 

### Analysis

#### Imports 

  1. [SciPy Fourier Transforms](https://docs.scipy.org/doc/scipy/tutorial/fft.html) 

The RMS voltage of a waveform between two frequency limits was calculated using [Parseval's Theorem](https://blog.prosig.com/2015/01/06/rms-of-time-history-and-fft-spectrum/#:~:text=Parseval's%20theorem%20states%20that%20the,to%20the%20Sample%20Rate%2C%20SR.) and the obtained power spectrum. [Gaussian evaluation](https://en.wikipedia.org/wiki/Gaussian_integral) was performed using the mean and standard deviation of the relaxed and concentrated data. From the data obtained, results that were positive and that were both smaller than the mean of the relaxed data and greater than the mean of the concentrated data were taken as the cross point of the two mean values. 

#### Relaxed and Concentrated State Data
![Relaxed and Concentrated State Data](https://user-images.githubusercontent.com/74623611/221341181-d602a7bc-076a-491f-b9f8-d3246c04d0b0.png)
#### Relaxed and Concentrated State Power Spectrum
![Relaxed and Concentrated State Power Spectrum](https://user-images.githubusercontent.com/74623611/221341190-48766f1c-71db-4ed2-b3c6-0c397a96dadd.png)
#### Relaxed and Concentrated State Brain Wave
![Relaxed and Concentrated State Brain Wave](https://user-images.githubusercontent.com/74623611/221341202-5c23d0e9-0eb2-4240-a81d-a5e5512eb718.png)



## EEG Gaming

### Flappy Bird Code


## SSVEP Speech

### GUI

                    Need Information and Picture of the GUI Layout

### Speech to Text & Text to Speech
#### Speech to Text
 We used the [Speech Recognition](https://pypi.org/project/SpeechRecognition/) library to listen for audio and convert it to text. "recognizer.listen" was used to collect the audio data, and "recognizer,recognize_google" was used to obtain the text version. 
 
 #### Text to Speech
 We used the [pyttsx3](https://pypi.org/project/pyttsx3/) library to initiate an engine. The rate and volume were set, and the functions "engine.say" and "engine.runAndWait" were used to obtain text to speech. 

### AI Generated Script
#### [OpenAI Text Completion API](https://platform.openai.com/docs/guides/completion) "Davinci" Model

The model model always generates three messages, with a fourth choice of getting three more messages. The model was called three times and fed three different prompts of:
  1. f"What would a human say in response to: '{**text**}'\nAI response:"
  2. f"What would an AI say in response to the following if it were human: '{**text**}'\nResponse:"
  3. f"Imagine an AI conversation about '{**text**}'. What would the AI say if it was trying to act human?\nResponse:"

where **text** is the input that the model takes which is dervied from speech to text. With the messages generated from the model, string formatting using **Python** was done to obtain the desired output string format. 

#### Different Models Considered
  1. [Google T5 (Text-to-Text Transfer Transformer) Model](https://paperswithcode.com/method/t5#:~:text=T5%2C%20or%20Text%2Dto%2D,to%20generate%20some%20target%20text.) 
  2. [Rasa Model](https://github.com/RasaHQ/rasa) 
  
## Credits

This project was based on the guidance from https://github.com/ryanlopezzzz/EEG with a modified circuit and new code for data-gathering, analysis, and gameplay. The repository had amazing explanations for everything and Ryan was great help when we reached out to him with questions. Much of their code no longer works as of January 2023 so we hope our project can help others replicate something similar for getting started with BCIs and EEG.
