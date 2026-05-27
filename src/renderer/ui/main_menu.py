# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_menu.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:37:31 by roandrie        #+#    #+#               #
#  Updated: 2026/05/27 10:42:59 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.game_engine import GameEngine
from src.renderer.ui.highscores_screen import HighscoresScreen
from src.renderer.ui.instructions_screen import InstructionsScreen
from src.renderer.ui.cheat_menu import CheatMenu
import math
from src.renderer.screen_settings import ScreenSettings
from src.utils import load_sprite_sheet
from src.game_engine.level_manager import LevelManager


class Pursuit(arcade.Sprite):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 parent_view: arcade.View,
                 textures_list: list,
                 scale: float = 1.8) -> None:

        super().__init__(
            path_or_texture=textures_list[0],
            center_x=center_x,
            center_y=center_y,
            scale=scale
        )

        self.parent_view = parent_view
        self.textures_list = textures_list


class Pacman(arcade.Sprite):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 parent_view: arcade.View,
                 textures_list: list,
                 scale: float = 1.8) -> None:

        super().__init__(
            path_or_texture=textures_list[0],
            center_x=center_x,
            center_y=center_y,
            scale=scale
        )

        self.parent_view = parent_view
        self.textures_list = textures_list
        self.current_texture_index = 0
        self.animation_time = 0.0
        self.animation_speed = 0.1

    def on_update(self, delta_time: float):
            self.center_x += self.change_x
            self.animation_time += delta_time
            if self.animation_time >= self.animation_speed:
                self.animation_time -= self.animation_speed
                self.current_texture_index = (self.current_texture_index + 1) % len(self.textures_list)
                self.texture = self.textures_list[self.current_texture_index]

class LogoButton(BaseButton):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.3
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.scale = scale
        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view
        self.is_landing = False
        self.total_time = 0.0
        self.gullman = False
        self.sprite_path = sprite_path

    def land(self):
        self.scale_x = 1.4
        self.scale_y = 0.7
        self.is_landing = True

    def jump(self):
        self.scale_x = 0.8
        self.scale_y = 1.4
        self.is_landing = False

    def on_update(self, delta_time):
        self.total_time += delta_time
        if self.is_landing:
            speed = 8 * delta_time
            self.scale_x = arcade.lerp(self.scale_x, 1.0, speed)
            self.scale_y = arcade.lerp(self.scale_y, 1.0, speed)
            if abs(self.scale_x - 1.0) < 0.01:
                self.scale_x = 1.0
                self.scale_y = 1.0
                self.is_landing = False
        else:
            t = self.total_time
            self.scale_x = 1.0 + math.sin(t * 3) * 0.05
            self.scale_y = 1.0 + math.cos(t * 3) * 0.05

    def on_click(self):
        if self.gullman is False:
            path = self.parent_view.window.asset_manager.textures["gullman"]
        else:
            path = self.parent_view.window.asset_manager.textures["logo"]
        self.texture = arcade.load_texture(path)
        self.gullman = not self.gullman

    def check_hover(self, x: float, y: float) -> None:
        pass

class CheatButton(BaseButton):
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
        if self.parent_view.window:
            self.parent_view.window.show_view(CheatMenu())


class ExitButton(BaseButton):
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
        arcade.exit()
        exit()


class InstructionsButton(BaseButton):
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
        instructions = InstructionsScreen(previous_view=self.parent_view)
        if self.parent_view.window:
            self.parent_view.window.show_view(instructions)


class HighscoresButton(BaseButton):
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
            parent_view=parent_view,
        )

    def on_click(self) -> None:
        if self.parent_view.window:
            self.parent_view.window.show_view(HighscoresScreen())


class PlayButton(BaseButton):
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
        self.parent_view.window.game_session = GameEngine()
        self.parent_view.window.show_view(self.parent_view.window.game_session)


class MainMenu(BaseMenu):
    def __init__(self) -> None:
        super().__init__()
        self.background = arcade.load_texture("assets/sprites/main_menu/ocean.png")

    def build_ui(self) -> None:

        logo_button = LogoButton(
            center_x=640,
            center_y=600,
            sprite_path=self.window.asset_manager.textures["logo"],
            parent_view=self,
        )

        play_button = PlayButton(
            center_x=640,
            center_y=475,
            sprite_path=self.window.asset_manager.textures["start_button"],
            parent_view=self
        )

        highscores_button = HighscoresButton(
            center_x=640,
            center_y=375,
            sprite_path=(
                self.window.asset_manager.textures["highscores_button"]
            ),
            parent_view=self
        )

        instructions_button = InstructionsButton(
            center_x=640,
            center_y=275,
            sprite_path=(
                self.window.asset_manager.textures["instructions_button"]
            ),
            parent_view=self
        )

        cheat_button = CheatButton(
            center_x=640,
            center_y=175,
            sprite_path=self.window.asset_manager.textures["cheat_button"],
            parent_view=self
        )

        exit_button = ExitButton(
            center_x=640,
            center_y=75,
            sprite_path=self.window.asset_manager.textures["exit_button"],
            parent_view=self
        )

        self.animation()

        self.button_list.append(logo_button)
        self.button_list.append(play_button)
        self.button_list.append(highscores_button)
        self.button_list.append(instructions_button)
        self.button_list.append(cheat_button)
        self.button_list.append(exit_button)

    def animation(self):
        level_manager = LevelManager(self.window)
        textures_list = load_sprite_sheet(
        textures=level_manager.asset_manager.textures["player"],
        sprite_width=192/6, sprite_height=32, sprites_columns=6,
        sprites_count=6)
        pacman = Pacman(
            center_x=-30,
            center_y=120,
            textures_list=textures_list,
            parent_view=self
        )
        self.button_list.append(pacman)
        pacman.change_x = 1000 / 700

        level_manager = LevelManager(self.window)
        textures_list = load_sprite_sheet(
        textures=level_manager.asset_manager.textures["enemy_cat_move"],
        sprite_width=192/6, sprite_height=32, sprites_columns=6,
        sprites_count=6)
        cat = Pursuit(
            center_x=-110,
            center_y=120,
            textures_list=textures_list,
            parent_view=self
        )
        cat.scale_x = -1.7
        self.button_list.append(cat)
        cat.change_x = 1000 / 350


        level_manager = LevelManager(self.window)
        textures_list = load_sprite_sheet(
        textures=level_manager.asset_manager.textures["enemy_fox_move"],
        sprite_width=192/6, sprite_height=32, sprites_columns=6,
        sprites_count=6)
        fox = Pursuit(
            center_x=-190,
            center_y=120,
            textures_list=textures_list,
            parent_view=self
        )
        fox.scale_x = -1.7
        self.button_list.append(fox)
        fox.change_x = 1000 / 350

        level_manager = LevelManager(self.window)
        textures_list = load_sprite_sheet(
        textures=level_manager.asset_manager.textures["enemy_rat_move"],
        sprite_width=192/6, sprite_height=32, sprites_columns=6,
        sprites_count=6)
        rat = Pursuit(
            center_x=-270,
            center_y=120,
            textures_list=textures_list,
            parent_view=self
        )
        rat.scale_x = -1.7
        self.button_list.append(rat)
        rat.change_x = 1000 / 350

        level_manager = LevelManager(self.window)
        textures_list = load_sprite_sheet(
        textures=level_manager.asset_manager.textures["enemy_dog_move"],
        sprite_width=192/6, sprite_height=32, sprites_columns=6,
        sprites_count=6)
        dog = Pursuit(
            center_x=-350,
            center_y=120,
            textures_list=textures_list,
            parent_view=self
        )
        dog.scale_x = -1.7
        self.button_list.append(dog)
        dog.change_x = 1000 / 350

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
            exit()

    def on_update(self, delta_time):
        self.button_list.update()
        for sprite in self.button_list:
            if isinstance(sprite, LogoButton) or isinstance(sprite, Pacman):
                sprite.on_update(delta_time)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT)
        )
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()
