from abc import ABC, abstractmethod
from typing import List, Optional
from player import Player 
from gameboard import GameBoard, LegalMoveChecker


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
