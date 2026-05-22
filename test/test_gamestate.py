import arcade
from src.maze import MazeFactory
from renderer.game_renderer import GameRenderer
from src.renderer.screen_settings import ScreenSettings
from src.game_engine.gamestate_manager import GameStateManager
from src.renderer.ui.game_over_screen import GameOverScreen
from src.renderer.ui.finish_screen import FinishScreen
from src.renderer.ui.ui_screen import UIScreen



class Test(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.config = self.window.game_config
        self.game_renderer = GameRenderer()
        self.state_manager = GameStateManager(self.window, parent_view=self)
        self.initialized = False

    def update(delta: float) -> None:
        pass

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if self.state_manager:
            self.state_manager.on_key_press(symbol, modifiers)

    def on_show_view(self) -> None:
        # game_over = GameOverScreen("465121534", self.config.highscore_filename,
        #                          previous_view=self)
        # self.window.show_view(game_over)

    #     self.clear()
    #     if not self.initialized:
    #         self.initialized = True
    #         self.setup()
    #     else:
    #         self.game_renderer.draw()

    # def setup(self) -> None:

    #     factory = MazeFactory()
    #     wall_data = factory.generate_maze(
    #         15, 15,
    #         self.window.asset_manager.textures,
    #         ScreenSettings.WIDTH,ScreenSettings.HEIGHT
    #     )

    #     self.game_renderer.wall_generator(wall_data)
    #     self.game_renderer.draw()

    #     self.state_manager = GameStateManager(self.window, parent_view=self)

        ui_screen = UIScreen("465121534", "03.00", 3)
        self.window.show_view(ui_screen)

