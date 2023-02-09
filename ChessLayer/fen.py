#!/usr/bin/env python3
import requests
import chess

Piece = {'K':"king",'Q':"queen",'N':"knight",'R':"rook",'B':"bishop"}

Number = {'1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight'}

Wrapped_Spk = {'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8',"king":'K',"queen":'Q',"knight":'N',"rook":'R',"bishop":'B',"x":'x',"check":'x'}


def Parse_move(move):
    """
    Function that takes a move and transcribe it to spoken text.
    Args:
    (move): string representing the pgn/fen move
    Return:
    (Parsed): Spoken text format for the pgn move
    """
    Parsed = ""
    for char in move:
        if char == 'O':
            if len(move) == 3:
                Parsed+="short castle"
            else:
                Parsed+="long castle"
            break
        if char == 'x':
            Parsed+='takes on '
        elif char == '+':
            Parsed+=' check'
        elif char.isupper():
           Parsed+= Piece[char] + " "
        elif char.islower():
           Parsed+= char + " "
        elif char.isdigit():
           Parsed+= Number[char]+ " "
        elif char == '#':
            Parsed+=" Checkmate"
    Parsed+=" \n"
    return " ".join(Parsed.split())



def Spoken_ToFen(Spoken):
    """
    convert Spoken text to fen
    Finish short castling...checkmate
    """
    if Spoken == 'short castle':
        return 'O-O'
    if Spoken == 'long castle':
        return 'O-O-O'
    Spoken = Spoken.replace("takes on", "x")
    Spoken = Spoken.replace("take on", "x")
    To_list = Spoken.split()


    spk =  ''
    for  elem  in  To_list:
        if len(elem) == 1:
            spk+=elem
        else:
            spk+=Wrapped_Spk[elem]
    return spk


def get_fen():
    """
    Function returning the CURRENT fen
    FEN example of return: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    """
    headers = {'Authorization': 'Bearer lip_U49eLe81bu3RcN4Gqe4X'}
    url = "https://lichess.org/api/account/playing"
    res = requests.get(url, headers = headers)
    if res.status_code != 200:
        print("Check your connection")
    res_json = res.json()
    fen = res_json["nowPlaying"][0]["fen"]
    return fen


def get_legalMoves():
    """
    Function that return the CURRENT possible moves to play.
    Example of return: ['Nh3', 'Nf3', 'Nc3', 'Na3', 'h3', 'g3', 'f3', 'e3', 'd3', 'c3', 'b3', 'a3', 'h4', 'g4', 'f4', 'e4', 'd4', 'c4', 'b4', 'a4']
    """
    fen = get_fen()
    board = chess.Board(fen)
    legal_moves = list(board.legal_moves)

    moves_t = str(board.legal_moves)[37:-1]
    moves_t = moves_t.replace(", ", "', '")
    moves_t = moves_t.replace("(", "('")
    moves_t = moves_t.replace(")", "')")
    moves_t = eval(moves_t)
    """
    moves_t: more than one move to play: ('Kf8', 'dxc5', 'g5', 'd5', 'a5')
    moves_t: one move to play: 'Kf8'
    """
    if type(moves_t) is not tuple: # One single move
        return [moves_t]

    moves = []
    for i in moves_t:
        moves.append(i)
    return moves


def get_pieces():
    """
    Function that returns a dictionary of the CURRENT legal moves per piece in spoken version.
    Example of return: {'knight': ['knight h three', 'knight f three'], 'pawn': ['h three']}
    """
    moves = get_legalMoves() # (INPUT: list of pgn leal moves)

    dic = {'N':[],'P':[],'K':[],'Q':[],'B':[],'R':[]}
    for move in moves:
        if move[0].islower():
            dic['P'].append(move)
        else:
            if move[0] == 'O': # Castling move
                dic['K'].append(move)
            else:
                dic[move[0]].append(move)

    pieces = {'knight':dic['N'], 'pawn':dic['P'], 'king':dic['K'], 'queen':dic['Q'], 'bishop':dic['B'], 'rook':dic['R']}
    
    # do not include pieces with no move to play
    updated = dict((key,value) for key, value in pieces.items() if value != []) 

    # get the spoken version of notation
    spk_fen={}
    for key in updated.keys():
        spk_fen[key] = []
        for fen in updated[key]:
            spk_fen[key].append(Parse_move(fen))
    return spk_fen


def get_grammar():
    """
    Function that return a tuple of:
      1. grammar to pass for the model recognizer.
        - Example: '["knight h six", "knight f six", "knight c six", "[unk]"]'
      2. `to_check`
        - 
    """
    legal_moves = get_pieces() # (INPUT)
    grammar = ''
    to_check= []
    for key, value in legal_moves.items():
        for elem in value:
            to_check.append(elem)
            grammar+='\"{0}\", '.format(elem)
    return '[{0}\"[unk]\"]'.format(grammar), to_check
