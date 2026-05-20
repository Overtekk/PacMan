# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  instructions_screen.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:52:32 by anacharp        #+#    #+#               #
#  Updated: 2026/05/20 13:13:09 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton


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
        arcade.set_background_color(arcade.color.BLACK)

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
        cat_ghost_txt = arcade.Text(text="CAT GHOST =", x=920, y=280,
                                    color=arcade.color.WHITE, font_size=20)
        cat_ghost = Ghosts(
            center_x=1200,
            center_y=295,
            sprite_path=(
                self.window.asset_manager.textures["cat_enemy"]
            ),
            parent_view=self
        )
        self.text_lst.append(cat_ghost_txt)
        self.button_list.append(cat_ghost)

        fox_ghost_txt = arcade.Text(text="FOX GHOST =", x=920, y=210,
                                    color=arcade.color.WHITE, font_size=20)
        fox_ghost = Ghosts(
            center_x=1200,
            center_y=225,
            sprite_path=(
                self.window.asset_manager.textures["fox_enemy"]
            ),
            parent_view=self
        )
        self.text_lst.append(fox_ghost_txt)
        self.button_list.append(fox_ghost)

        rat_ghost_txt = arcade.Text(text="RAT GHOST =", x=920, y=140,
                                    color=arcade.color.WHITE, font_size=20)
        rat_ghost = Ghosts(
            center_x=1200,
            center_y=155,
            sprite_path=(
                self.window.asset_manager.textures["rat_enemy"]
            ),
            parent_view=self
        )
        self.text_lst.append(rat_ghost_txt)
        self.button_list.append(rat_ghost)

        dog_ghost_txt = arcade.Text(text="DOG GHOST =", x=920, y=70,
                                    color=arcade.color.WHITE, font_size=20)
        dog_ghost = Ghosts(
            center_x=1200,
            center_y=85,
            sprite_path=(
                self.window.asset_manager.textures["dog_enemy"]
            ),
            parent_view=self
        )
        self.text_lst.append(dog_ghost_txt)
        self.button_list.append(dog_ghost)

    def write_pacgums(self) -> None:
        fish_txt = arcade.Text(text="PACGUMS =", x=1032, y=430,
                               color=arcade.color.WHITE, font_size=20)
        fish = Assets(
            center_x=1240,
            center_y=440,
            sprite_path=(
                self.window.asset_manager.textures["pacgum"]
            ),
            parent_view=self
        )
        self.text_lst.append(fish_txt)
        self.button_list.append(fish)

        burger_txt = arcade.Text(text="SUPER_PACGUMS =", x=930, y=360,
                                 color=arcade.color.WHITE, font_size=20)
        burger = Assets(
            center_x=1240,
            center_y=370,
            sprite_path=(
                self.window.asset_manager.textures["super_pacgum"]
            ),
            parent_view=self
        )
        self.text_lst.append(burger_txt)
        self.button_list.append(burger)

    def write_player(self) -> None:
        pacman_txt = arcade.Text(text="PACMAN =", x=1050, y=510,
                                 color=arcade.color.WHITE, font_size=20)
        pacman = Pacman(
            center_x=1435,
            center_y=520,
            sprite_path=(
                self.window.asset_manager.textures["player"]
            ),
            parent_view=self
        )
        self.text_lst.append(pacman_txt)
        self.button_list.append(pacman)

    def write_commands(self) -> None:
        commands = arcade.Text(text="COMMANDS:", x=15, y=520,
                               color=arcade.color.WHITE, font_size=20)
        play = arcade.Text(text="- Play with WASD", x=15, y=470,
                           color=arcade.color.WHITE, font_size=15)
        pause = arcade.Text(text="- Press SPACE to pause", x=15, y=420,
                            color=arcade.color.WHITE, font_size=15)
        exit = arcade.Text(text="- Press ESC to exit", x=15, y=370,
                           color=arcade.color.WHITE, font_size=15)
        self.text_lst.append(commands)
        self.text_lst.append(play)
        self.text_lst.append(pause)
        self.text_lst.append(exit)

    def write_rules(self) -> None:
        rules = arcade.Text(text="RULES:", x=15, y=300,
                            color=arcade.color.WHITE, font_size=20)
        rule1 = arcade.Text(text="- Pacman avoids ghosts", x=15, y=250,
                            color=arcade.color.WHITE, font_size=15)
        rule2 = arcade.Text(text="- Pacgums give you points", x=15, y=200,
                            color=arcade.color.WHITE, font_size=15)
        rule3 = arcade.Text(text="- SuperPacgums give you more points", x=15,
                            y=150,
                            color=arcade.color.WHITE, font_size=15)
        rule4 = arcade.Text(
            text="- After eating a SuperPacgum you can eat ghosts", x=15,
            y=100, color=arcade.color.WHITE, font_size=15)
        rule5 = arcade.Text(text="- Ghosts give you more points", x=15, y=50,
                            color=arcade.color.WHITE, font_size=15)
        self.text_lst.append(rules)
        self.text_lst.append(rule1)
        self.text_lst.append(rule2)
        self.text_lst.append(rule3)
        self.text_lst.append(rule4)
        self.text_lst.append(rule5)
