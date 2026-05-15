"""
Spec for: num_islands
"""

TITLE = "Number of Islands"

DESCRIPTION = """
Given a 2D grid of '1' (land) and '0' (water), count the number of
islands. An island is a maximal group of '1' cells connected
horizontally or vertically (NOT diagonally).

Example:
    grid = [["1","1","0"],
            ["1","0","0"],
            ["0","0","1"]]
    -> 2 islands (the L-shape in the top-left, and the lone '1' at bottom-right)
"""

CONSTRAINTS = """
- Grid dimensions up to 300x300
- Cells are strings '0' or '1' (not ints)
- Diagonal connections don't count
- Empty grid returns 0
"""

SIGNATURE = "def solution(grid: list[list[str]]) -> int:"

CASES = [
    # canonical example: L-shape + isolated cell
    ([["1","1","0"],["1","0","0"],["0","0","1"]], 2),
    # one connected blob (donut)
    ([["1","1","1"],["0","1","0"],["1","1","1"]], 1),
    # empty grid
    ([], 0),
    # single cell - water
    ([["0"]], 0),
    # single cell - land
    ([["1"]], 1),
    # alternating row: each '1' isolated
    ([["1","0","1","0","1"]], 3),
    # all water, multi-cell
    ([["0","0"],["0","0"]], 0),
    # all land, multi-cell
    ([["1","1"],["1","1"]], 1),
    # diagonal-only touching: must NOT merge
    ([["1","0","1"],["0","1","0"],["1","0","1"]], 5),
    # vertical strip
    ([["1"],["1"],["0"],["1"]], 2),
]

MUTATES_INPUT = True
