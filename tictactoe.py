from abc import ABC, abstractmethod
from typing import Dict, Optional

##
## Interfaces 
##
class MoveValidator(ABC): 
    @abstractmethod 
    def is_valid_move(self, move_context: Dict) -> bool: 
        pass 

    @abstractmethod 
    def why_invalid() -> str: 
        pass 

    @abstractmethod 
    def reset() -> None: 
        pass 

class Player(ABC):  
    @abstractmethod 
    def __init__(self, name: str, v: MoveValidator): 
        pass 

    @abstractmethod 
    def get_name(self) -> str: 
        pass

    @abstractmethod 
    def get_move(self) -> Dict: 
        pass 

class Game(ABC): 
    
    @abstractmethod
    def __init__(self, players: List[Player], tenacity: int): 
        pass 

    @abstractmethod 
    def share_rules(self) -> str: 
        pass 

    @abstractmethod 
    def is_completed(self) -> bool: 
        pass 

    @abstractmethod 
    def progress_turn(self) -> None: 
        pass 

    @abstractmethod 
    def has_winner(self) -> bool: 
        pass 

    @abstractmethod
    def get_winner(self) -> Player:
        pass 

    @abstractmethod 
    def get_result(self) -> str: 
        pass 

##
## Implementations 
##
class TicTacToe(Game): 
    ROW_KEY = 'Row'
    COL_KEY = 'Column'

    def __init__(self, players: List[Player], tenacity: int): 
        assert len(players) == 2, 'Must have 2 players to play this game'
        self.players: List[Player] = players 
        self.tenacity: int  = tenacity
        self.game_completed : bool= False 
        self.winner : Optional[Player]= None
        self.is_draw = False 

    def share_rules(self) -> str: 
        return 'String of rules, whatever you want them to be'

    def is_completed(self) -> bool: 
        return self.game_completed
 
    def progress_turn(self) -> None: 
        if self.is_completed(): 
            return 

        next_player = self._get_next_player()
        move = self._get_valid_move()
        if move is None: 
            self.game_completed = True 
            self.winner = None 
            raise RuntimeError(f'Player {next_player.get_name()} has failed to provide a valid move. Reached max attempts')
        self._update_game_board(move) 
        self._update_game_status()

    def _update_game_board(self, move: Dict): 
        ## Insert the move onto the board 
        pass 

    def _update_game_status(self): 
        ## Check for a winner 
        pass 

    def _get_next_player(self):       
        next_player = self.players[0]
        self.players = self.players[1:]
        self.players.append(next_player)
        return self.players[-1]

    def has_winner(self) -> bool: 
        return self.winner is not None 

    def get_winner(self) -> Player:
        return self.winner 

    def get_result(self) -> str: 
        if not self.game_completed: 
            return '' 

        if not self.has_winner(): 
            return 'Cats Game'
        
        return f"{self.winner.get_name()} Wins!"
        



class TicTacToeMoveValidator(MoveValidator): 
    ROW_MIN = 0
    ROW_MAX = 2
    COL_MIN = 0
    COL_MAX = 2

    ## Validity Reasons
    _UNSET = '' 
    _IS_VALID = 'Move Is Valid' 
    _INVALID_ROW = 'Row Entry is Invalid'
    _INVALID_COL = 'Column Entry is Invalid'
    _MISSING_KEYS = 'Missing Row or Column Key'

    def __init__(self): 
        self.validity_reason = UNSET

    def _move_contains_proper_keys(self, move_context: Dict) -> bool
        if TicTacToe.ROW_KEY not in move_context: 
            return False 
        if TicTacToe.COL_KEY not in move_context: 
            return False 
        return True 

    def _row_is_valid(self, move_context: Dict) -> bool 
        r = int(move_context[TicTacToe.ROW_KEY])
        return r >= ROW_MIN and r <= ROW_MAX

    def _col_is_valid(self, move_context: Dict) -> bool 
        r = int(move_context[TicTacToe.ROW_KEY])
        return r >= ROW_MIN and r <= ROW_MAX

    def reset(self): 
        self.validity_reason = self._UNSET 

    def is_valid_move(self, move_context: Dict): 
        if not _move_contains_proper_keys(move_context): 
            self.validity_reason = self._MISSING_KEYS
            return False 
        if not _row_is_valid(move_context): 
            self.validity_reason = self._INVALID_ROW
            return False 
        if not _col_is_valid(move_context): 
            self.validity_reason = self._INVALID_COL
            return False 

        self._validity_reason = self._IS_VALID
        return True 
        

class HumanTicTacToe(Player): 
    def __init__(self, name: str, v: MoveValidator): 
        self.validator = v 
        self.name = name

    def get_name(self) -> str: 
        return self.name

    def get_move(self) -> Dict: 
        move = self._query_move()
        if not self.validator.is_valid_move(move): 
            return {}
        return move       

    def _query_move(self) -> Dict: 
        row = input(f'{self.name} - input Row of Move') 
        col = input(f'{self.name} - input Column of Move')
        return {
            TicTacToe.ROW_KEY: int(row), 
            TicTacToe.COL_KEY: int(col)
        }



        




if __name__ == "__main__": 

    players = [ 
        HumanTicTacToe('Ham', TicTacToeMoveValidator()), 
        HumanTicTacToe('Beans', TicTacToeMoveValidator())
    ]

    game = TicTacToe(players, 5)

    game.share_rules()
    while not game.is_completed(): 
        game.progress_turn()

    if game.has_winner(): 
        print(f'Winner: {game.get_winner()}')
    else: 
        print(f'Game Is Draw: {game.get_result()}')
