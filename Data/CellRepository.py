class CellRepository:
    """
    Class that will act as a container, storing objects in a grid
        from a layered architecture view, this should act as the Infrastructure/Data base
    ( for this project this can be replaced with a list or another python predefined container)
    """

    def __init__(self, size=(-1, -1)):
        self._cells = []
        self._nr_rows, self._nr_cols = size

    def get_dimensions(self):
        return self._nr_rows, self._nr_cols

    def append(self, cell):
        self._cells.append(cell)

    def get_at(self, coordinates):
        x, y = coordinates
        if 0 > x or x >= self._nr_rows or 0 > y or y >= self._nr_cols:
            return None
        try:
            return self._cells[self._nr_cols * x + y]
        except IndexError:
            # print("Can't return cell at {x}, {y}".format(x=x, y=y))
            return None

    def update(self, coordinates, new_cell):
        x, y = coordinates
        self._cells[self._nr_cols * x + y] = new_cell

    def reset(self):
        self._cells = []

    def get_all(self):
        return self._cells

    def __iter__(self):
        for cell in self._cells:
            yield cell

    def __len__(self):
        return len(self._cells)

    def __contains__(self, item):
        if type(item) is not tuple:
            raise Exception("Has to be a tuple")
        item_x, item_y = item
        position = item_x * self._nr_cols + item_y
        return -1 < position < len(self._cells)
