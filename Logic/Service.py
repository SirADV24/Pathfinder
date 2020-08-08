from Data.CellRepository import CellRepository
from Data.Cell import Cell
from Logic.Pathfinder import _a_star, _dijkstra, _breadth_first
from Logic.Heuristic import *
from Logic.MazeGenerator import _generate_maze_recursive_backtracker


class Serivce:
    """
        Class that will connect all the other components
    """

    def __init__(self):
        #  default parameters
        self._cells_on_row, self._cells_on_column = (20, 10)  # default world small
        self._cells = CellRepository((self._cells_on_row, self._cells_on_column))
        self._pathfinder_algorythm = "A star"  # default pathfinder algorythm
        self._heuristic = "Manhatan"  # default heuristic
        self._allow_diagonal_movement = False  # default directions
        self._start, self._end = None, None
        ###
        self._pathfinder_algorythms = {
            "A star": _a_star,
            "Dijkstra": _dijkstra,
            "BreadthFirst": _breadth_first
        }
        self._heuristic_functions = {
            "Manhatan": h_manhatan_distance,
            "Octile": h_manhatan_distance_diagonal,
            "Euclidian": h_square_euclidian_distance,
            "Euclidian-squared": h_square_euclidian_distance_squared
        }

    def get_grid_size(self):
        return self._cells_on_row, self._cells_on_column

    def set_algorythm(self, algorythm):
        self._pathfinder_algorythm = algorythm

    def set_world_size(self, size):
        self._cells_on_row, self._cells_on_column = size
        self._cells = CellRepository((self._cells_on_row, self._cells_on_column))
        self._start, self._end = None, None

    def set_heuristic(self, heuristic):
        self._heuristic = heuristic

    def set_diagonal_movement(self, how):
        self._allow_diagonal_movement = how

    def generate_empty_cells(self, reset=True):
        if (self._cells_on_row, self._cells_on_column) == (-1, -1):
            raise Exception("Grid size not specified")

        if reset:
            self._cells.reset()
            self._start, self._end = None, None

        if (self._cells_on_row, self._cells_on_column) == (-1, -1):
            self._cells_on_row, self._cells_on_column = self._cells.get_dimensions()

        for i in range(self._cells_on_row):
            for j in range(self._cells_on_column):
                self._cells.append(Cell(i, j))

    def cell_left_clicked(self, coordinates):
        cell = self._cells.get_at(coordinates)

        if cell.get_color() == "black":
            return cell

        if self._start is None and cell != self._end:
            cell.set_color("Start")
            self._start = cell
        elif self._end is None and cell != self._start:
            cell.set_color("End")
            self._end = cell
        else:
            if not cell == self._end and not cell == self._start:
                cell.set_color("Wall")

        self._cells.update(coordinates, cell)
        return cell

    def cell_right_clicked(self, coordinates):
        cell = self._cells.get_at(coordinates)

        cell.set_color()
        if cell == self._start:
            self._start = None
        elif cell == self._end:
            self._end = None

        self._cells.update(coordinates, cell)
        return cell

    def maze(self, draw_cell):
        for cell in self._cells:
            cell.set_color("Wall")
        draw_cell(self._cells)
        lenght = _generate_maze_recursive_backtracker(self._cells, [(0, -1), (1, 0), (-1, 0), (0, 1)],
                                                      draw_cell, self._cells.get_at((2, 2)))
        if lenght < 10:
            self.maze(draw_cell)

    def get_cells(self):
        return self._cells.get_all()

    def get_animation_info(self):
        return self._pathfinder_algorythm, self._heuristic, self._allow_diagonal_movement

    def animate(self, draw_function):
        heuristic = self._heuristic_functions[self._heuristic]
        allow_diagonal = self._allow_diagonal_movement
        self._pathfinder_algorythms[self._pathfinder_algorythm] \
            (self._cells, self._start, self._end, allow_diagonal, draw_function, heuristic)
