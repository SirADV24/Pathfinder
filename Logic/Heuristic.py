#  usefull doc http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#S7
from math import sqrt


def h_manhatan_distance(point_a, point_b):
    x_a, y_a = point_a
    x_b, y_b = point_b
    dx = abs(x_a - x_b)
    dy = abs(y_a - y_b)
    return dx + dy


def h_manhatan_distance_diagonal(point_a, point_b):
    # also knowed as octile distance
    sqrt_2 = 1.4142  # sqrt(2)
    x_a, y_a = point_a
    x_b, y_b = point_b
    dx = abs(x_a - x_b)
    dy = abs(y_a - y_b)
    return (dx + dy) + (sqrt_2 - 2) * min(dx, dy)


def h_square_euclidian_distance_squared(point_a, point_b):
    x_a, y_a = point_a
    x_b, y_b = point_b
    dx = abs(x_a - x_b)
    dy = abs(y_a - y_b)
    return dx * dx + dy * dy


def h_square_euclidian_distance(point_a, point_b):
    x_a, y_a = point_a
    x_b, y_b = point_b
    dx = abs(x_a - x_b)
    dy = abs(y_a - y_b)
    return 1 * sqrt(dx * dx + dy * dy)

