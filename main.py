#!/usr/bin/env python3
"""
Resource:https://singerlinks.com/2022/03/how-to-convert-microphone-speech-to-text-using-python-and-vosk/
"""
###  to delete
from os import chdir
chdir("/home/cuore-pc/Programming/Project/Chess-ASR/")
###


import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json


####  to start selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from   Selenium.Selenium_Functions import *
from ChessLayer.fen import *
####

'''This script processes audio input from the microphone and displays the transcribed text.'''

# list all audio devices known to your system
print("Display input/output devices")
print(sd.query_devices())


# get the samplerate - this is needed by the Kaldi recognizer
device_info = sd.query_devices(sd.default.device[0], 'input')
samplerate = int(device_info['default_samplerate'])

# display the default input device
print("===> Initial Default Device Number:{} Description: {}".format(sd.default.device[0], device_info))

# setup queue and callback function
q = queue.Queue()

def recordCallback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
    
# build the model and recognizer objects.
print("===> Build the model and recognizer objects.  This will take a few minutes.")
model = Model(lang="en-us")

recognizer = KaldiRecognizer(model, samplerate)
recognizer.SetWords(False)


### Starting selenium
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
Connect_To_Lichess(driver) #?
###
Waiting_Myturn(driver) # Placed
grammar, to_check = get_grammar(get_pieces())
recognizer.SetGrammar(grammar)

print("===> Begin recording. Press Ctrl+C to stop the recording ")
recognizer.SetGrammar(grammar)
try:
    with sd.RawInputStream(dtype='int16',
                           channels=1,
                           callback=recordCallback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):

                recognizerResult = recognizer.Result()
                #print("recognizerResult:", recognizerResult)
                # convert the recognizerResult string into a dictionary  
                resultDict = json.loads(recognizerResult)
                if not resultDict.get("text", "") == "":
                    print("-> ", resultDict['text'])
                    SpokeN=resultDict['text']
                    print(to_check)
                    if "unk"  not in SpokeN and len(SpokeN.split()) >= 2 and SpokeN in to_check:
                        fen_ToSend = Spoken_ToFen(SpokeN)
                        print("Sending \"{}\" to selenium".format(fen_ToSend))
                        Keyboard_commands(driver, fen_ToSend)
                        Waiting_Myturn(driver) # Placed
                        grammar, to_check = get_grammar(get_pieces())
                        #breakpoint()
                        recognizer.SetGrammar(grammar)
                        print("command is received")
                else:
                    print("no input sound")

except KeyboardInterrupt:
    print('===> Finished Recording')
except Exception as e:
    print(str(e))


#rec.SetGrammar('["one zero one two three oh", "four five six", "seven eight nine zero", "[unk]"]')
