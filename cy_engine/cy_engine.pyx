import chess


cdef class PositionCache:
    cdef public dict container
    cdef public list history
    cdef public long max_size

    def __init__(self):
        self.container = {}
        self.history = []
        self.max_size = 500000

    def add_to_cache(self, str position, long score):
        if position not in self.container:
            if len(self.container) < self.max_size:
                self.container[position] = score
                self.history.append(position)
            else:
                key = self.history.pop()
                self.container.pop(key)
                self.container[position] = score

    def get_position(self, str key):
        return self.container.get(key)


cdef class CyGameEngine:
    cdef public board
    cdef public str color
    cdef public long pawn_value
    cdef public long knight_value

    def __init__(self, color):
        self.board = chess.Board()
        self.color = color
        self.pawn_value = 100
        self.knight_value = 280