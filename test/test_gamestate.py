from src.renderer.game_renderer import GameRenderer
from src.game_engine.gamestate_manager import GameStateManager
import arcade
from src.renderer.ui.finish_screen import FinishScreen
from src.renderer.ui.game_over_screen import GameOverScreen

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
        game_over = FinishScreen("100000", self.config.highscore_filename,
                                 previous_view=self)
        self.window.show_view(game_over)

