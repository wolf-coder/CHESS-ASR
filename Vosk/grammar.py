# legal_moves = get_pieces()


def rec_process(data, recognizer):
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
            if "unk"  not in resultDict['text']:
                fen_ToSend = Spoken_ToFen(resultDict['text'])
                print("Sending \"{}\" to selenium".format(fen_ToSend))
                
                recognizer.SetGrammar(grammar0)
                # command sent to selenium
        else:
            print("no input sound")
    
