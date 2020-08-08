import pygame as pg
import pygame_menu as pgm


class Menu:
    TUTORIAL_TEXT = ["- Use Left-Click to fill cells on the board, first cell will be the starting",
                     "point while the second one will be the end point, the rest will be walls",
                     "- Use Right-Click to erase any filled cell",
                     "- In the menu choose your preferred algorythm, grid size or others",
                     "- HotKeys: ",
                     "Press M to open menu again after closing",
                     "Press R to reset the grid to its original state",
                     "Press G to generate a random maze",
                     "Press Space to start the visualistion once your are done drawing",
                     "Quick Note: not every algorythm uses an heuristic ",
                     "and not every combination of heuristic, algorythm,",
                     "and diagonal movement are optimal",
                     "the purpose of this project is to show the different combinations"]

    def __init__(self, service, screen):
        self._service = service
        # don't hardcode this
        self._window = pgm.Menu(500, 1000, "Menu", theme=pgm.themes.THEME_BLUE)
        self._tutorial_menu = pgm.Menu(500, 1000, "Tutorial", theme=pgm.themes.THEME_BLUE)

        self._screen = screen
        self._running = False
        self._world_size_dict = {
            "Small": (20, 10),
            "Medium": (40, 20),
            "Large": (80, 40),
            "Huge": (160, 80)
        }
        self._init_grphic()

    def _init_grphic(self):
        self._window.add_button("Tutorial", self._show_tutorial)
        self._window.add_selector("Algorythm", [("A star", 0), ("Dijkstra", 1),
                                                ("BreadthFirst", 2)],
                                  onchange=self._set_algorythm)
        self._window.add_selector("Heuristic", [("Manhatan", 0), ("Euclidian", 1),
                                                ("Euclidian-squared", 2), ("Octile", 3)],
                                  onchange=self._set_heuristic)
        self._window.add_selector("Grid Size",
                                  [("Small", 0), ("Medium", 1), ("Large", 2), ("Huge", 3)],
                                  onchange=self._set_world_size)
        self._window.add_selector("Allow diagonal movement", [("Not Allowed", 0), ("Allowed", 1)],
                                  onchange=self._set_diagonal_movement)
        self._window.add_button("Apply and Exit Menu", self._stop)

    def _show_tutorial(self):
        self._tutorial_menu.enable()
        for string in Menu.TUTORIAL_TEXT:
            self._tutorial_menu.add_label(string)
        self._tutorial_menu.add_button("GO BACK", self._hide_tutorial)
        self._tutorial_menu.mainloop(self._screen)

    def _hide_tutorial(self):
        self._tutorial_menu.disable()

    def _set_algorythm(self, *args):
        self._service.set_algorythm(args[0][0])

    def _set_world_size(self, *args):
        self._service.set_world_size(self._world_size_dict[args[0][0]])

    def _set_heuristic(self, *args):
        self._service.set_heuristic(args[0][0])

    def _set_diagonal_movement(self, *args):
        how = False
        if args[0][0] == "Allowed":
            how = True
        self._service.set_diagonal_movement(how)

    def _stop(self):
        self._window.disable()
        pg.display.update()

    def show(self):
        self._window.enable()
        self._window.mainloop(self._screen)
