# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  base_button.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:31:51 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 19:33:57 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from abc import ABC, abstractmethod
from pathlib import Path


class BaseButton(arcade.Sprite, ABC):
    def __init__(
        self, center_x: float, center_y: float, sprite_path: Path,
        scale: float = 1.0
    ) -> None:

        # Visual representation (Composition)
        self.sprite = arcade.Sprite(filename=sprite_path, scale=scale)

        # Sync visual position with logical position
        self.sprite.center_x = center_x
        self.sprite.center_y = center_y

    def check_hover(self, x: float, y: float) -> None:
        if self.collides_with_point((x, y)):
            self.color = arcade.color.LIGHT_GRAY
        else:
            self.color = arcade.color.WHITE

    @abstractmethod
    def on_click(self) -> None:
        pass
