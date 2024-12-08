#!/usr/bin/env python3


# from game.tictactoe import HumanInputPlayer, StupidAI, TicTacToeGB, TicTacToe


# if __name__ == "__main__": 
	
# 	b = TicTacToeGB(**{TicTacToeGB.EMPTY_CELL_VALUE:'?'})
# 	b.initialize()
# 	b.display()
	
# 	runner = TicTacToe([StupidAI(), HumanInputPlayer('Human')], 
# 						TicTacToeGB())
# 	runner.setup()
# 	runner.run()
# 	runner.display_board()
# 	print(runner.announce_winner())
from tests.mock_move_support import MockLegalMoveChecker	

if __name__ == "__main__": 
	m = MockLegalMoveChecker(True) 
	m.is_legal_move.expect_call(False)
	assert False == m.is_legal_move(), 'Failed Mock test'
	m.check_mock_expectations()
	m.mock_reset()
	m.is_legal_move.ignore_calls()
	assert m.is_legal_move(), 'Failed default return test' 
	m.check_mock_expectations()
	m.mock_reset()
