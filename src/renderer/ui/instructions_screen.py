# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  instructions_screen.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:52:32 by anacharp        #+#    #+#               #
#  Updated: 2026/05/28 11:36:21 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.utils import load_sprite_sheet
from src.game_engine.level_manager import LevelManager
from src.renderer.screen_settings import ScreenSettings


class Ghosts(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.5
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class Pacman(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.5
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class Assets(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.8
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class Instructions(BaseButton):
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
            self.parent_view.window.show_view(self.parent_view.previous_view)


class InstructionsScreen(BaseMenu):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()
        self.previous_view = previous_view
        self.background = arcade.load_texture(
            "assets/sprites/main_menu/ocean.png"
        )

    def build_ui(self) -> None:
        instructions = Instructions(
            center_x=640,
            center_y=600,
            sprite_path=(
                self.window.asset_manager.textures["instructions_button"]
            ),
            parent_view=self
        )
        self.button_list.append(instructions)

        self.write_commands()
        self.write_rules()
        self.write_player()
        self.write_pacgums()
        self.write_ghosts()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            if self.window:
                self.window.show_view(self.previous_view)

    def write_ghosts(self) -> None:
        level_manager = LevelManager(self.window)
        cat_ghost_txt = arcade.Text(
            text="ST GLORIUS RICTUS IV =", x=742, y=280,
            color=arcade.color.GRAY, font_size=15,
            font_name="Press Start 2P"
        )
        textures_list = load_sprite_sheet(
            textures=level_manager.asset_manager.textures["enemy_cat_move"],
            sprite_width=32, sprite_height=32,
            sprites_columns=1, sprites_count=1
        )

        cat_ghost = Ghosts(
            center_x=1240,
            center_y=295,
            sprite_path=textures_list[0],
            parent_view=self
        )

        self.text_lst.append(cat_ghost_txt)
        self.button_list.append(cat_ghost)

        fox_ghost_txt = arcade.Text(
            text="CHIPEUR =", x=1003, y=210,
            color=arcade.color.SAFETY_ORANGE, font_size=15,
            font_name="Press Start 2P"
        )

        textures_list = load_sprite_sheet(
            textures=level_manager.asset_manager.textures["enemy_fox_move"],
            sprite_width=32, sprite_height=32,
            sprites_columns=1, sprites_count=1
        )

        fox_ghost = Ghosts(
            center_x=1240,
            center_y=225,
            sprite_path=textures_list[0],
            parent_view=self
        )

        self.text_lst.append(fox_ghost_txt)
        self.button_list.append(fox_ghost)

        rat_ghost_txt = arcade.Text(
            text="RATATOUILLE =", x=923, y=140,
            color=arcade.color.PASTEL_GRAY,
            font_size=15, font_name="Press Start 2P"
        )

        textures_list = load_sprite_sheet(
            textures=level_manager.asset_manager.textures["enemy_rat_move"],
            sprite_width=32, sprite_height=32,
            sprites_columns=1, sprites_count=1
        )

        rat_ghost = Ghosts(
            center_x=1240,
            center_y=155,
            sprite_path=textures_list[0],
            parent_view=self
        )
        self.text_lst.append(rat_ghost_txt)
        self.button_list.append(rat_ghost)

        dog_ghost_txt = arcade.Text(
            text="FLEUR =", x=1043, y=70,
            color=arcade.color.APRICOT, font_size=15,
            font_name="Press Start 2P")

        textures_list = load_sprite_sheet(
            textures=level_manager.asset_manager.textures["enemy_dog_move"],
            sprite_width=32, sprite_height=32,
            sprites_columns=1, sprites_count=1
        )

        dog_ghost = Ghosts(
            center_x=1240,
            center_y=85,
            sprite_path=textures_list[0],
            parent_view=self
        )
        self.text_lst.append(dog_ghost_txt)
        self.button_list.append(dog_ghost)

    def write_pacgums(self) -> None:
        fish_txt = arcade.Text(
            text="PACGUMS =", x=1000, y=425,
            color=arcade.color.PASTEL_GREEN, font_size=15,
            font_name="Press Start 2P"
        )

        fish = Assets(
            center_x=1240,
            center_y=440,
            sprite_path=self.window.asset_manager.textures["pacgum"],
            parent_view=self
        )
        self.text_lst.append(fish_txt)
        self.button_list.append(fish)

        burger_txt = arcade.Text(
            text="SUPER_PACGUMS =", x=880, y=355,
            color=arcade.color.GREEN, font_size=15,
            font_name="Press Start 2P"
        )

        burger = Assets(
            center_x=1240,
            center_y=370,
            sprite_path=self.window.asset_manager.textures["super_pacgum"],
            parent_view=self
        )
        self.text_lst.append(burger_txt)
        self.button_list.append(burger)

    def write_player(self) -> None:
        level_manager = LevelManager(self.window)
        pacman_txt = arcade.Text(
            text="PACMAN =", x=1020, y=505,
            color=arcade.color.YELLOW_ROSE, font_size=15,
            font_name="Press Start 2P"
        )

        textures_list = load_sprite_sheet(
            textures=level_manager.asset_manager.textures["player"],
            sprite_width=32, sprite_height=32,
            sprites_columns=1, sprites_count=1
        )

        pacman = Pacman(
            center_x=1240,
            center_y=520,
            sprite_path=textures_list[0],
            parent_view=self
        )
        self.text_lst.append(pacman_txt)
        self.button_list.append(pacman)

    def write_commands(self) -> None:
        commands = arcade.Text(text="COMMANDS:", x=15, y=520,
                               color=arcade.color.BABY_BLUE, font_size=20,
                               font_name="Press Start 2P")
        play = arcade.Text(text="- Play with WASD or ←↑↓→", x=15, y=470,
                           color=arcade.color.WHITE, font_size=15,
                           font_name="Press Start 2P")
        pause = arcade.Text(text="- Press ESC to pause", x=15, y=420,
                            color=arcade.color.WHITE, font_size=15,
                            font_name="Press Start 2P")
        exit = arcade.Text(text="- Press ESC to exit instructions", x=15,
                           y=370, color=arcade.color.WHITE, font_size=15,
                           font_name="Press Start 2P")
        self.text_lst.append(commands)
        self.text_lst.append(play)
        self.text_lst.append(pause)
        self.text_lst.append(exit)

    def write_rules(self) -> None:
        rules = arcade.Text(text="RULES:", x=15, y=300,
                            color=arcade.color.RED, font_size=20,
                            font_name="Press Start 2P")
        rule1 = arcade.Text(text="- Pacman avoids ghosts", x=15, y=250,
                            color=arcade.color.WHITE, font_size=15,
                            font_name="Press Start 2P")
        rule2 = arcade.Text(text="- Pacgums give you points", x=15, y=200,
                            color=arcade.color.WHITE, font_size=15,
                            font_name="Press Start 2P")
        rule3 = arcade.Text(text="- SuperPacgums give you more points", x=15,
                            y=150,
                            color=arcade.color.WHITE, font_size=15,
                            font_name="Press Start 2P")
        rule4 = arcade.Text(
                text="  and eating ghosts power", x=15,
                y=100, color=arcade.color.WHITE, font_size=15,
                font_name="Press Start 2P")
        rule5 = arcade.Text(text="- Ghosts give you more points", x=15, y=50,
                            color=arcade.color.WHITE, font_size=15,
                            font_name="Press Start 2P")
        self.text_lst.append(rules)
        self.text_lst.append(rule1)
        self.text_lst.append(rule2)
        self.text_lst.append(rule3)
        self.text_lst.append(rule4)
        self.text_lst.append(rule5)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT)
        )
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

    def on_update(self, delta_time):
        self.button_list.update()
        for sprite in self.button_list:
            if isinstance(sprite, Instructions):
                sprite.on_update(delta_time)
