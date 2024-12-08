from abc import ABC, abstractmethod
from typing import List, Type, Optional



class Move(ABC):
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

class MoveResult(ABC):
	""" 
		Class: Context Object for Post Move Processing communication 
		Intent of this is to avoid passing the board around and instead 
		pass around metatdata about the board 
	"""
	def __init__(self, *args, **kwargs):
		self.__applied = False
		self.__retry = True
		self.__game_ended_with_move = False
		self.__game_has_winner = False

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

class Player(ABC):
	NAME='NAME'
	NAME_DEFAULT=None
	def __init__(self, *args, **kwargs):
		self.__name = kwargs.get('name', None)

	def get_name(self) -> str:
		return self.__name
	
	def initialize(self) -> None:
		return None

	@abstractmethod
	def get_move(self) -> Move:
		pass

class LegalMoveChecker(ABC):

	@abstractmethod
	def is_legal_move(self, move: Move) -> bool:
		pass

	@abstractmethod
	def display_rules(self)-> bool:
		pass

class BoardLocation(ABC):

	@abstractmethod
	def get_board_coordinates(self) -> dict:
		pass

	@abstractmethod
	def get_board_metadata(self) -> dict:
		pass

class GameBoard(ABC):

	@abstractmethod
	def initialize(self, *args, **kwargs):
		pass

	@abstractmethod
	def get_board_ruleset(self) -> LegalMoveChecker:
		pass

	@abstractmethod
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

class SequenceSearcher(ABC):
	SEARCH_HORIZONTAL = "Search Horizontals"
	SEARCH_VERTICALS = "Search Verticals"
	SEARCH_DIAGONALS = "Search Diagonals"

	def __init__(self, num_in_sequence: int, horizontal: bool = True, 
			  vertical: bool = True, diag: bool = True):
		self.__seq_num: int = num_in_sequence
		self.__search_dir = { 
			self.SEARCH_HORIZONTAL: horizontal, 
			self.SEARCH_VERTICALS: vertical, 
			self.SEARCH_DIAGONALS: diag
		}

	def sequence_size(self):
		return self.__seq_num

	def no_search(self, starting_spot, gb: GameBoard, sqs: int) -> bool:
		pass

	def search_h(self, starting_spot, gb: GameBoard, sqs: int) -> bool:
		pass

	def search_v(self, starting_spot, gb: GameBoard, sqs: int) -> bool:
		pass

	def search_d(self, starting_spot, gb: GameBoard, sqs: int) -> bool:
		pass

	def search(self, gb: GameBoard) -> bool:
		for spot in gb:
			for _, search_method in self.__search_dir.items():
				if search_method(spot, gb, self.sequence_size()):
					return True
		return False


class GameRunner(ABC):
	STARTING_TURN = 'Starting Turn'
	STARTING_TURN_DEFAULT = 0

	DISPLAY_BOARD = 'Display Board'
	DISPLAY_BOARD_EACH_TURN = 0
	DISPLAY_BOARD_NEVER = 1

	GAME_NAME = 'Game Name'
	GAME_NAME_DEFAULT = 'Unset' 

	def __init__(self, players: List[Player], game_boad: GameBoard, **kwargs):
		self.__players = players
		self.__game_board = game_boad
		self.__game_completed = False
		self.__winner = None
		self.__game_name = kwargs.get(self.GAME_NAME, self.GAME_NAME_DEFAULT)

	@abstractmethod
	def _update_game_state(self, p: Player) -> None:
		""" 
			p: Player who just completed their turn 
			
			Utilizes game board, ruleset, and any other information required 
			to update local state. 
			
			Expected: 
				Set self._game_completed => True if the game is over 
				Set self._winner => inputted Player if that player just made a move that won them the game. 
		"""
		pass

	def get_winner(self) -> Optional[Player]:
		return self.__winner

	def is_tie(self) -> bool:
		return self.is_game_finished() and (None is self.get_winner())

	def is_game_finished(self) -> bool:
		"""
			return True if the game is over 
		"""
		return self.__game_completed

	def get_players(self) -> List[Player]:
		"""
			Gets a list of players where the order is the turn order for a given round.  
		"""
		return self.__players

	def get_game_board(self) -> GameBoard:
		""" 
			Returns the game board of the game in progress
		"""
		return self.__game_board
	
	def game_name(self) -> str: 
		return self.__game_name

	def display_board(self) -> None:
		self.get_game_board().display()

	def announce_winner(self) -> str:
		if self.is_tie():
			return " ".join([
				self.game_name(), 
				"has resulted in a tie between:", 
				", ".join(self.get_players())
			])
		return " ".join([ 
			self.game_name(), 
			"has resulted in", 
			self.get_winner().name(),
			"winning!"
			])

	@abstractmethod
	def debug_log(self, *args, **kwargs):
		"""
			Advanced choice, using a debug log method rather than just print. There are a bunch of different 
			Logging utillities available to you in python but depending on the setup, this might be 
			The better choice. It's important to think about the use case and decide what 
			works best for you in your project. Don't overthink it though "it doesn't matter" is a 
			fair conclusion. 
		"""
		return

	@abstractmethod
	def get_legal_move_tenacity(self) -> int:
		"""
			Returns the number of attempts a player gets to provide a legal move 
			Default: Return 1
			
			Other games have the choice of overloading 
		"""
		return 1

	@abstractmethod
	def get_move_tenacity(self) -> int:
		""" 
			Different from "Legal_move_tenacity" this is about not using moves 
			that have already been used or that an attentive player would know is not allowed 
			due to game state. 
			Default: Return 2
			
			Other games have the choice of overloading. 
		"""
		return 2

	@abstractmethod
	def __get_next_player_given(self, turn: int) -> tuple[Player, int]: 
		""" 
			Naieve implementation of turn number as an int. a Turn is considered 1 player making a play. 
			Therefore if there were 5 players in a game, each player would get a turn and then the 1st player 
			would go again which would be the 6th turn. 
			return (Player for this turn, next turn number)
		"""
		if self.is_game_finished():
			return (None, turn)
		return (self.get_players()[turn % len(self.get_players())], turn + 1)

	def __pick_legal_move(self, gb: GameBoard, rs: LegalMoveChecker, p: Player):
		for _ in range(self.get_legal_move_tenacity()):
			turn_move = p.get_move()
			if rs.is_legal_move(turn_move):
				return (True, turn_move)
		return (False, None)

	def progress_turn(self, player):
		game_board = self.get_game_board()
		rules = game_board.get_board_ruleset()
		has_legal_move, turn_move = self.__pick_legal_move(game_board, rules, player)
		if not has_legal_move:
			# Illegal moves do not contribute to non-applicable 
			# moves. Being illegal too many times is a game over. 
			return False
		update_ctxt = game_board.update_board_with_move(turn_move)
		if not update_ctxt.was_move_applied():
			return False
		if update_ctxt.did_move_end_game():
			self.__game_completed = True
		return True

	def setup(self, *args, **kwargs) -> None:
		for player in self.get_players():
			player.initialize()
		self.get_game_board().initialize()

	def run(self, *args, **kwargs) -> None:
		
		turn = kwargs.get(self.STARTING_TURN, self.STARTING_TURN_DEFAULT)
		display_board = kwargs.get(self.DISPLAY_BOARD, self.DISPLAY_BOARD_EACH_TURN)
		
		next_player, turn = self.__get_next_player_given(turn)
		while None is not next_player:
			if not self.progress_turn(next_player):
				raise RuntimeError("Could not progress turn")
			self._update_game_state(next_player)
			if display_board == self.DISPLAY_BOARD_EACH_TURN:
				self.display_board()
			next_player, turn = self.__get_next_player_given(turn)

		if display_board != self.DISPLAY_BOARD_NEVER:
			self.display_board()
