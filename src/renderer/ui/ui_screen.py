# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ui_screen.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:44:37 by roandrie        #+#    #+#               #
#  Updated: 2026/05/22 15:52:34 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.renderer.screen_settings import ScreenSettings


class DisplayLives(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.5,
        anchor_x="left",
        anchor_y="top"
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale,
            anchor_x=anchor_x,
            anchor_y=anchor_y
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class UIScreen(BaseMenu):
    def __init__(self, score: str, time: str, nb_lives: int) -> None:
        super().__init__()
        self.score = score
        self.time = time
        self.nb_lives = nb_lives

    def build_ui(self) -> None:
        x = 30
        y = ScreenSettings.HEIGHT - 30
        count = 0
        for i in range (self.nb_lives):
            count += 1
            lives = DisplayLives(
                center_x=x,
                center_y=y,
                sprite_path=(
                    self.window.asset_manager.textures["life"]
                ),
                parent_view=self
            )
            self.button_list.append(lives)
            x += 45
            if count >= 3:
                count = 0
                y -= 50
                x = 30

        display_score = arcade.Text(text=f"Score: {self.score}",
                                    x=ScreenSettings.WIDTH - 10,
                                    y=ScreenSettings.HEIGHT - 10,
                                    color=arcade.color.WHITE, font_size=20,
                                    font_name="pressStart2P", anchor_x="right",
                                    anchor_y="top")
        self.text_lst.append(display_score)
        display_time = arcade.Text(text=self.time, x=ScreenSettings.WIDTH -10,
                                   y=10,
                                   color=arcade.color.WHITE,
                                   font_size=20, font_name="pressStart2P",
                                   anchor_x="right", anchor_y="bottom")
        self.text_lst.append(display_time)

    def on_draw(self):
        self.clear()
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()
