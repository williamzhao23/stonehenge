"""
Tree class
# Code taken from CSC148 lecture materials and slightly modified
"""
from typing import Union, List


class Tree:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree.
    Specialized for iterative minimax.

    value - value of root node
    children - child nodes
    score - score of the state
    """
    value: object
    children: Union[List['Tree'], None]
    score: Union[int, None]

    def __init__(self, value: object = None, children: List['Tree'] = None) ->\
            None:
        """
        Create Tree self with content value and 0 or more children

        >>> t = Tree(5, [Tree(1), Tree(2)])
        >>> t.value
        5
        >>> t.children[0].value
        1
        >>> t.children[0].children
        []
        """
        self.value = value
        self.children = children[:] if children is not None else []
        self.score = None


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
