from typing import Type
from game.move_support import Move, MoveResult, LegalMoveChecker
from .mock import Mockable

class MockMove(Move, Mockable):
	""" Class: Effectively Dictionary Wrapper """ 
	def __init__(self, *args, **kwargs):
		self.__move_contents = kwargs

	def raw(self) -> dict:
		return self.__move_contents

	def add(self, key, val):
		self.__move_contents[key] = val

	@classmethod
	def from_raw(cls, m: Type['Move']):
		pass

class MockMoveResult(MoveResult, Mockable):
	""" 
		Class: Context Object for Post Move Processing communication 
		Intent of this is to avoid passing the board around and instead 
		pass around metatdata about the board 
	"""
	APPLIED="applied", 
	RETRY="retry"
	GAME_ENDED="game_ended"
	HAS_WINNER="has_winner"

	def __init__(self, *args, **kwargs):
		self.__applied = kwargs.get(self.APPLIED, False)
		self.__retry = kwargs.get(self.RETRY, True)
		self.__game_ended_with_move = kwargs.get(self.GAME_ENDED, False)
		self.__game_has_winner = kwargs.get(self.HAS_WINNER, False)

	def was_move_applied(self) -> bool:
		""" 
			Return True if there were no issues and was applied 
		"""
		return self.__applied

	def can_retry(self) -> bool:
		""" 
			Return True if there was an error but can retry. False in all other states 
		"""
		return self.__retry

	def did_move_end_game(self) -> bool:
		""" 
			returns True if game board set this for the game ending from move application. 
		"""
		return self.__game_ended_with_move

	def game_has_winner(self) -> bool:
		""" 
			return True if: Someone has won the game 
			return False if: No valid moves remain OR game is incomplete 
		"""
		return self.__game_has_winner

	def set_move_was_applied(self) -> None:
		self.__applied = True
		self.set_cannot_retry()

	def set_cannot_retry(self) -> None:
		self.__retry = False

	def set_game_ended_from_move(self) -> None:
		self.__game_ended_with_move = True
		self.set_cannot_retry()

	def set_game_has_winner(self) -> None:
		self.__game_has_winner = True


class MockLegalMoveChecker(LegalMoveChecker, Mockable):
	def __init__(self): 
		pass 

	def is_legal_move(self, move: Move) -> bool:
		return True

	def display_rules(self)-> bool:
		return True 


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
