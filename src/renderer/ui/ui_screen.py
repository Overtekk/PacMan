# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ui_screen.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:44:37 by roandrie        #+#    #+#               #
#  Updated: 2026/05/26 15:50:18 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
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
        self.display_score = ""
        self.display_time = ""

    def build_ui(self) -> None:
        x = 30
        y = ScreenSettings.HEIGHT - 30
        count = 0
        for _ in range (self.nb_lives):
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

        self.display_score = arcade.Text(text=f"Score: {self.score}",
                                         x=ScreenSettings.WIDTH // 2, y=10,
                                         color=arcade.color.WHITE,
                                         font_size=20,
                                         font_name="pressStart2P",
                                         anchor_x="center", anchor_y="bottom")
        self.text_lst.append(self.display_score)
        self.display_time = arcade.Text(text=self.time,
                                        x=ScreenSettings.WIDTH - 10,
                                        y=ScreenSettings.HEIGHT - 10,
                                        color=arcade.color.WHITE,
                                        font_size=20, font_name="pressStart2P",
                                        anchor_x="right", anchor_y="top")
        self.text_lst.append(self.display_time)

    def on_draw(self):
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

    def update(self, score, time, live):
        self.score = str(score)
        self.time = str(time)
        self.nb_lives = int(live)
        if isinstance(self.display_score, arcade.Text):
            self.display_score.text = f"Score: {self.score}"
        if isinstance(self.display_time, arcade.Text):
            self.display_time.text = self.time
        self.button_list.clear()
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
