# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ui_screen.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:44:37 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:49:31 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from src.renderer.screen_settings import ScreenSettings


class DisplayLives(arcade.Sprite):
    """
    UI element sprite designated for drawing player inventory health
    indicators (hearts).
    """
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View,
                 scale: float = 1.5,
                 anchor_x: str = "left",
                 anchor_y: str = "top") -> None:
        """Initializes a life display heart tracking indicator.

        Args:
            center_x (float): Initial horizontal screen position.
            center_y (float): Initial vertical screen position.
            sprite_path (Path): Path referencing the heart image asset.
            parent_view (arcade.View): The active parent UI layout container
            view.
            scale (float): Geometric rendering scale modifier.
            anchor_x (str): Horizontal boundary clipping orientation anchor.
            anchor_y (str): Vertical boundary clipping orientation anchor.
        """

        super().__init__(path_or_texture=sprite_path,
                         scale=scale,
                         anchor_x=anchor_x,
                         anchor_y=anchor_y)

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class UIScreen(BaseMenu):
    """
    Head-Up Display layer updating scores, game timers, levels, and structural
    health metrics.
    """
    def __init__(self, score: str, time: str, nb_lives: int,
                 level: int) -> None:
        """Initializes the heads-up status bars and maps label text positioning
        data.

        Args:
            score (str): Initial string representation of game session score
            points.
            time (str): Initial string representation of the match timer.
            nb_lives (int): Current count of operational player retry tokens.
            level (int): Zero-indexed index representing active level stages.
        """
        super().__init__()
        self.score: str = score
        self.time: str = time
        self.nb_lives: int = nb_lives
        self.display_score: arcade.Text
        self.display_time: arcade.Text
        self.level: int = level

        # Initialise the display of scores, timer and lives
        self.display_score = arcade.Text(text=f"Score: {self.score}",
                                         x=ScreenSettings.WIDTH // 2, y=10,
                                         color=arcade.color.WHITE,
                                         font_size=20,
                                         font_name="Press Start 2P",
                                         anchor_x="center", anchor_y="bottom")
        self.display_time = arcade.Text(text=self.time,
                                        x=ScreenSettings.WIDTH - 10,
                                        y=ScreenSettings.HEIGHT - 10,
                                        color=arcade.color.WHITE,
                                        font_size=20,
                                        font_name="Press Start 2P",
                                        anchor_x="right", anchor_y="top")
        self.more_lives = arcade.Text(text="", x=0, y=0,
                                      color=arcade.color.LIGHT_GRAY,
                                      font_size=30, font_name="Press Start 2P")
        self.display_level = arcade.Text(text=f"Level {self.level+1}",
                                         x=ScreenSettings.WIDTH // 2,
                                         y=ScreenSettings.HEIGHT - 10,
                                         color=arcade.color.WHITE,
                                         font_size=20,
                                         font_name="Press Start 2P",
                                         anchor_x="center", anchor_y="top")

        # Add it into the text list
        self.text_lst.append(self.display_score)
        self.text_lst.append(self.display_time)
        self.text_lst.append(self.more_lives)
        self.text_lst.append(self.display_level)

    def build_ui(self) -> None:
        """Constructs and draws health-specific configuration elements."""
        self.regenerate_lives()

    def regenerate_lives(self) -> None:
        """
        Dynamically builds heart sprite stacks up to a cap of 5, writing text
        overflow extensions beyond.
        """
        # Check the number of lifes and display it
        self.button_list.clear()
        x = 30
        y = ScreenSettings.HEIGHT - 30

        # It can display 5 sprites
        for count in range(1, self.nb_lives + 1):
            if count <= 5:
                lives = DisplayLives(
                    center_x=x, center_y=y,
                    sprite_path=self.window.asset_manager.textures["heart"],
                    parent_view=self
                )
                self.button_list.append(lives)
                x += 45

        # If there is more than 5 lives, it's write '+ nb_of_lives - 5'
        if self.nb_lives > 5:
            self.more_lives.text = f"+{self.nb_lives - 5}"
            self.more_lives.x = x - 10
            self.more_lives.y = y - 22

        # When the user looses lives and there is not more than 5 lives anymore
        # it writes nothing except the sprites
        else:
            self.more_lives.text = ""

    def on_draw(self) -> None:
        """
        Dispatches draw calls onto structural target components and textual
          displays.
        """
        # Draw sprites and texts
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

    def update(self, score: str, time: str, live: int,
               level: int) -> None:
        """Modifies running text fields and dynamically updates live sprites
        during runtime adjustments.

        Args:
            score (str): String format tracking values of active match totals.
            time (str): Raw tracking numerical strings of clock conditions.
            live (int): Numeric representation of active player health
            statuses.
            level (int): Stage iteration tracker parameter.
        """
        # Update the time, the score, and the number of lives
        self.score = str(int(score))
        self.time = str(int(time))
        self.level = level
        self.display_score.text = f"Score: {self.score}"
        self.display_time.text = self.time
        self.display_level.text = f"Level {self.level+1}"
        if int(live) != self.nb_lives:
            self.nb_lives = int(live)
            self.regenerate_lives()
