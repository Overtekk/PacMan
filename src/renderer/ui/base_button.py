# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  base_button.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:31:51 by roandrie        #+#    #+#               #
#  Updated: 2026/06/02 16:31:06 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
import random

from typing import Union
from abc import ABC, abstractmethod
from pathlib import Path


class BaseButton(arcade.Sprite, ABC):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Union[arcade.Texture, Path],
                 parent_view: arcade.View,
                 scale: float = 1.5) -> None:

        super().__init__(path_or_texture=sprite_path, scale=scale)

        self.origin_x = center_x
        self.origin_y = center_y
        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view
        self.shake_timer = 0.0
        self.shaking = False

    def start_shake(self, duration: float) -> None:
        self.shake_timer = duration
        self.shaking = True

    def on_update(self, delta_time: float) -> None:
        if self.shaking:
            self.shake_timer -= delta_time
            if self.shake_timer <= 0:
                # Stop the shake
                self.shaking = False
                self.center_x = self.origin_x
                self.center_y = self.origin_y
            else:
                # Shake the sprite
                amp = 5 * (self.shake_timer / 1.0)
                self.center_x = self.origin_x + random.uniform(-amp, amp)
                self.center_y = self.origin_y + random.uniform(-amp, amp)

    def check_hover(self, x: float, y: float) -> None:
        # check if the mouse is over the sprite and color it in light gray
        if self.collides_with_point((x, y)):
            self.color = arcade.color.LIGHT_GRAY
            if (hasattr(self.parent_view, "menu_time")
               and self.parent_view.menu_time > 120.0):
                # If the user spend more than 2 minutes on main menu it moves
                # the sprites when you hover the mouse over them
                self.center_x += 4
                self.center_y += 4
            else:
                # The sprites shake when you hover the mouse over them.
                self.start_shake(0.2)
        else:
            self.color = arcade.color.WHITE

    @abstractmethod
    def on_click(self) -> None:
        pass
