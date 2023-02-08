#!/usr/bin/env python3
import requests
import chess

Piece = {'K':"king",'Q':"queen",'N':"knight",'R':"rook",'B':"bishop"}

Number = {'1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight'}

Wrapped_Spk = {'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6','seven':'7','eight':'8',"king":'K',"queen":'Q',"knight":'N',"rook":'R',"bishop":'B',"x":'x'}


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
                Parsed+="short castling"
            else:
                Parsed+="long castling"
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
    """
    headers = {'Authorization': 'Bearer lip_U49eLe81bu3RcN4Gqe4X'}
    url = "https://lichess.org/api/account/playing"
    pgn = requests.get(url, headers = headers)
    pgnjson = pgn.json()
    fen = pgnjson["nowPlaying"][0]["fen"]

    return fen

def get_legalMoves():
    """
    """
    board = chess.Board(get_fen())
    legal_moves = list(board.legal_moves)

    moves_t = str(board.legal_moves)[37:-1]
    moves_t = moves_t.replace(", ", "', '")
    moves_t = moves_t.replace("(", "('")
    moves_t = moves_t.replace(")", "')")
    moves_t = eval(moves_t)
    moves = []

    for i in moves_t:
        moves.append(i)
    return moves


def get_pieces():
    """
    """
    moves = get_legalMoves()
    dic = {'N':[],'P':[],'K':[],'Q':[],'B':[],'R':[]}
    for move in moves:
        if move[0].islower():
            dic['P'].append(move)
        else:
            dic[move[0]].append(move)
    pieces = {'knight':dic['N'],'pawn':dic['P'],'king':dic['K'],'queen':dic['Q'],'bishop':dic['B'],'rook':dic['R']}
    updated = dict((key,value) for key, value in pieces.items() if value != [])
    spk_fen={}
    
    for key in updated.keys():
        spk_fen[key] = []
        for fen in updated[key]:
            spk_fen[key].append(Parse_move(fen))
    return spk_fen


def get_grammar(legal_moves):
    """
    """
    grammar = ''
    to_check= []
    for key, value in legal_moves.items():
        for elem in value:
            to_check.append(elem)
            grammar+='\"{0}\", '.format(elem)
    return '[{0}\"[unk]\"]'.format(grammar), to_check
