#!/usr/bin/env python3

import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from Selenium.Selenium_Functions import *
from ChessLayer.fen import *


# list Input/Output devices
print(" Displaying input/output devices:")
print(sd.query_devices())


# get the device sample rate
device_info = sd.query_devices(sd.default.device[0], 'input')
samplerate = int(device_info['default_samplerate'])


print("===>  Device Number:{} \nDevice Info: {}".format(sd.default.device[0],
                                                        device_info))

# setup queue and callback function
q = queue.Queue()


def recordCallback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


# build the model and recognizer objects.
print("===> Build the model and recognizer objects.")
model = Model(lang="en-us")

recognizer = KaldiRecognizer(model, samplerate)
recognizer.SetWords(False)


# Starting selenium
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
Connect_To_Lichess(driver)

# wait for our turn then speak our move
Waiting_Myturn(driver)  # selenium listen to an element
grammar, to_check = get_grammar()
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
                    SpokeN = resultDict['text']
                    if "unk" not in SpokeN and len(SpokeN.split()) >= 2\
                       and SpokeN in to_check:
                        fen_ToSend = Spoken_ToFen(SpokeN)
                        print("Sending \"{}\" to selenium".format(fen_ToSend))
                        Keyboard_commands(driver, fen_ToSend)
                        Waiting_Myturn(driver)
                        grammar, to_check = get_grammar()
                        recognizer.SetGrammar(grammar)
                        print("command is received")
                    else:
                        print("{}: Not a move/legal_move".format(SpokeN))
                else:
                    print("no input sound")

except KeyboardInterrupt:
    print('===> Finished Recording')
except Exception as e:
    print(str(e))
