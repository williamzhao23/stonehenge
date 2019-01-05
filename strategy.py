"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
from tree import Tree


def state_score_r(game: Any, state: Any) -> int:
    """
    Return the move score for a state of a game. This implementation is
    recursive.
    """
    if game.is_over(state):
        current = 'p1' if state.p1_turn is True else 'p2'
        other = 'p1' if current == 'p2' else 'p2'
        old_state = game.current_state
        game.current_state = state
        if game.is_winner(current) and not game.is_winner(other):
            game.current_state = old_state
            return 1
        elif game.is_winner(other) and not game.is_winner(current):
            game.current_state = old_state
            return -1
        game.current_state = old_state
        return 0
    states = [state.make_move(m) for m in state.get_possible_moves()]
    return max([-state_score_r(game, s) for s in states])


def state_score_i(game: Any, state_: Any) -> int:
    """
    Return the move score for a state of a game. This implementation is
    iterative.
    """
    initial = Tree(state_)
    stack = [initial]
    while stack != []:
        tree = stack.pop()
        state = tree.value
        if game.is_over(state):
            current = 'p1' if state.p1_turn is True else 'p2'
            other = 'p1' if current == 'p2' else 'p2'
            old_state = game.current_state
            game.current_state = state
            if game.is_winner(current) and not game.is_winner(other):
                game.current_state = old_state
                tree.score = 1
            elif game.is_winner(other) and not game.is_winner(current):
                game.current_state = old_state
                tree.score = -1
            else:
                game.current_state = old_state
                tree.score = 0
        elif tree.children == []:
            states = [state.make_move(m) for m in state.get_possible_moves()]
            trees = [Tree(s) for s in states]
            tree.children = trees
            stack.append(tree)
            for t in trees:
                stack.append(t)
        else:
            tree.score = max([-c.score for c in tree.children])
    return initial.score


def recursive_minimax_strategy(game: Any) -> Any:
    """
    Return a move for game that leads to a win, if a win is possible. This
    implementation is recursive.
    """
    moves = game.current_state.get_possible_moves()
    possible_states = [game.current_state.make_move(m) for m in moves]
    scores = [-state_score_r(game, s) for s in possible_states]
    return moves[scores.index(max(scores))]


def iterative_minimax_strategy(game: Any) -> Any:
    """
    Return a move for game that leads to a win, if a win is possible. This
    implementation is iterative.
    """
    moves = game.current_state.get_possible_moves()
    possible_states = [game.current_state.make_move(m) for m in moves]
    scores = [state_score_i(game, s) for s in possible_states]
    scores_ = [-s for s in scores]
    return moves[scores_.index(max(scores_))]


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
