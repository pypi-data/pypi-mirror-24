
from rpython.rlib.rbisect import bisect_left, bisect_right

def test_bisect_left():
    cases = [
            ([], 1, 0),
            ([1], 0, 0),
            ([1], 1, 0),
            ([1], 2, 1),
            ([1, 1], 0, 0),
            ([1, 1], 1, 0),
            ([1, 1], 2, 2),
            ([1, 1, 1], 0, 0),
            ([1, 1, 1], 1, 0),
            ([1, 1, 1], 2, 3),
            ([1, 1, 1, 1], 0, 0),
            ([1, 1, 1, 1], 1, 0),
            ([1, 1, 1, 1], 2, 4),
            ([1, 2], 0, 0),
            ([1, 2], 1, 0),
            ([1, 2], 1.5, 1),
            ([1, 2], 2, 1),
            ([1, 2], 3, 2),
            ([1, 1, 2, 2], 0, 0),
            ([1, 1, 2, 2], 1, 0),
            ([1, 1, 2, 2], 1.5, 2),
            ([1, 1, 2, 2], 2, 2),
            ([1, 1, 2, 2], 3, 4),
            ([1, 2, 3], 0, 0),
            ([1, 2, 3], 1, 0),
            ([1, 2, 3], 1.5, 1),
            ([1, 2, 3], 2, 1),
            ([1, 2, 3], 2.5, 2),
            ([1, 2, 3], 3, 2),
            ([1, 2, 3], 4, 3),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 0, 0),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 1, 0),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 1.5, 1),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 2, 1),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 2.5, 3),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 3, 3),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 3.5, 6),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 4, 6),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 5, 10),
        ]
    for lst, elem, exp in cases:
        assert bisect_left(lst, elem, len(lst)) == exp

def test_bisect_right():
    cases = [

            ([], 1, 0),
            ([1], 0, 0),
            ([1], 1, 1),
            ([1], 2, 1),
            ([1, 1], 0, 0),
            ([1, 1], 1, 2),
            ([1, 1], 2, 2),
            ([1, 1, 1], 0, 0),
            ([1, 1, 1], 1, 3),
            ([1, 1, 1], 2, 3),
            ([1, 1, 1, 1], 0, 0),
            ([1, 1, 1, 1], 1, 4),
            ([1, 1, 1, 1], 2, 4),
            ([1, 2], 0, 0),
            ([1, 2], 1, 1),
            ([1, 2], 1.5, 1),
            ([1, 2], 2, 2),
            ([1, 2], 3, 2),
            ([1, 1, 2, 2], 0, 0),
            ([1, 1, 2, 2], 1, 2),
            ([1, 1, 2, 2], 1.5, 2),
            ([1, 1, 2, 2], 2, 4),
            ([1, 1, 2, 2], 3, 4),
            ([1, 2, 3], 0, 0),
            ([1, 2, 3], 1, 1),
            ([1, 2, 3], 1.5, 1),
            ([1, 2, 3], 2, 2),
            ([1, 2, 3], 2.5, 2),
            ([1, 2, 3], 3, 3),
            ([1, 2, 3], 4, 3),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 0, 0),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 1, 1),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 1.5, 1),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 2, 3),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 2.5, 3),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 3, 6),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 3.5, 6),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 4, 10),
            ([1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 5, 10),
        ]
    for lst, elem, exp in cases:
        assert bisect_right(lst, elem, len(lst)) == exp
