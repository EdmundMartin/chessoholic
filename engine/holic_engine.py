from typing import List, Optional, Tuple

import chess

from engine.consts import PAWN_TABLE, KNIGHT_TABLE, BISHOP_TABLE, ROOK_TABLE, QUEEN_TABLE, KING_TABLE
from engine.caching import PositionCache


WHITE = 'WHITE'
BLACK = 'BLACK'


class GameEngine:

    __slots__ = ('_color', 'board', 'PAWN_VALUE', 'KNIGHT_VALUE', 'BISHOP_VALUE', 'ROOK_VALUE',
                 'QUEEN_VALUE', 'PAWN_TABLE', 'KNIGHT_TABLE', 'BISHOP_TABLE', 'ROOK_TABLE',
                 'QUEEN_TABLE', 'KING_TABLE', 'move_history', 'position_cache')

    def __init__(self, engine_color: str = WHITE, pawn_value: int = 100, knight_value: int = 280,
                 bishop_value: int = 320, rook_value: int = 500, queen_value: int = 900,):
        self._color = engine_color
        self.board = chess.Board()

        self.PAWN_VALUE = pawn_value
        self.KNIGHT_VALUE = knight_value
        self.BISHOP_VALUE = bishop_value
        self.ROOK_VALUE = rook_value
        self.QUEEN_VALUE = queen_value

        self.PAWN_TABLE = PAWN_TABLE
        self.KNIGHT_TABLE = KNIGHT_TABLE
        self.BISHOP_TABLE = BISHOP_TABLE
        self.ROOK_TABLE = ROOK_TABLE
        self.QUEEN_TABLE = QUEEN_TABLE
        self.KING_TABLE = KING_TABLE

        self.move_history = []
        self.position_cache = PositionCache()

    def is_engine_turn(self):
        if self._color == WHITE:
            return self.board.turn
        else:
            return not self.board.turn

    def is_checkmate(self) -> Tuple[bool, int]:
        in_check = self.board.is_checkmate()
        if in_check and self.is_engine_turn():
            return True, -9999
        elif in_check:
            return True, 9999
        return False, 0

    def is_stalemate(self) -> Tuple[bool, int]:
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return True, 0
        return False, 0

    def _calculate_material(self) -> int:
        val_map = {
            1: self.PAWN_VALUE,
            2: self.KNIGHT_VALUE,
            3: self.BISHOP_VALUE,
            4: self.ROOK_VALUE,
            5: self.QUEEN_VALUE,
        }
        material_score: int = 0
        for k, v in val_map.items():
            white_pieces = len(self.board.pieces(k, chess.WHITE))
            black_pieces = len(self.board.pieces(k, chess.BLACK))
            material_score += v * (white_pieces - black_pieces)
        return material_score

    def _calculate_position(self) -> int:
        pos_score = 0
        val_map = {
            1: self.PAWN_TABLE,
            2: self.KNIGHT_TABLE,
            3: self.BISHOP_TABLE,
            4: self.ROOK_TABLE,
            5: self.QUEEN_TABLE,
            6: self.KING_TABLE,
        }
        for key, table in val_map.items():
            pos_sq = sum([table[i] for i in self.board.pieces(key, chess.WHITE)])
            pos_sq -= sum([table[i] for i in self.board.pieces(key, chess.BLACK)])
            pos_score += pos_sq
        return pos_score

    def eval_board(self) -> int:
        fen = self.board.fen()
        score = self.position_cache.get_position(fen)
        if score:
            self.position_cache.add_to_cache(fen, score)
            return score
        check, score = self.is_checkmate()
        if check:
            self.position_cache.add_to_cache(fen, score)
            return score
        stale, score = self.is_stalemate()
        if stale:
            return score
        material = self._calculate_material()
        pos_score = self._calculate_position()
        total_score = material + pos_score
        if self._color == WHITE:
            self.position_cache.add_to_cache(fen, score)
            return total_score
        self.position_cache.add_to_cache(fen, score)
        return -total_score

    def quiesce(self, alpha, beta):
        stand_pat = self.eval_board()
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move)
                score = -self.quiesce(-beta, -alpha)
                self.board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

    def alpha_beta(self, alpha, beta, depth_left: int):
        best_score = -9999
        if depth_left == 0:
            return self.quiesce(alpha, beta)
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.alpha_beta(-beta, -alpha, depth_left - 1)
            self.board.pop()
            if score >= beta:
                return score
            if score > best_score:
                best_score = score
            if score > alpha:
                alpha = score
        return best_score

    def select_move(self, depth):
        best_move = chess.Move.null()
        best_value = -99999
        alpha = -100000
        beta = 100000
        for move in self.board.legal_moves:
            self.board.push(move)
            board_value = -self.alpha_beta(-beta, -alpha, depth - 1)
            if board_value > best_value:
                best_value = board_value
                best_move = move
            if board_value > alpha:
                alpha = board_value
            self.board.pop()
        self.move_history.append(best_move)
        return best_move


if __name__ == '__main__':
    engine = GameEngine()

    result = engine.eval_board()
    print(result)