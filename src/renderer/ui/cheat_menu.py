# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheat_menu.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:43:51 by roandrie        #+#    #+#               #
#  Updated: 2026/06/01 10:39:40 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import PIL.Image
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
            parent_view: arcade.View,
            texture_off: Path
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_on = self.texture
        self.texture_off = texture_off
        self.active: bool = False

    def on_click(self) -> None:
        if self.active:
            self.texture = self.texture_on
            self.active = False
            self._disable_cheat()

        else:
            self.texture = self.texture_off
            self.active = True
            self._activate_cheat()

    def _activate_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY on")

    def _disable_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY off")


class SpeedUpButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_off: Path
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_on = self.texture
        self.texture_off = texture_off
        self.active: bool = False

    def on_click(self) -> None:
        if self.active:
            self.texture = self.texture_on
            self.active = False
            self._disable_cheat()

        else:
            self.texture = self.texture_off
            self.active = True
            self._activate_cheat()

    def _activate_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY on")

    def _disable_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY off")


class NextLevelButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_off: Path
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_on = self.texture
        self.texture_off = texture_off
        self.active: bool = False

    def on_click(self) -> None:
        if self.active:
            self.texture = self.texture_on
            self.active = False
            self._disable_cheat()

        else:
            self.texture = self.texture_off
            self.active = True
            self._activate_cheat()

    def _activate_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY on")

        self.parent_view.previous_view.player.cheat_invincible = True

    def _disable_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY off")

        self.parent_view.previous_view.player.cheat_invincible = False


class FreezeGhostButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_off: Path
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_on = self.texture
        self.texture_off = texture_off
        self.active: bool = False

    def on_click(self) -> None:
        if self.active:
            self.texture = self.texture_on
            self.active = False
            self._disable_cheat()

        else:
            self.texture = self.texture_off
            self.active = True
            self._activate_cheat()

    def _activate_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY on")

    def _disable_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY off")


class ExtraLivesButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_off: Path
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_on = self.texture
        self.texture_off = texture_off
        self.active: bool = False

    def on_click(self) -> None:
        if self.active:
            self.texture = self.texture_on
            self.active = False
            self._disable_cheat()

        else:
            self.texture = self.texture_off
            self.active = True
            self._activate_cheat()

    def _activate_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY on")

    def _disable_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY off")


class InvincibilityButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_off: Path
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_on = self.texture
        self.texture_off = texture_off
        self.active: bool = False

    def on_click(self) -> None:
        if self.active:
            self.texture = self.texture_on
            self.active = False
            self._disable_cheat()

        else:
            self.texture = self.texture_off
            self.active = True
            self._activate_cheat()

    def _activate_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY on")

    def _disable_cheat(self) -> None:
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY off")


class CheatMenu(BaseMenu):
    def __init__(
        self, previous_view: arcade.View, background: PIL.Image.Image
    ) -> None:
        super().__init__()

        self.previous_view = previous_view
        self.background = background

    def build_ui(self) -> None:
        # Create all the cheat mode buttons
        invincibility = InvincibilityButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=600,
            sprite_path=(
                self.window.asset_manager.textures["invincibility_off"]
            ),
            parent_view=self.previous_view,
            texture_off=arcade.load_texture(
                self.window.asset_manager.textures["invincibility_on"]
            )
        )
        extra_lives = ExtraLivesButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=500,
            sprite_path=(
                self.window.asset_manager.textures["extra_lives_off"]
            ),
            parent_view=self.previous_view,
            texture_off=arcade.load_texture(
                self.window.asset_manager.textures["extra_lives_on"]
            )
        )
        freeze_ghost = FreezeGhostButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=400,
            sprite_path=(
                self.window.asset_manager.textures["freeze_ghost_off"]
            ),
            parent_view=self.previous_view,
            texture_off=arcade.load_texture(
                self.window.asset_manager.textures["extra_lives_on"]
            )
        )
        next_level = NextLevelButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=300,
            sprite_path=(
                self.window.asset_manager.textures["next_level_off"]
            ),
            parent_view=self.previous_view,
            texture_off=arcade.load_texture(
                self.window.asset_manager.textures["next_level_on"]
            )
        )

        if isinstance(self.previous_view, MainMenu):
            extra_time = ExtraTime(
                center_x=ScreenSettings.WIDTH // 2,
                center_y=200,
                sprite_path=(
                    self.window.asset_manager.textures["extra_time_off"]
                ),
                parent_view=self.previous_view,
                texture_off=arcade.load_texture(
                self.window.asset_manager.textures["extra_time_on"]
            )
            )
            self.button_list.append(extra_time)
        else:
            speed_up = SpeedUpButton(
                center_x=ScreenSettings.WIDTH // 2,
                center_y=200,
                sprite_path=(
                    self.window.asset_manager.textures["speed_up_off"]
                ),
                parent_view=self.previous_view,
                texture_off=arcade.load_texture(
                self.window.asset_manager.textures["speed_up_on"]
            )
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
        # Draw the game background image
        if self.background:
            arcade.draw_texture_rect(
                self.background, arcade.XYWH(
                    self.window.width / 2, self.window.height / 2,
                    self.window.width, self.window.height)
            )

        # Draw a black rectangle with an opacity
        arcade.draw_rect_filled(
            arcade.XYWH(
                self.window.width / 2, self.window.height / 2,
                self.window.width, self.window.height),
            (0, 0, 0, 180)
        )
        # Draw the buttons
        self.button_list.draw()
