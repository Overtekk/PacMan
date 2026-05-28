# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  base_button.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:31:51 by roandrie        #+#    #+#               #
#  Updated: 2026/05/28 11:53:59 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from abc import ABC, abstractmethod
from pathlib import Path
import random


class BaseButton(arcade.Sprite, ABC):
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
                self.shaking = False
                self.center_x = self.origin_x
                self.center_y = self.origin_y
            else:
                amp = 5 * (self.shake_timer / 1.0)
                self.center_x = self.origin_x + random.uniform(-amp, amp)
                self.center_y = self.origin_y + random.uniform(-amp, amp)

    def check_hover(self, x: float, y: float) -> None:
        if self.collides_with_point((x, y)):
            self.color = arcade.color.LIGHT_GRAY
            if arcade.get_window().time > 120.0:
                self.center_x += 4
                self.center_y += 4
            else:
                self.start_shake(0.2)
        else:
            self.color = arcade.color.WHITE

    @abstractmethod
    def on_click(self) -> None:
        pass
