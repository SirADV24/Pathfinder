
class Cell:
    """
    Class that will hold all the attributes of a grid cell
    """
    def __init__(self, pos_x, pos_y, color="white"):
        self._x = pos_x
        self._y = pos_y
        self._color = color
        self._colors = {
            "default": "white",
            "Processed": "green",
            "On stack": "grey",
            "Start": "blue",
            "End": "red",
            "Wall": "black",
            "Path": "purple"
        }

    def get_coordinates(self):
        return self._x, self._y

    def get_color(self):
        return self._color

    def check_if_wall(self):
        return self._color == "black" or self._color == "Wall"

    def set_color(self, color=None):
        if color is None:
            color = self._colors["default"]
        if color in self._colors.keys():
            color = self._colors[color]
        self._color = color

    def __lt__(self, other):
        return False

