# puzz

A python jigsaw puzzle generator.

## usage

Generate problem and solution csv files for a puzzle with arbitrary rows and columns:

```
$ python3 puzz.py --rows 3 --cols 4
```

## pieces

Each piece contains information with unique edges and its orientation:

```python
{
    'id': 3,
    'edge_top': None,
    'edge_right': None,
    'edge_bottom': 'tab-21',
    'edge_left': 'blank-33',
    'orientation': 'W',
    'row': 0,
    'col': 0,
}
```

### orientation

Orientations are simply the cardinal directions:

```
['N', 'E', 'S', 'W']
```

The solution assumes the puzzle itself is oriented with its top edge facing north.

If a piece has orientation `'W'`, its top edge is facing west.

### edges

An edge value of `tab-21` will match with another edge with value `blank-21`. [More on jigsaw puzzle terminology](https://english.stackexchange.com/a/47672).

A `None` value of an edge corresponds to an actual edge piece of a puzzle.

Edge ids are generated as the product of the (always prime) ids of the pieces they connect. Consequently, the example piece will have piece with `id=7` on its bottom (east of the piece when taking its orientation into account), and piece with `id=11` on its left edge (south of the piece).

This example piece is in the top left corner of the puzzle.


## goal

Write a program that reads in `problem.csv` and correctly determines the orientation, row, and column of each piece.

`problem.csv` will contain piece ids and edge information, with only a single random piece's orientation, row, and column value pre-populated.

`solution.csv` will have all piece information filled in.

## etc

See the problem and solution csvs in `examples/` for a simple 2x3 puzzle.

This runs quick for small puzzles, but takes like 5 seconds to generate a 1000-piece puzzle. Could probably be optimized, and my code could probably be prettier. In addition, the prime number multiplication to ensure edge id uniqueness might end up overflowing for really large puzzles.

A hash function or something like [diffie-hellman](https://security.stackexchange.com/questions/45963/diffie-hellman-key-exchange-in-plain-english) key exchange for checking if edge pieces matched might have been a cooler way to make it less obvious which edge pieces match.
