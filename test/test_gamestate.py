import arcade
from src.maze import MazeFactory
from src.renderer.maze_renderer import GameRenderer
from src.renderer.screen_settings import ScreenSettings
from src.game_engine.gamestate_manager import GameStateManager
from src.renderer.ui.game_over_screen import GameOverScreen
from src.renderer.ui.finish_screen import FinishScreen



class Test(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.config = self.window.game_config
    #     self.game_renderer = GameRenderer()
    #     self.state_manager = GameStateManager(self.window, parent_view=self)

    # def update(delta: float) -> None:
    #     pass

    # def on_key_press(self, symbol: int, modifiers: int) -> None:
    #     if self.state_manager:
    #         self.state_manager.on_key_press(symbol, modifiers)

    def on_show_view(self) -> None:
        game_over = FinishScreen("522465")
        self.window.show_view(game_over)
        # self.clear()
        # self.setup()

    # def setup(self) -> None:

    #     factory = MazeFactory()
    #     wall_data = factory.generate_maze(
    #         15, 15,
    #         self.window.asset_manager.textures,
    #         ScreenSettings.WIDTH,ScreenSettings.HEIGHT,
    #         self.game_renderer
    #     )

    #     self.game_renderer.wall_generator(wall_data)
    #     self.game_renderer.draw()

    #     self.state_manager = GameStateManager(self.window, parent_view=self)
