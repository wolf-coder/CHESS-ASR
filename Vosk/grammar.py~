def rec_grammar0(data, recognizer):
    """
    With grammar0
    """
    if recognizer.AcceptWaveform(data):
        recognizerResult = recognizer.Result()
        print("recognizerResult:", recognizerResult)
        # convert the recognizerResult string into a dictionary  
        resultDict = json.loads(recognizerResult)
        if not resultDict.get("text", "") == "":
            print("-> ", resultDict['text'])
            # command sent to selenium
        else:
            print("no input sound")
    
