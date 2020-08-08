from queue import PriorityQueue
from Logic.Heuristic import *


_directions = {
    "Diagonal": [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],
    "Non-Diagonal": [(0, -1), (1, 0), (-1, 0), (0, 1)]
}


def _get_neighbours(cell, cells, directions):
    cell_x, cell_y = cell.get_coordinates()
    neighbours = []
    for direction in directions:
        neighbour_x, neighbour_y = cell_x + direction[0], cell_y + direction[1]
        neighbour = cells.get_at((neighbour_x, neighbour_y))
        if neighbour is not None and not neighbour.check_if_wall():
            neighbours.append(neighbour)
    return neighbours


def get_cost(point_a, point_b):
    # return the distance between 2 adjacent nodes
    x_a, y_a = point_a
    x_b, y_b = point_b
    if x_a == x_b or y_a == y_b:
        return 1
    else:
        return 1.4142  # sqrt(2)


def _a_star(cells, start, end, allow_diagonal, draw_cell, heuristic):
    directions = _directions["Diagonal"] if allow_diagonal else _directions["Non-Diagonal"]
    queue = PriorityQueue()
    count = 0
    queue.put((0, count, start))
    parents = {}
    g_score = {cell: float("inf") for cell in cells}
    g_score[start] = 0
    f_score = {cell: float("inf") for cell in cells}
    f_score[start] = heuristic(start.get_coordinates(), end.get_coordinates())

    queue_elements = {start}  # Priority queue doesn't have check element existance
    found = False
    while not queue.empty():
        current = queue.get()[2]
        queue_elements.remove(current)

        for neighbour in _get_neighbours(current, cells, directions):
            if neighbour == end:
                parents[neighbour] = current
                found = True
                break
            if g_score[current] + 1 < g_score[neighbour]:
                cost = get_cost(current.get_coordinates(), neighbour.get_coordinates())
                parents[neighbour] = current
                g_score[neighbour] = g_score[current] + cost
                f_score[neighbour] = g_score[current] + cost \
                                     + heuristic(neighbour.get_coordinates(), end.get_coordinates())

                if neighbour not in queue_elements:
                    count += 1
                    queue.put((f_score[neighbour], count, neighbour))
                    queue_elements.add(neighbour)

        if current != start and current != end:
            current.set_color("Processed")
            draw_cell([current])

        if found:

            current = parents[end]
            while current != start:
                current.set_color("Path")
                draw_cell([current])
                current = parents[current]

            return parents, end, start


def _dijkstra(cells, start, end, allow_diagonal, draw_cell, heuristic=None):
    directions = _directions["Diagonal"] if allow_diagonal else _directions["Non-Diagonal"]

    queue = PriorityQueue()
    queue.put((0, start))
    parents = {}
    distances = {start: 0}
    found = False
    while not queue.empty():
        current = queue.get()[1]

        for neighbour in _get_neighbours(current, cells, directions):
            if neighbour == end:
                parents[neighbour] = current
                found = True
                break

            if neighbour not in distances.keys():
                distances[neighbour] = float("inf")
                cost = get_cost(current.get_coordinates(), neighbour.get_coordinates())
                if distances[current] + cost < distances[neighbour]:
                    distances[neighbour] = distances[current] + cost
                    parents[neighbour] = current
                    queue.put((distances[neighbour], neighbour))

            if current != start and current != end:
                current.set_color("Processed")
                draw_cell([current])

            if found:

                current = parents[end]
                while current != start:
                    current.set_color("Path")
                    draw_cell([current])
                    current = parents[current]

                return parents, end, start


def _breadth_first(cells, start, end, allow_diagonal, draw_cell, heuristic=None):
    # bfs
    directions = _directions["Diagonal"] if allow_diagonal else _directions["Non-Diagonal"]

    visited = {cell: False for cell in cells}
    queue = [start]
    visited[start] = True
    parents = {}
    found = False
    while len(queue) != 0:
        current = queue.pop(0)
        if current == end:
            pass

        for neighbour in _get_neighbours(current, cells, directions):
            if visited[neighbour]:
                continue
            parents[neighbour] = current

            if neighbour == end:
                found = True
                break

            queue.append(neighbour)
            visited[neighbour] = True

        if current != start and current != end:
            current.set_color("Processed")
            draw_cell([current])

        if found:
            current = parents[end]
            while current != start:
                current.set_color("Path")
                draw_cell([current])
                current = parents[current]

            return parents, end, start
