from interfaces import *		
import random
import string

class TicTacToeMove(Move): 
	X_POS = 'X Position'
	Y_POS = 'Y Position'
	NAME = 'Name'
	def __init__(self, x_pos, y_pos, name):
		super().__init__(**{
			self.X_POS: x_pos, 
			self.Y_POS: y_pos, 
			self.NAME: name
		})
	def get_x(self): 
		return self.raw()[self.X_POS]
	def get_y(self): 
		return self.raw()[self.Y_POS]
	def get_name(self): 
		return self.raw()[self.NAME]
		
	@classmethod
	def from_raw(cls, m: Move): 
		raw = m.raw()
		return TicTacToeMove(raw[cls.X_POS], raw[cls.Y_POS], raw[cls.NAME])
		
			
class HumanInputPlayer(Player): 
	def __init__(self, name: str):
		self.set_name(name)
	
	def get_move(self) -> Move: 
		_column = self.prompt_user("column")
		_row = self.prompt_user("row")
		return TicTacToeMove(_column, _row, self.get_name())
		
	def prompt_user(self, p: str) -> int: 
		return int(input(f'please insert {p} of type [int]'))

class StupidAI(Player):
	TIC_TAC_TOE_MOVES = { 
		0: (0,0), 1: (0,1), 2: (0,2),
		3: (1,0), 4: (1,1), 5: (1,2),
		6: (2,0), 7: (2,1), 8: (2,2),
	}

	def __init__(self):
		self.set_name(self.__generate_random_name())
		self.__attempted_moves = {}

	def get_move(self) -> Move: 
		col, row = __pick_unique_move()
		return TicTacToeMove(_column, _row, self.get_name())
	
	def __generate_random_name(self): 
		l = string.ascii_lowercase
		result_str = ''.join(random.choice(l) for i in range(10))
		return f'Ai-Player-{result_str}'

	def __get_unique(self): 
		m = random.choice(self.TIC_TAC_TOE_MOVES.keys())
		while m in self.__attempted_moves: 
			m = random.choice(self.TIC_TAC_TOE_MOVES.keys())
		return m 

	def __pick_unique_move(self): 
		m = self.__get_unique()
		self.__attempted_moves[m] = self.TIC_TAC_TOE_MOVES[m]
		return self.TIC_TAC_TOE_MOVES[m]

			
class TicTacToeRuleset(BoardRuleset):
	def __init__(self, board_size): 
		self.__board_size = board_size
		self.__min_row_col = 0
		self.__max_row_col = self.__board_size - 1
		
	def is_legal_move(self, raw: Move) -> bool: 
		'''
			A move is legal if it's in bounds and has a valid name to place
		'''
		_move = TicTacToeMove.from_raw(raw)
		def is_out_of_bounds(to_check): 
			return self.__min_row_col < to_check or to_check > self.__max_row_col 
		if is_out_of_bounds(_move.get_x()): 
			return False 
		if is_out_of_bounds(_move.get_y()): 
			return False 
		return _move.get_name() is not None and len(_move.get_name()) > 0
		
	def display_rules(self)-> bool: 
		return True

		 
				 	 	 
class TicTacToeGB(GameBoard):  
	BOARD_SIZE_OVERRIDE = "Board Size Override"
	BOARD_SIZE_DEFAULT = 3
	EMPTY_CELL_VALUE = "Empty Cell Value"
	EMPTY_CELL_DEFAULT = " "
	SEQUENCE_SEARCH_TOOL = "Sequence Search Tool"
	SEQUENCE_NUM = "Number In A Row" 
	SEQUENCE_NUM_DEFAULT = 3
	
	def __init__(self, *args, **kwargs): 
		self.__board = None
		self.__board_size = kwargs.get(self.BOARD_SIZE_OVERRIDE, self.BOARD_SIZE_DEFAULT)
		self.__empty_cell = kwargs.get(self.EMPTY_CELL_VALUE, self.EMPTY_CELL_DEFAULT)
		self.__board_ruleset = TicTacToeRuleset(board_size=self.__board_size)
		self.__game_completed = False 
		self.__seq_req = kwargs.get(self.SEQUENCE_NUM, self.SEQUENCE_NUM_DEFAULT)
		self.__sequence_searcher = kwargs.get(self.SEQUENCE_SEARCH_TOOL, SequenceSearcher(self.__seq_req))
	
	def initialize(self, *args, **kwargs): 
		self.__board = [[None for j in range(self.__board_size)] for i in range(self.__board_size)]
		return 
		
	def get_board_ruleset(self) -> BoardRuleset: 
		return self.__board_ruleset
	
	def update_board_with_move(self, move: Move) -> MoveResult: 
		# We check again for safety, though canonically not required. 
		assert self.get_board_ruleset().is_legal_move(move), "Illegal moved passed into update_board_with_move"
		
		gbuc = self.__process_move(TicTacToeMove.from_raw(move))
		return self.__update_board_state(gbuc)
		
	def is_game_complete(self): 
		return self._game_completed
		
	def display(self) -> None: 
		def clean_data(inp): 
			return inp if inp is not None else self.__empty_cell
		print_data = [[clean_data(r) for r in row] for row in self.__board]
		print_data = [" | ".join(r) for r in print_data]
		delim = '\n'+('-' * len(max(print_data, key=len)))+'\n'
		print_data = delim.join(print_data)
		print(print_data)
	
	def __is_cell_empty(self, row, column): 
		return self.__board[row][column] != None 
		
	def __apply_move_to_cell(self, row, column, name): 
		self.__board[row][column] = name
	
	def __process_move(self, move: TicTacToeMove) -> MoveResult: 
		res = MoveResult()
		x = move.get_x()
		y = move.get_y()
		if not self._is_cell_empty(y, x): 
			return res
		self._apply_move_to_cell(y, x, move.get_name())
		res.set_move_was_applied()
		return res
		
	def __update_board_state(self, res: MoveResult) -> MoveResult: 
		if not res.was_move_applied(): 
			return res
			
		# Game ends with a winner 
		if self.__sequence_searcher.search(self): 
			self.__game_completed = True 
			res.set_game_has_winner()
			res.set_game_ended_from_move()
			return res
		
		# Game Ends in a Tie 
		if self.__no_moves_left(): 
			self.__game_completed = True 
			res.set_game_ended_from_move()
			return res
		
		# Game has not ended 
		return res


			 				 	
			
def foo(*args, **kwargs): 
	print(kwargs)
	return kwargs
		


if __name__ == "__main__": 
	print("Hello world") 
	print(type(foo(**{"FOOBAR":1, "BARFOO":2})))
	
	b = TicTacToeGB(**{TicTacToeGB.EMPTY_CELL_VALUE:'?'})
	b.initialize()
	b.display()
	