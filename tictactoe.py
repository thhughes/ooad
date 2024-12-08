from abc import ABC, abstractmethod
from typing import Dict, Optional, List

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
    def set_move_validator(self, v: MoveValidator) -> None: 
        pass 

    @abstractmethod 
    def get_name(self) -> str: 
        pass

    @abstractmethod 
    def get_move(self) -> Dict: 
        pass 

class Game(ABC): 
    
    @abstractmethod
    def __init__(self, players: List[Player], mv: MoveValidator, tenacity: int): 
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
    def display_board(self) -> None: 
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

class GameBoard(ABC): 

    @abstractmethod
    def is_move_available(self, move: Dict) -> bool: 
        pass 

    @abstractmethod 
    def update_with_move(self, move: Dict) -> None: 
        pass 

    @abstractmethod 
    def has_winner(self) -> bool: 
        pass 

    @abstractmethod
    def printable(self) -> str: 
        pass 

    ## Future 
    # @abstractmethod
    # def set_board_validator(self, v: BoardValidator) -> None: 
    #     pass 

##
## Implementations 
##
class TicTacToe(Game): 
    ROW_KEY = 'Row'
    COL_KEY = 'Column'
    TEAM_KEY = 'Team'
    TEAM_X = 'X'
    TEAM_O = 'O'
    BAD_PLAYER = 'Bad Player' 

    def __init__(self, tenacity: int): 
        self.players: List[Player] = []
        self.board: GameBoard = None

        self.tenacity: int  = tenacity
        self.game_completed : bool = False 
        self.winner : Optional[Player] = None
        self.is_draw = False 
        self.is_forfeit = False 
        self.round_number = 0

    def set_players(self, players: List[Player]): 
        assert len(players) == 2, f"Illegal number of players, got [{len(players)}], expected 2"
        self.players = players
    
    def set_board(self, b: GameBoard): 
        self.board = b

    def share_rules(self) -> str: 
        return 'String of rules, whatever you want them to be'

    def is_completed(self) -> bool: 
        return self.game_completed
 
    def _get_next_move(self, p: Player) -> Dict: 
        for i in range(self.tenacity): 
            move = p.get_move()
            if {} == move: 
                continue 
            if self.TEAM_KEY not in move: 
                print("Illegal Move - No Team Key")
                continue 
            if move[self.TEAM_KEY] not in [self.TEAM_X, self.TEAM_O]: 
                print("Illegal Move - Invalid Team Key")
                continue 
            return move
        return {self.BAD_PLAYER: p}
            
    def display_board(self) -> None: 
        print(self.board.printable())


    def progress_turn(self) -> None: 
        if self.is_completed(): 
            return 

        turn_player = self._get_next_player()
        for i in range(self.tenacity): 
            next_move = self._get_next_move(turn_player)
            if self.BAD_PLAYER in next_move: 
                self._set_game_over_for(turn_player)
                return 

            if self.board.is_move_available(next_move):
                self.board.update_with_move(next_move)
                self.winner = turn_player if self.has_winner() else None
                self.game_completed = self.winner is not None
                self.round_number = self.round_number + 1 
                return 

        self._set_game_over_for(turn_player)
        return 



    def _set_game_over_for(self, p: Player): 
        self.is_forfeit = True
        self.game_completed = True 
        self.winner = player[0] if self.players[0].get_name() == p.get_name() else self.players[1]

    def _get_next_player(self):  
        return self.players[self.round_number%2]

    def has_winner(self) -> bool: 
        return self.winner is not None 

    def get_winner(self) -> Player:
        return self.winner 

    def get_result(self) -> str: 
        if not self.game_completed: 
            return '' 

        if not self.has_winner(): 
            return 'Cats Game'

        win_reason = ''
        if self.is_forfeit: 
            win_reason = 'Due to forfeit of other player, '

        return f"{win_reason}{self.winner.get_name()} Wins!"
        
class TicTacToeBoard(GameBoard): 
    EMPTY = None
    EMPTY_ROW = [None, None, None]
    def __init__(self): 
        self._board = [ 
            [None, None, None], 
            [None, None, None], 
            [None, None, None]
        ]
        self.draw = False 
    def _row_col_from_move(self, move: Dict) -> (int,int): 
        r = move[TicTacToe.ROW_KEY]
        c = move[TicTacToe.COL_KEY]
        return r, c

    def is_move_available(self, move: Dict) -> bool: 
        r, c = self._row_col_from_move(move)
        assert r <= len(self._board)
        assert c <= len(self._board[0])
        return self._board[r][c] is None

    def update_with_move(self, move: Dict) -> None: 
        r, c = self._row_col_from_move(move)
        self._board[r][c] = move[TicTacToe.TEAM_KEY]

    def has_winner(self) -> bool: 
        # Check rows
        for row in self._board:
            if row[0] == row[1] == row[2] != self.EMPTY:
                return True 
        
        # Check columns
        for col in range(3):
            if self._board[0][col] == self._board[1][col] == self._board[2][col] != self.EMPTY:
                return True 
        
        # Check diagonals
        if self._board[0][0] == self._board[1][1] == self._board[2][2] != self.EMPTY:
            return True
        if self._board[0][2] == self._board[1][1] == self._board[2][0] != self.EMPTY:
            return True 
        
        complete_board = all( [
            [all(item is not None for item in self._board[0])], 
            [all(item is not None for item in self._board[1])], 
            [all(item is not None for item in self._board[2])]
        ] )
        self.draw = complete_board
        return False

    def is_tie(self) -> bool: 
        return self.draw

    def printable(self) -> str: 
        print(self._board)
        print_list = []
        for r in self._board: 
            safe_row = [v if v is not None else ' ' for v in r]
            print_list.append("|".join(safe_row))
            print_list.append("\n")
            print_list.append("-"*len("|".join(safe_row)))
            print_list.append("\n")

        return ''.join(print_list[:-2])
        

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
    _INVALID_ENTRY = 'Entry is Invalid'

    def __init__(self): 
        self.validity_reason = self._UNSET

    def _move_contains_proper_keys(self, move_context: Dict) -> bool:
        if TicTacToe.ROW_KEY not in move_context: 
            return False 
        if TicTacToe.COL_KEY not in move_context: 
            return False 
        if TicTacToe.TEAM_KEY not in move_context: 
            return False 
        return True 

    def _row_is_valid(self, move_context: Dict) -> bool:
        r = int(move_context[TicTacToe.ROW_KEY])
        return r >= self.ROW_MIN and r <= self.ROW_MAX

    def _col_is_valid(self, move_context: Dict) -> bool:
        r = int(move_context[TicTacToe.ROW_KEY])
        return r >= self.COL_MIN and r <= self.COL_MAX

    def _value_is_valid(self, move_context: Dict) -> bool: 
        return move_context[TicTacToe.TEAM_KEY] in [TicTacToe.TEAM_X, TicTacToe.TEAM_O]

    def reset(self): 
        self.validity_reason = self._UNSET 

    def is_valid_move(self, move_context: Dict): 
        if not self._move_contains_proper_keys(move_context): 
            self.validity_reason = self._MISSING_KEYS
            return False 
        if not self._row_is_valid(move_context): 
            self.validity_reason = self._INVALID_ROW
            return False 
        if not self._col_is_valid(move_context): 
            self.validity_reason = self._INVALID_COL
            return False 
        if not self._value_is_valid(move_context): 
            self.validity_reason = self._INVALID_ENTRY
            return False

        self._validity_reason = self._IS_VALID
        return True 

    def why_invalid(self): 
        return self._validity_reason 
        

class HumanTicTacToe(Player):
    def __init__(self, name: str, player_key: str): 
        self.validator = None 
        self.name = name
        assert player_key in [TicTacToe.TEAM_X, TicTacToe.TEAM_O], f"Illegal Player Key {player_key}"
        self.player_key = player_key

    def set_move_validator(self, v: MoveValidator): 
        self.validator = v

    def get_name(self) -> str: 
        return self.name

    def get_move(self) -> Dict: 
        move = self._query_move()
        if not self.validator.is_valid_move(move): 
            print(f"Invalid Input - [{self.validator.why_invalid()}]")
            return {}
        return move       

    def _query_move(self) -> Dict: 
        row = input(f'{self.name} - input Row of Move') 
        col = input(f'{self.name} - input Column of Move')
        return {
            TicTacToe.ROW_KEY: int(row), 
            TicTacToe.COL_KEY: int(col), 
            TicTacToe.TEAM_KEY: self.player_key
        }


if __name__ == "__main__": 

    players = [ 
        HumanTicTacToe('Ham', TicTacToe.TEAM_X), 
        HumanTicTacToe('Beans', TicTacToe.TEAM_O)
    ]
    for p in players: 
        p.set_move_validator(TicTacToeMoveValidator())

    game = TicTacToe(5)
    game.set_players(players)
    game.set_board(TicTacToeBoard())
    # game.set_move_validator(TicTacToeMoveValidator())

    game.share_rules()
    while not game.is_completed(): 
        game.progress_turn()
        game.display_board()

    if game.has_winner(): 
        print(f'Winner: {game.get_winner()}')
    else: 
        print(f'Game Is Draw: {game.get_result()}')
