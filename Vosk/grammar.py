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
            SpokeN=resultDict['text']
            if "unk"  not in SpokeN and len(SpokeN.split()) >= 2 :
                fen_ToSend = Spoken_ToFen(SpokeN)
                print("Sending \"{}\" to selenium".format(fen_ToSend))
                Keyboard_commands(driver, fen_ToSend)
                Waiting_Myturn(driver) # Placed
                grammar = get_grammar(get_pieces())
                #breakpoint()
                recognizer.SetGrammar(grammar)
                print("command is received")
        else:
            print("no input sound")
    
