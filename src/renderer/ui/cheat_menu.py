# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheat_menu.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:43:51 by roandrie        #+#    #+#               #
#  Updated: 2026/06/01 09:13:37 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.renderer.screen_settings import ScreenSettings
from src import game_config
from src.renderer.ui.main_menu import MainMenu
from src.utils import print_log


class BackButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> None:
        if self.parent_view.window:
            self.parent_view.window.show_view(self.parent_view)


class ExtraTime(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> None:
        # Add more time only in main menu
        if isinstance(self.parent_view, MainMenu):
            if self.parent_view.window:
                self.parent_view.window.game_config.level_max_time += 3000.0
        if game_config.debug_mode:
            print_log("Added 3000.0 seconds")


class SpeedUpButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> bool:
        # Add more speed only in game
        from src.game_engine import GameEngine
        from src.renderer.ui.pause_menu import PauseMenu
        if isinstance(self.parent_view, PauseMenu):
            if isinstance(self.parent_view.previous_view, GameEngine):
                game_engine = self.parent_view.previous_view
                game_engine.player.speed += 10
                if game_config.debug_mode:
                    print_log("Speed increases by 10")


class NextLevelButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> None:
        # Mets un booleen youpi Rom1 content
        pass


class FreezeGhostButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> None:
        # Mets un booleen youpi Rom1 content
        pass


class ExtraLivesButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> None:
        # Add more lives in main menu and in game
        from src.game_engine import GameEngine
        from src.renderer.ui.pause_menu import PauseMenu
        from src.renderer.ui.main_menu import MainMenu
        if isinstance(self.parent_view, PauseMenu):
            if isinstance(self.parent_view.previous_view, GameEngine):
                self.parent_view.previous_view.state_manager.live += 1001
                if game_config.debug_mode:
                    print_log("Add 1001 lives more\n")
        elif isinstance(self.parent_view, MainMenu):
            if self.parent_view.window:
                self.parent_view.window.game_config.live += 1001
        if game_config.debug_mode:
            print_log("Added 1001 lives more")


class InvincibilityButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> None:
        # Mets un booleen youpi Rom1 content
        pass


class CheatMenu(BaseMenu):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()

        self.previous_view = previous_view
        self.background = arcade.load_texture(
            self.window.asset_manager.textures["ocean"]
        )

    def build_ui(self) -> None:
        # Create all the cheat mode buttons
        invincibility = InvincibilityButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=600,
            sprite_path=(
                self.window.asset_manager.textures["invincibility"]
            ),
            parent_view=self.previous_view
        )
        extra_lives = ExtraLivesButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=500,
            sprite_path=(
                self.window.asset_manager.textures["extra_lives"]
            ),
            parent_view=self.previous_view
        )
        freeze_ghost = FreezeGhostButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=400,
            sprite_path=(
                self.window.asset_manager.textures["freeze_ghost"]
            ),
            parent_view=self.previous_view
        )
        next_level = NextLevelButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=300,
            sprite_path=(
                self.window.asset_manager.textures["next_level"]
            ),
            parent_view=self.previous_view
        )

        if isinstance(self.previous_view, MainMenu):
            extra_time = ExtraTime(
                center_x=ScreenSettings.WIDTH // 2,
                center_y=200,
                sprite_path=(
                    self.window.asset_manager.textures["extra_time"]
                ),
                parent_view=self.previous_view
            )
            self.button_list.append(extra_time)
        else:
            speed_up = SpeedUpButton(
                center_x=ScreenSettings.WIDTH // 2,
                center_y=200,
                sprite_path=(
                    self.window.asset_manager.textures["speed_up"]
                ),
                parent_view=self.previous_view
            )
            self.button_list.append(speed_up)

        back = BackButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=100,
            sprite_path=(
                self.window.asset_manager.textures["return_button"]
            ),
            parent_view=self.previous_view,
        )
        # Add all buttons on a button list
        self.button_list.append(invincibility)
        self.button_list.append(extra_lives)
        self.button_list.append(freeze_ghost)
        self.button_list.append(next_level)
        self.button_list.append(back)

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            if self.previous_view:
                self.window.show_view(self.previous_view)

    def on_draw(self) -> None:
        self.clear()
        # Draw the beach background
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT)
        )
        # Draw the buttons
        self.button_list.draw()
