from engine.holic_engine import GameEngine


if __name__ == '__main__':
    turn = 'CPU'
    game = GameEngine()
    while True:
        if turn == 'CPU':
            mov = game.select_move(4)
            print(mov)
            game.board.push(mov)
            turn = 'Human'
        else:
            print(game.board)
            while True:
                try:
                    valid_move = input('Enter Move:')
                    mov = game.board.push_san(valid_move)
                except Exception as e:
                    print('Invalid move')
                else:
                    turn = 'CPU'
                    break
