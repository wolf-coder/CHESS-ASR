# legal_moves = get_pieces()

def get_grammar(legal_moves):
    """
    processing the possible moves to spoken text
    yourstring = "L{0}L".format(yourstring)
    """
    grammar = ''
    for key, value in legal_moves.items():
        for elem in value:
            grammar+='\"{0}\", '.format(elem)
    return '[{0}\"[unk]\"]'.format(grammar)

def rec_grammar(data, recognizer):
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
    
