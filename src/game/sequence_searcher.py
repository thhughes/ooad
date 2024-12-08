from abc import ABC, abstractmethod
from .interfaces import GameBoard, BoardLocation

class SequenceSearchInterface(ABC): 

	@abstractmethod
	def sequence_size(self): 
		raise NotImplementedError()

	# Search Configs 
	SEARCH_GAME_BOARD = "GameBoard"
	SEARCH_START_LOCATION = "StartLocation"

	@abstractmethod
	def search(self, *args, **kwargs) -> bool:
		raise NotImplementedError()


class SequenceSearcher(SequenceSearchInterface):
	# Settings 
	SETTING_HORIZONTAL = "Search Horizontals"
	SETTING_HORIZONTAL_DEFAULT = True 
	
	SETTING_VERTICALS = "Search Verticals"
	SETTING_VERTICALS_DEFAULT = True 
	
	SETTING_DIAGONALS = "Search Diagonals"
	SETTING_DIAGONALS_DEFAULT = True 

	LOCAL_SEARCH_ONLY = "Local Search Only" 
	LOCAL_SEARCH_ONLY_DEFAULT = False 
    

	def __init__(self, num_in_sequence: int, **kwargs):
		self.__search_horizontal = kwargs.get(self.SETTING_HORIZONTAL, 
											  self.SETTING_HORIZONTAL_DEFAULT)
		self.__search_vertical   = kwargs.get(self.SETTING_VERTICALS, 
											  self.SETTING_VERTICALS_DEFAULT)
		self.__search_diagonal   = kwargs.get(self.SETTING_DIAGONALS, 
											  self.SETTING_DIAGONALS_DEFAULT)
		self.__local_search = kwargs.get(self.LOCAL_SEARCH_ONLY, 
								        self.LOCAL_SEARCH_ONLY_DEFAULT)
		
		self.__seq_num: int = num_in_sequence
		
		self.__search_dir = { 
			self.SETTING_HORIZONTAL: 
			    self._search_h if self.__search_horizontal else self.no_search, 
			self.SETTING_VERTICALS:  
			    self._search_v if self.__search_vertical  else self.no_search, 
			self.SETTING_DIAGONALS:  
			    self._search_d if self.__search_diagonal else self.no_search
		}

	def sequence_size(self):
		return self.__seq_num

	def _no_search(self, starting_spot: BoardLocation, gb: GameBoard, sqs: int) -> bool:
		""" Search Method: 
            /param: starting_spot - the location to start a search 
			/param: gb - the gameboard to search 
			/param: sqs - the number of spaces to check. 
			
			/return: False always
		"""
		return False 

	def _search_h(self, starting_spot: BoardLocation, gb: GameBoard, sqs: int) -> bool:
		""" Search Method: Look for a horizontal sequence 
            /param: starting_spot - the location to start a search 
			/param: gb - the gameboard to search 
			/param: sqs - the number of spaces to check. 
			
			/return: True if there is a sequence sqs long along a horizontal 
		"""
		pass

	def _search_v(self, starting_spot: BoardLocation, gb: GameBoard, sqs: int) -> bool:
		""" Search Method: Look for a vertical sequence 
            /param: starting_spot - the location to start a search 
			/param: gb - the gameboard to search 
			/param: sqs - the number of spaces to check. 
			
			/return: True if there is a sequence sqs long along a vertical 
		"""
		pass

	def _search_d(self, starting_spot: BoardLocation, gb: GameBoard, sqs: int) -> bool:
		""" Search Method: Look for a diagonal sequence 
            /param: starting_spot - the location to start a search 
			/param: gb - the gameboard to search 
			/param: sqs - the number of spaces to check. 
			
			/return: True if there is a sequence sqs long along a diagonal 
		"""
		pass
	
	def search(self, *args, **kwargs) -> bool:
		if self.__local_search: 
			return self._full_search(*args, **kwargs)
		
		return self._spot_search(*args, **kwargs)
	
	def _full_search(self, *args, **kwargs) -> bool: 
		gb = kwargs.get(self.SEARCH_GAME_BOARD)
		for spot in gb:
			for _, search_method in self.__search_dir.items():
				if search_method(spot, gb, self.sequence_size()):
					return True
		return False
	
	def _spot_search(self, *args, **kwargs) -> bool: 
		gb = kwargs.get(self.SEARCH_GAME_BOARD)
		start = kwargs.get(self.SEARCH_START_LOCATION, None)
		if start is None: 
			return self._full_search(*args, **kwargs)

		raise NotImplementedError('Local Only Search not currently supported')