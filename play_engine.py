import time

from engine.holic_engine import PyGameEngine
#from engine.cy_holic_engine import CyGameEngine


if __name__ == '__main__':
    turn = 'CPU'
    game = PyGameEngine()
    while True:
        if turn == 'CPU':
            start = time.time()
            mov = game.select_move(2)
            print(mov)
            print('Move took: ', time.time() - start)
            game.board.push(mov)
            turn = 'Human'
        else:
            print(game.board)
            while True:
                try:
                    valid_move = input('Enter Move:')
                    mov = game.board.push_uci(valid_move)
                except Exception as e:
                    print('Invalid move')
                else:
                    turn = 'CPU'
                    break
