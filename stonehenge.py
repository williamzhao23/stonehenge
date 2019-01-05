"""
Game and GameState classes and helper functions for the game Stonehenge.
"""
from typing import List, Dict
from game import Game
from game_state import GameState


def create_ley_dl(board_size: int) -> List[List[int]]:
    """
    Return ley_lines along the down-left diagonals given a board_size of
    Stonehenge.

    >>> create_ley_dl(1)
    [[0], [1, 2]]
    >>> create_ley_dl(4)
    [[0, 2, 5, 9], [1, 3, 6, 10, 14], [4, 7, 11, 15], [8, 12, 16], [13, 17]]
    """
    # Generate first diagonal
    ley_dl = [[0]]
    start = 0
    for n in range(2, board_size + 1):
        ley_dl[0].append(start + n)
        start += n
    # Generate heads of other diagonals
    ley_dl.append([1])
    start = 1
    for n in range(3, board_size + 2):
        ley_dl.append([start + n])
        start += n
    # Fill in other diagonals
    for n in range(1, board_size):
        start = ley_dl[n][0]
        for i in range(n + 1, board_size + 1):
            ley_dl[n].append(start + i)
            start += i
        ley_dl[n].append(start + board_size)
    ley_dl[-1].append(ley_dl[-1][0] + board_size)
    return ley_dl


def create_ley_dr(board_size: int) -> List[List[int]]:
    """
    Return ley-lines along the down-right diagonals given a board_size of
    Stonehenge.

    >>> create_ley_dr(1)
    [[1], [0, 2]]
    >>> create_ley_dr(4)
    [[1, 4, 8, 13], [0, 3, 7, 12, 17], [2, 6, 11, 16], [5, 10, 15], [9, 14]]
    """
    # Generate first diagonal
    ley_dr = [[1]]
    start = 1
    for n in range(3, board_size + 2):
        ley_dr[0].append(start + n)
        start += n
    # Generate heads of other diagonals
    ley_dr.append([0])
    start = 0
    for n in range(2, board_size + 1):
        ley_dr.append([start + n])
        start += n
    # Fill in other diagonals
    for n in range(1, board_size):
        start = ley_dr[n][0]
        for i in range(n + 2, board_size + 2):
            ley_dr[n].append(start + i)
            start += i
        ley_dr[n].append(start + board_size + 1)
    ley_dr[-1].append(ley_dr[-1][0] + board_size + 1)
    return ley_dr


def create_ley_row(board_size: int) -> List[List[int]]:
    """
    Return ley-lines along the horizontal rows given a board_size of
    Stonehenge.

    >>> create_ley_row(1)
    [[0, 1], [2]]
    >>> create_ley_row(3)
    [[0, 1], [2, 3, 4], [5, 6, 7, 8], [9, 10, 11]]
    """
    ley_row = []
    start = 0
    for n in range(2, board_size + 2):
        ley_row.append([n for n in range(start, start + n)])
        start += n
    ley_row.append([n for n in range(start, start + board_size)])
    return ley_row


def create_markers(line: List[List[str]], state: Dict[str, int]) -> List[str]:
    """
    Return a list of strings to mark the status of ley-lines given a ley-line,
    line, and the current state of the cells of the board, state.

    >>> create_markers([['A'], ['B', 'C']], {'A': 0, 'B': 0, 'C': 0})
    ['@', '@']
    >>> create_markers([['A', 'B'], ['C']], {'A': 1, 'B': 0, 'C': 2})
    ['1', '2']
    """
    markers = []
    for list_ in line:
        cell1 = 0
        cell2 = 0
        for cell in list_:
            if state[cell] == 1:
                cell1 += 1
            elif state[cell] == 2:
                cell2 += 1
        if cell1/len(list_) >= 0.5:
            markers.append('1')
        elif cell2/len(list_) >= 0.5:
            markers.append('2')
        else:
            markers.append('@')
    return markers


def create_cells(rows: List[List[str]],
                 state: Dict[str, int]) -> List[List[str]]:
    """
    Return a list of strings to represent taken and untaken cells given the
    rows of the game board and the state of the game.

    >>> create_cells([['A', 'B'], ['C']], {'A': 0, 'B': 0, 'C': 0})
    [['A', 'B'], ['C']]
    >>> create_cells([['A', 'B'], ['C']], {'A': 1, 'B': 2, 'C': 0})
    [['1', '2'], ['C']]
    """
    return [[x if state[x] == 0 else str(state[x]) for x in l] for l in rows]


def is_winner(state: 'StonehengeState', player: int) -> bool:
    """
    Return true if and only if player, 1 or 2, would have won a
    Stonehenge game with the current state.

    >>> is_winner(StonehengeState(True, 1).make_move('A'), 1)
    True
    >>> is_winner(StonehengeState(False, 1).make_move('A'), 1)
    False
    >>> is_winner(StonehengeState(True, 1).make_move('A'), 2)
    False
    """
    lines = sum([state.mark_dl, state.mark_dr, state.mark_row], [])
    num = sum([1 for x in lines if x == str(player)])
    return num / len(lines) >= 0.5


class StonehengeState(GameState):
    """
    The state of the game Stonehenge at a specific point.

    ley - ley-lines along the down-left diagonals, down-right diagonals, and
          horizontal rows
    mark_dl - markers for down-left ley-lines
    mark_dr - markers for down-right ley-lines
    mark_row - markers for horizontal ley-lines
    cell_state - current state of cells on board
    """
    ley: List[List[List[str]]]
    mark_dl: List[str]
    mark_dr: List[str]
    mark_row: List[str]
    cell_state: Dict[str, int]

    CELLS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def __init__(self, is_p1_turn: bool, board_size: int) -> None:
        """
        Initialize a game state for Stonehenge with size board_size and
        current player based on is_p1_turn. Overrides GameState.__init__

        >>> state = StonehengeState(True, 1)
        >>> state.p1_turn is True
        True
        >>> state.ley
        [[['A'], ['B', 'C']], [['B'], ['A', 'C']], [['A', 'B'], ['C']]]
        >>> state.mark_dl
        ['@', '@']
        >>> state.cell_state
        {'A': 0, 'B': 0, 'C': 0}
        """
        self.p1_turn = is_p1_turn
        # Create cells on board
        num_cells = sum(range(3, 3 + board_size))
        used_cells = StonehengeState.CELLS[:num_cells]
        self.cell_state = {x: 0 for x in used_cells}
        # Create ley-lines
        ley_dl, ley_dr, ley_row = [], [], []
        index_dl = create_ley_dl(board_size)
        index_dr = create_ley_dr(board_size)
        index_row = create_ley_row(board_size)
        for list_ in index_dl:
            ley_dl.append([StonehengeState.CELLS[x] for x in list_])
        for list_ in index_dr:
            ley_dr.append([StonehengeState.CELLS[x] for x in list_])
        for list_ in index_row:
            ley_row.append([StonehengeState.CELLS[x] for x in list_])
        self.ley = [ley_dl, ley_dr, ley_row]
        self.mark_dl = create_markers(ley_dl, self.cell_state)
        self.mark_dr = create_markers(ley_dr, self.cell_state)
        self.mark_row = create_markers(ley_row, self.cell_state)

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game,
        Stonehenge. Overrides GameState.__str__

        >>> print(StonehengeState(True, 1))
              @   @
             /   /
        @ - A - B
             \\ / \\
          @ - C   @
               \\
                @
        """
        # Create markers and modifier based on board size.
        dl, dr, row = self.mark_dl, self.mark_dr, self.mark_row
        cells = create_cells(self.ley[2], self.cell_state)
        mod = len(self.ley[0])
        # Create blocks of the board block by block
        starter = '      ' + '  ' * (mod - 2) +\
                  '{}   {}\n'.format(dl[0], dl[1]) + '     ' +\
                  '  ' * (mod - 2) + '/   /\n'
        mid1 = ''
        for i in range(mod - 2):
            mid1 += '  ' * (mod - 2 - i) + row[i] +\
                   (' - {}' * (2 + i)).format(*cells[i]) + '   ' +\
                   dl[2 + i] + '\n' + '     ' + '  ' * (mod - 3 - i) +\
                   '/ \\ ' * len(cells[i]) + '/\n'
        mid2 = row[mod - 2] + (' - {}' * mod).format(*cells[-2]) + '\n' +\
            '     ' + '\\ / ' * (mod - 1) + '\\' + '\n'
        mid3 = '  ' + row[-1] + (' - {}' * (mod - 1)).format(*cells[-1]) +\
               '   {}'.format(dr[0]) + '\n'
        dr = dr[1:]
        dr.reverse()
        end = '    ' + '   \\' * (mod - 1) + '\n' + '     ' +\
              ('   {}' * (mod - 1)).format(*dr)
        return starter + mid1 + mid2 + mid3 + end

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves that can be applied to this state. Overrides
        GameState.get_possible_moves

        >>> StonehengeState(True, 1).get_possible_moves()
        ['A', 'B', 'C']
        >>> StonehengeState(True, 3).get_possible_moves()
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        """
        if not is_winner(self, 1) and not is_winner(self, 2):
            moves = []
            for key in self.cell_state:
                if self.cell_state[key] == 0:
                    moves.append(key)
            return moves
        return []

    def make_move(self, move: str) -> 'StonehengeState':
        """
        Return the StonehengeState that results from applying move to this
        StonehengeState. Overrides GameState.make_move

        >>> state1 = StonehengeState(True, 2)
        >>> state1.p1_turn
        True
        >>> state1.cell_state
        {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0}
        >>> state1.get_possible_moves()
        ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        >>> state2 = state1.make_move('A')
        >>> state2.p1_turn
        False
        >>> state2.cell_state
        {'A': 1, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0}
        >>> state2.get_possible_moves()
        ['B', 'C', 'D', 'E', 'F', 'G']
        >>> state1.p1_turn
        True
        """
        new_state = StonehengeState(not self.p1_turn, len(self.mark_dl) - 1)
        new_state.cell_state = self.cell_state.copy()
        new_state.cell_state[move] = 1 if self.p1_turn else 2
        old_dl, old_dr, old_row = self.mark_dl.copy(), self.mark_dr.copy(),\
            self.mark_row.copy()
        new_dl = create_markers(self.ley[0], new_state.cell_state)
        new_dr = create_markers(self.ley[1], new_state.cell_state)
        new_row = create_markers(self.ley[2], new_state.cell_state)
        new_state.mark_dl = [old_dl[i] if old_dl[i] != '@' else new_dl[i] for
                             i in range(len(old_dl))]
        new_state.mark_dr = [old_dr[i] if old_dr[i] != '@' else new_dr[i] for
                             i in range(len(old_dr))]
        new_state.mark_row = [old_row[i] if old_row[i] != '@' else new_row[i]
                              for i in range(len(old_row))]
        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state of Stonehenge (which can be used
        for equality testing). Overrides GameState.__repr__

        >>> state = StonehengeState(True, 1)
        >>> state
        Player: p1 | Cells: {'A': 0, 'B': 0, 'C': 0} | Lines: ['@', '@', \
'@', '@', '@', '@']
        """
        current_player = 'p1' if self.p1_turn is True else 'p2'
        return 'Player: {} | Cells: {}'.format(current_player, self.cell_state)\
               + ' | Lines: {}'.format(sum([self.mark_dl, self.mark_dr,
                                            self.mark_row], []))

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self. Overrides GameState.rough_outcome

        >>> StonehengeState(True, 1).rough_outcome()
        1
        >>> StonehengeState(False, 1).rough_outcome()
        1
        >>> StonehengeState(True, 1).make_move('A').rough_outcome()
        -1
        """
        current = 1 if self.p1_turn is True else 2
        opponent = 2 if current == 1 else 1
        states = [self.make_move(x) for x in self.get_possible_moves()]
        # Return WIN if possible for current player to win
        if any([is_winner(x, current) for x in states]):
            return self.WIN
        substates = [[x.make_move(y) for y in x.get_possible_moves()]
                     for x in states]
        # Return LOSE if possible for opponent to win in all resulting states
        if all([any([is_winner(s, opponent) for s in l]) for l in substates]):
            return self.LOSE
        # Return estimate based on key-line capture difference
        lines = sum([self.mark_dl, self.mark_dr, self.mark_row], [])
        num_cur = sum([1 for x in lines if x == str(current)])
        num_opp = sum([1 for x in lines if x == str(opponent)])
        if num_cur == num_opp:
            return self.DRAW
        elif num_cur > num_opp:
            return (num_cur - num_opp) / (len(lines) / 2)
        return -((num_opp - num_cur) / (len(lines) / 2))


class StonehengeGame(Game):
    """
    The two-player game Stonehenge.

    current_state - the state of a game of Stonehenge
    """
    current_state: StonehengeState

    INSTRUCTIONS = 'Two players will take turns claiming cells, the letters' +\
                   'on the board. A player captures a ley-line, permanently' +\
                   ', when they capture at least half of the cells in that ' +\
                   'ley-line. The player who first captures at least half o' +\
                   'f the ley-lines wins!'

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        Overrides Game.__init__
        """
        side_length = int(input('Enter the length of the board\'s sides: '))
        while side_length < 1:
            side_length = int(input('Enter the length of the board\'s sides: '))
        self.current_state = StonehengeState(p1_starts, side_length)

    def get_instructions(self) -> str:
        """
        Return the instructions for Stonehenge. Overrides Game.get_instructions
        """
        return StonehengeGame.INSTRUCTIONS

    def is_over(self, state: StonehengeState) -> bool:
        """
        Return whether or not this game is over at state. Overrides
        Game.is_over
        """
        return is_winner(state, 1) or is_winner(state, 2)

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game. Overrides Game.is_winner

        Precondition: player is 'p1' or 'p2'.
        """
        current_player = 1 if player == 'p1' else 2
        return self.is_over(self.current_state) and is_winner(
            self.current_state, current_player)

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move. Overrides Game.str_to_move
        """
        if string in self.current_state.get_possible_moves():
            return string
        return '-1'


if __name__ == '__main__':
    from python_ta import check_all
    check_all(config='a2_pyta.txt')
