#!/usr/bin/env python3

from game.tictactoe import HumanInputPlayer, StupidAI, TicTacToeGB, TicTacToe


if __name__ == "__main__": 
	
	b = TicTacToeGB(**{TicTacToeGB.EMPTY_CELL_VALUE:'?'})
	b.initialize()
	b.display()
	
	runner = TicTacToe([StupidAI(), HumanInputPlayer('Human')], 
						TicTacToeGB())
	runner.setup()
	runner.run()
	runner.display_board()
	print(runner.announce_winner())
	