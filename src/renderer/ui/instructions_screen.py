# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  instructions_screen.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:52:32 by anacharp        #+#    #+#               #
#  Updated: 2026/05/30 12:39:49 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.utils import load_sprite_sheet
from src.renderer.screen_settings import ScreenSettings
from typing import Union


class Ghosts(arcade.Sprite):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Union[arcade.Texture, Path],
                 parent_view: arcade.View,
                 scale: float = 1.5) -> None:

        super().__init__(path_or_texture=sprite_path, scale=scale)

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class Pacman(arcade.Sprite):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Union[arcade.Texture, Path],
                 parent_view: arcade.View,
                 scale: float = 1.5) -> None:

        super().__init__(path_or_texture=sprite_path, scale=scale)

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class Assets(arcade.Sprite):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Union[arcade.Texture, Path],
                 parent_view: arcade.View,
                 scale: float = 1.8) -> None:

        super().__init__(path_or_texture=sprite_path, scale=scale)

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class Instructions(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Union[arcade.Texture, Path],
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x, center_y=center_y,
                         sprite_path=sprite_path, parent_view=parent_view)

    def on_click(self) -> None:
        # Return to main menu
        from src.renderer.ui.main_menu import MainMenu
        if self.parent_view.window:
            self.parent_view.window.show_view(MainMenu())


class InstructionsScreen(BaseMenu):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()
        self.previous_view = previous_view

        # Initialise the beach background
        self.background = arcade.load_texture(
            "assets/sprites/main_menu/ocean.png"
        )

    def build_ui(self) -> None:
        # Create all sprites and texts
        instructions = Instructions(
            center_x=ScreenSettings.WIDTH // 2,
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
        # Return to main menu
        if symbol == arcade.key.ESCAPE:
            if self.window:
                self.window.show_view(self.previous_view)

    def write_ghosts(self) -> None:

        # Create cat sprite and write it's name
        cat_ghost_txt = arcade.Text(text="ST GLORIUS RICTUS IV =",
                                    x=ScreenSettings.WIDTH - 538,
                                    y=280, color=arcade.color.GRAY,
                                    font_size=15, font_name="Press Start 2P")
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["enemy_cat_move"],
            sprite_width=32, sprite_height=32,
            sprites_columns=1, sprites_count=1)
        cat_ghost = Ghosts(center_x=ScreenSettings.WIDTH - 40, center_y=295,
                           sprite_path=textures_list[0], parent_view=self)

        # Create fox sprite and write it's name
        fox_ghost_txt = arcade.Text(text="CHIPEUR =",
                                    x=ScreenSettings.WIDTH - 277, y=210,
                                    color=arcade.color.SAFETY_ORANGE,
                                    font_size=15, font_name="Press Start 2P")
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["enemy_fox_move"],
            sprite_width=32, sprite_height=32, sprites_columns=1,
            sprites_count=1)
        fox_ghost = Ghosts(center_x=ScreenSettings.WIDTH - 40, center_y=225,
                           sprite_path=textures_list[0], parent_view=self)

        # Create rat sprite and write it's name
        rat_ghost_txt = arcade.Text(text="RATATOUILLE =",
                                    x=ScreenSettings.WIDTH - 357, y=140,
                                    color=arcade.color.PASTEL_GRAY,
                                    font_size=15, font_name="Press Start 2P")
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["enemy_rat_move"],
            sprite_width=32, sprite_height=32, sprites_columns=1,
            sprites_count=1)
        rat_ghost = Ghosts(center_x=ScreenSettings.WIDTH - 40, center_y=155,
                           sprite_path=textures_list[0], parent_view=self)

        # Create dog sprite and write it's name
        dog_ghost_txt = arcade.Text(text="FLEUR =",
                                    x=ScreenSettings.WIDTH - 237, y=70,
                                    color=arcade.color.APRICOT, font_size=15,
                                    font_name="Press Start 2P")
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["enemy_dog_move"],
            sprite_width=32, sprite_height=32, sprites_columns=1,
            sprites_count=1)
        dog_ghost = Ghosts(center_x=ScreenSettings.WIDTH - 40, center_y=85,
                           sprite_path=textures_list[0], parent_view=self)

        # Add all texts on a text list and all sprites on a button list
        self.text_lst.append(cat_ghost_txt)
        self.button_list.append(cat_ghost)
        self.text_lst.append(fox_ghost_txt)
        self.button_list.append(fox_ghost)
        self.text_lst.append(rat_ghost_txt)
        self.button_list.append(rat_ghost)
        self.text_lst.append(dog_ghost_txt)
        self.button_list.append(dog_ghost)

    def write_pacgums(self) -> None:
        # Create pacgum sprite and write it's name
        fish_txt = arcade.Text(text="PACGUMS =", x=ScreenSettings.WIDTH - 280,
                               y=425,
                               color=arcade.color.PASTEL_GREEN, font_size=15,
                               font_name="Press Start 2P")
        fish = Assets(center_x=ScreenSettings.WIDTH - 40, center_y=440,
                      sprite_path=self.window.asset_manager.textures["pacgum"],
                      parent_view=self)

        # Create super pacgum sprite and write it's name
        burger_txt = arcade.Text(
            text="SUPER_PACGUMS =", x=ScreenSettings.WIDTH - 400, y=355,
            color=arcade.color.GREEN, font_size=15,
            font_name="Press Start 2P"
        )
        burger = Assets(
            center_x=ScreenSettings.WIDTH - 40,
            center_y=370,
            sprite_path=self.window.asset_manager.textures["super_pacgum"],
            parent_view=self)

        # Add all texts on a text list and all sprites on a button list
        self.text_lst.append(fish_txt)
        self.button_list.append(fish)
        self.text_lst.append(burger_txt)
        self.button_list.append(burger)

    def write_player(self) -> None:
        # Create pacman sprite and write it's name
        pacman_txt = arcade.Text(text="PACMAN =", x=ScreenSettings.WIDTH - 260,
                                 y=505,
                                 color=arcade.color.YELLOW_ROSE, font_size=15,
                                 font_name="Press Start 2P")
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["player"],
            sprite_width=32, sprite_height=32, sprites_columns=1,
            sprites_count=1)
        pacman = Pacman(center_x=ScreenSettings.WIDTH - 40, center_y=520,
                        sprite_path=textures_list[0], parent_view=self)

        # Add text on a text list and the sprite on a button list
        self.text_lst.append(pacman_txt)
        self.button_list.append(pacman)

    def write_commands(self) -> None:
        # Write commands text
        commands = arcade.Text(text="COMMANDS:", x=15, y=520,
                               color=arcade.color.BABY_BLUE, font_size=20,
                               font_name="Press Start 2P")
        play = arcade.Text(text="- Play with WASD or ←↑↓→", x=15, y=470,
                           color=arcade.color.WHITE, font_size=15,
                           font_name="Press Start 2P")
        pause = arcade.Text(text="- Press ESC to pause", x=15, y=420,
                            color=arcade.color.WHITE, font_size=15,
                            font_name="Press Start 2P")
        exit = arcade.Text(text="- Press SPACE to skip the countdown", x=15,
                           y=370, color=arcade.color.WHITE, font_size=15,
                           font_name="Press Start 2P")

        # Add text on a text list
        self.text_lst.append(commands)
        self.text_lst.append(play)
        self.text_lst.append(pause)
        self.text_lst.append(exit)

    def write_rules(self) -> None:
        # Write rules text
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
        rule4 = arcade.Text(text="  and eating ghosts power", x=15,
                            y=100, color=arcade.color.WHITE, font_size=15,
                            font_name="Press Start 2P")
        rule5 = arcade.Text(text="- Ghosts give you more points", x=15, y=50,
                            color=arcade.color.WHITE, font_size=15,
                            font_name="Press Start 2P")

        # Add text on a text list
        self.text_lst.append(rules)
        self.text_lst.append(rule1)
        self.text_lst.append(rule2)
        self.text_lst.append(rule3)
        self.text_lst.append(rule4)
        self.text_lst.append(rule5)

    def on_draw(self) -> None:
        self.clear()

        # Draw the beach background
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT)
        )

        # Draw all the sprites and the texts
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

    def on_update(self, delta_time: float) -> None:
        # Update the instruction sprite to check if user touch it or not
        self.button_list.update()
        for sprite in self.button_list:
            if isinstance(sprite, Instructions):
                sprite.on_update(delta_time)
