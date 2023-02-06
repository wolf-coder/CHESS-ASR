#!/usr/bin/env python3
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json


# selenium requirements
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from   Selenium.Selenium_Functions import *
from ChessLayer.fen import *


# list Input/Output devices
print("input/output devices:")
print(sd.query_devices())


# get the sample rate 
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

Waiting_Myturn(driver) # Placed
grammar, to_check = get_grammar(get_pieces())
recognizer.SetGrammar(grammar)

try:
    with sd.RawInputStream(dtype='int16',
                           channels=1,
                           callback=recordCallback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):

                recognizerResult = recognizer.Result()
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
