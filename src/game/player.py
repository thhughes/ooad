from abc import ABC, abstractmethod
from gameboard import Move

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
