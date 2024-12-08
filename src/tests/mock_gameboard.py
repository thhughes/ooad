from game.gameboard import BoardLocation, GameBoard
from game.move_support import LegalMoveChecker, Move, MoveResult
from mock_move_support import MockLegalMoveChecker, MockMove, MockMoveResult
from typing import Optional, List

class MockBoardLocation(BoardLocation):
	def __init__(self, *args, **kwargs): 
		self._next_coordinates = {}
		self._next_meta = {}
		pass 

	def set_location_contents(self, coordinates, metadata): 
		self._next_coordinates = coordinates
		self._next_meta = metadata

	def get_board_coordinates(self) -> dict:
		return self._next_coordinates

	def get_board_metadata(self) -> dict:
		return self._next_meta

class MockGameBoard(GameBoard):

	def initialize(self, *args, **kwargs):
		self.get_board_ruleset_ret : LegalMoveChecker = kwargs.get('LegalMoveChecker')

	def get_board_ruleset(self) -> LegalMoveChecker:
		return self.get_board_ruleset_ret

	def update_board_with_move(self, move: Move) -> MoveResult:
		"""
			Attempts to update the game board with the new move.
			The move is expected to be Legal, if it's not legal
			an error will occurr. Although the move may be legal,
			the move is not guaranteed to be valid.
			
			A valid move is one that can be made on the board
			(e.g. a piece is not moved to an already occupied location)
			or is deemed invalid due to a given game state
		"""
		pass

	@abstractmethod
	def is_game_complete(self):
		## Could Template Caching
		pass

	@abstractmethod
	def display(self) -> None:
		pass

	@abstractmethod
	def _get_surrounding_locations(self, spot: BoardLocation) -> List[BoardLocation]:
		"""
			Board Searching Method: a list of locations all directly touching the passed in location
		"""
		pass

	@abstractmethod
	def _reset_board_iteration(self) -> None:
		""" Iterator reset """
		pass

	@abstractmethod
	def _next_board_location(self) -> Optional[BoardLocation]:
		""" Iterator Next """
		pass

	def __iter__(self):
		self._reset_board_iteration()
		return self

	def __next__(self) -> Optional[BoardLocation]:
		nxt = self._next_board_location()
		if nxt is None:
			raise StopIteration
		return nxt