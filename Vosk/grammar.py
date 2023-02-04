# legal_moves = get_legalMoves()

grammar0 = '["pawn king queen knight rook bishop ", "take takes on","a b c d e f g h", "one two three four five six seven eight"]'

grammar1 = '["one zero one two three oh", "four five six", "seven eight nine zero", "[unk]"]'

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
    
