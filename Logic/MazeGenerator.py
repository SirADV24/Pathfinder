import random


def _get_neighbours(cell, cells, directions):
    cell_x, cell_y = cell.get_coordinates()
    neighbours = []
    for direction in directions:
        neighbour_x, neighbour_y = cell_x + direction[0], cell_y + direction[1]
        neighbour = cells.get_at((neighbour_x, neighbour_y))
        if neighbour is not None and neighbour.check_if_wall():
            neighbours.append(neighbour)
    return neighbours


def _backtrack(stack, cells, directions, visited):
    while stack:
        current = stack.pop()
        for neighbour in _get_neighbours(current, cells, directions):
            if not visited[neighbour]:
                return neighbour

    return None


def _generate_maze_recursive_backtracker(cells, directions, draw, start=(2, 2)):
    visited = {cell: False for cell in cells}
    visited[start] = True
    stack = []
    current = start
    maze_lenght = 0

    while current is not None:
        while current is not None:
            # we move current to one random neighbour
            shuffled_neighbours = _get_neighbours(current, cells, directions)
            random.shuffle(shuffled_neighbours)
            for neighbour in shuffled_neighbours:
                if not visited[neighbour] and len(_get_neighbours(neighbour, cells, directions)) >= 4:
                    current.set_color("default")
                    draw([current])
                    maze_lenght += 1
                    visited[current] = True
                    current = neighbour
                    stack.append(current)
                    break
            else:
                break
            if not stack:
                return maze_lenght
        current = _backtrack(stack, cells, directions, visited)

    return maze_lenght




