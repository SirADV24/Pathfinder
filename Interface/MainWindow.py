import pygame as pg
from Interface.utils import colors
from Interface.Menu import Menu


class MainWindow:
    def __init__(self, width, height, service):
        self._sizes = width, height
        self._service = service
        self._screen = pg.display.set_mode(self._sizes)
        # Default parameters
        self._grid_size = service.get_grid_size()
        self._cell_size = width / self._grid_size[0], height / self._grid_size[1]
        self._menu = Menu(self._service, self._screen)

        self._show_menu = True
        self._user_drawing = False
        self._user_erasing = False
        self._animation_going = False
        self._key_bindings = {
            pg.K_SPACE: self._animation,
            pg.K_r: self._reset,
            pg.K_g: self._generate_maze
        }

    def draw_cells(self, cells):
        # function to draw the cells
        for cell in cells:
            rect_x, rect_y = cell.get_coordinates()
            rect_width, rect_height = self._cell_size
            pg.draw.rect(self._screen, colors[cell.get_color()],
                         pg.Rect(rect_width * rect_x, rect_height * rect_y, rect_width, rect_height))
            # draw the borders :
            # North
            pg.draw.aaline(self._screen, colors["light grey"],
                           (rect_width * rect_x, rect_height * rect_y),
                           (rect_width * (rect_x + 1), rect_height * rect_y))
            # South
            pg.draw.aaline(self._screen, colors["light grey"],
                           (rect_width * rect_x, rect_height * (rect_y + 1)),
                           (rect_width * (rect_x + 1), rect_height * (rect_y + 1)))
            # West
            pg.draw.aaline(self._screen, colors["light grey"],
                           (rect_width * rect_x, rect_height * rect_y),
                           (rect_width * rect_x, rect_height * (rect_y + 1)))
            # East
            pg.draw.aaline(self._screen, colors["light grey"],
                           (rect_width * (rect_x + 1), rect_height * rect_y),
                           (rect_width * (rect_x + 1), rect_height * (rect_y + 1)))

    def _lock_events(self):
        pg.event.set_blocked(pg.MOUSEMOTION)
        pg.event.set_blocked(pg.MOUSEBUTTONUP)
        pg.event.set_blocked(pg.MOUSEBUTTONDOWN)
        pg.event.set_blocked(pg.KEYDOWN)

    def _unlock_events(self):
        pg.event.set_allowed(pg.MOUSEMOTION)
        pg.event.set_allowed(pg.MOUSEBUTTONUP)
        pg.event.set_allowed(pg.MOUSEBUTTONDOWN)
        pg.event.set_allowed(pg.KEYDOWN)

    def _mouse_down(self, event, erasing=False):
        # function called when user is painting/erasing
        try:
            mouse_x, mouse_y = event.pos
        except Exception as ex:
            return
        # check if coordinates are in the grid limits
        if mouse_x < 0 or mouse_x > self._sizes[0] or mouse_y < 0 or mouse_y > self._sizes[1]:
            return
        # convert coordinates from real ones to grid ones
        coordinates = (int(mouse_x // self._cell_size[0]),
                       int(mouse_y // self._cell_size[1]))
        if not erasing:
            new_cell = self._service.cell_left_clicked(coordinates)
            self.draw_cells([new_cell])
            self._user_drawing = True
        else:
            new_cell = self._service.cell_right_clicked(coordinates)
            self.draw_cells([new_cell])
            self._user_drawing = True
        pg.display.update()

    def _reset(self):
        self._service.generate_empty_cells(True)
        self.draw_cells(self._service.get_cells())
        pg.display.update()

    def update_user_settings(self):
        self._grid_size = self._service.get_grid_size()
        self._cell_size = self._sizes[0] / self._grid_size[0], self._sizes[1] / self._grid_size[1]
        self._service.generate_empty_cells((self._sizes[0] / self._grid_size[0],
                                            self._sizes[1] / self._grid_size[1]))

        self._screen.fill(colors["white"])
        self.draw_cells(self._service.get_cells())
        pg.display.update()

    def _animation_function(self, cell):
        # this function will be called by the animation function for each cell
        self.draw_cells(cell)
        pg.display.update()

    def _show_legend(self):
        animation_algorythm, animation_heuristic, animation_movement \
            = self._service.get_animation_info()
        legend = "Algorythm: " + animation_algorythm + \
                 "    Heuristic: " + animation_heuristic + \
                 "    Diagonal Movement: " + str(animation_movement)
        pg.display.set_caption(legend)

    def _generate_maze(self):
        self._lock_events()
        self._reset()
        self._service.maze(lambda cells: self._animation_function(cells))
        self._unlock_events()

    def _animation(self):
        self._animation_going = True
        self._lock_events()
        self._service.animate(lambda cell: self._animation_function(cell))
        self._show_legend()
        self._animation_going = False
        self._unlock_events()

    def run(self):
        i_am_running = True
        while i_am_running:
            if not self._show_menu:
                if self._animation_going:
                    continue
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        i_am_running = False
                        break
                    # mouse actions
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self._user_drawing = True
                        elif event.button == 3:
                            self._user_erasing = True
                    elif event.type == pg.MOUSEBUTTONUP:
                        self._user_drawing = False
                        self._user_erasing = False
                    # keyboards actions

                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_m:
                            self._show_menu = True
                            break
                        elif event.key in self._key_bindings.keys():
                            self._key_bindings[event.key]()

                    if self._user_drawing and not self._user_erasing:
                        #  With this aproach user can draw walls continuously
                        self._mouse_down(event)

                    if self._user_erasing:
                        self._mouse_down(event, erasing=True)
            else:
                self._menu.show()
                self.update_user_settings()
                self._show_menu = False
