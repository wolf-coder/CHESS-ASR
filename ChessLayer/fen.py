#!/usr/bin/env python3
import requests
import chess
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
    breakpoint()
    moves_t = moves_t.replace(", ", "', '")
    moves_t = moves_t.replace("(", "('")
    moves_t = moves_t.replace(")", "')")
    moves_t = eval(moves_t)
    moves = []

    for i in moves_t:
        moves.append(i)
    return moves
