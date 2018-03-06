"""
Puzz - a python jigsaw puzzle generator.
"""
import argparse
import csv
import random


def is_prime(a):
    """
    Determine if `a` is prime. Ripped straight from SO.
    """
    return a > 1 and all(a % i for i in range(2, int(a**0.5) + 1))


def generate_primes(n):
    """
    Generate list of first n primes, starting with 3.
    """
    primes = []

    val = 3
    while len(primes) < n:

        if is_prime(val):
            primes.append(val)
        val += 1

    return primes


def rotate_orientation_clockwise(orientation):
    """
    Rotate cardinal direction clockwise.
    """
    orientations = ['N', 'E', 'S', 'W']
    idx = orientations.index(orientation)
    return orientations[idx+1] if idx < len(orientations)-1 else orientations[0]


def rotate_piece_clockwise(piece):
    """
    Rotate a piece clockwise, updating edge ids and orientation.
    """
    return {
        'id': piece['id'],
        'orientation': rotate_orientation_clockwise(piece['orientation']),
        'row': piece['row'],
        'col': piece['col'],
        'edge_top': piece['edge_right'],
        'edge_right': piece['edge_bottom'],
        'edge_bottom': piece['edge_left'],
        'edge_left': piece['edge_top'],
    }


def generate_puzz(rows, cols):
    """
    Generate a puzzle with dimensions (rows, cols).
    """
    def idx(r, c):
        return c*rows + r

    # generate randomly ordered list of primes to serve as piece ids
    piece_ids = generate_primes(rows*cols)
    random.shuffle(piece_ids)

    # create pieces
    puzz = []
    for r in range(rows):
        for c in range(cols):

            id = piece_ids[idx(r,c)]

            # create piece, along with deterministic unique edge ids
            piece = {
                'id': id,
                'orientation': 'N',
                'row': r,
                'col': c,
                'edge_left': piece_ids[idx(r, c-1)]*id if c > 0 else None,
                'edge_right': piece_ids[idx(r, c+1)]*id if c<cols-1 else None,
                'edge_top': piece_ids[idx(r-1, c)]*id if r > 0 else None,
                'edge_bottom': piece_ids[idx(r+1, c)]*id if r<rows-1 else None,
            }

            # rotate piece randomly
            for _ in range(random.randint(0,3)):
                piece = rotate_piece_clockwise(piece)

            puzz.append(piece)

    # assemble set of edge ids
    edge_ids = set(
        v
        for piece in puzz
        for k,v in piece.items()
        if 'edge_' in k
        and v is not None
    )

    # update each edge id flagging as a 'tab' or 'blank'
    for e_id in edge_ids:
        pcs = [
            piece
            for piece in puzz
            if any(v == e_id for k,v in piece.items() if 'edge_' in k)
        ]

        # should always have exactly 2 pieces
        if len(pcs) != 2:
            raise Exception(f'not 2 pcs: {len(pcs)}')

        # get specific keys for these edges
        keys = [k for p in pcs for k,v in p.items() if v == e_id]

        # randomly assign a tab and a blank to the pair of edges
        types = ['tab', 'blank']
        random.shuffle(types)

        # update edge id
        for p, k, t in zip(pcs, keys, types):
            p[k] = f'{t}-{p[k]}'


    return puzz


def generate_csvs(puzz):
    """
    Generate problem and solution csvs for a given puzz.
    """
    header_order = [
        'id',
        'edge_top',
        'edge_right',
        'edge_bottom',
        'edge_left',
        'orientation',
        'row',
        'col',
    ]

    # write out entire puzz as solution
    with open('solution.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header_order)
        writer.writeheader()
        writer.writerows(puzz)

    # create a problem puzzle with only a single piece's solution populated
    solution_idx = random.randint(0, len(puzz))
    prob_puzz = list(puzz)
    for idx, p in enumerate(prob_puzz):
        if idx == solution_idx:
            continue
        p['orientation'] = None
        p['row'] = None
        p['col'] = None

    with open('problem.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=header_order)
        writer.writeheader()
        writer.writerows(prob_puzz)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rows', required=True, type=int)
    parser.add_argument('-c', '--cols', required=True, type=int)
    args = parser.parse_args()

    puzz = generate_puzz(args.rows, args.cols)
    generate_csvs(puzz)
