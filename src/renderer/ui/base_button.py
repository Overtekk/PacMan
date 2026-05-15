# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  base_button.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:31:51 by roandrie        #+#    #+#               #
#  Updated: 2026/05/15 13:30:03 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from abc import ABC, abstractmethod
from pathlib import Path


class BaseButton(arcade.Sprite, ABC):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.0
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view

    def check_hover(self, x: float, y: float) -> None:
        if self.collides_with_point((x, y)):
            self.color = arcade.color.LIGHT_GRAY
        else:
            self.color = arcade.color.WHITE

    @abstractmethod
    def on_click(self) -> None:
        pass
