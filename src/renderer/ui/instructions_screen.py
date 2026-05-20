# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  instructions_screen.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:52:32 by anacharp        #+#    #+#               #
#  Updated: 2026/05/20 08:53:19 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton


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

        commands = arcade.Text(text="Play with WASD", x= 540, y = 520,
                                color=arcade.color.WHITE, font_size=15)
        pause = arcade.Text(text="Press SPACE to pause", x= 540, y = 470,
                                color=arcade.color.WHITE, font_size=15)
        exit = arcade.Text(text="Press ESC to exit", x= 540, y = 420,
                                color=arcade.color.WHITE, font_size=15)
        self.text_lst.append(commands)
        self.text_lst.append(pause)
        self.text_lst.append(exit)
