# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  finish_screen.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:43:32 by roandrie        #+#    #+#               #
#  Updated: 2026/06/15 14:44:35 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from src.renderer.screen_settings import ScreenSettings
from pathlib import Path
from src.leaderboard.update_leaderboard import save_score_to_leaderboard
from .base_menu import BaseMenu


class Glasses(arcade.Sprite):
    """
    Animated accessory sprite that slides toward Pac-Man's eyes during victory
    loops.
    """
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 parent_view: arcade.View,
                 sprite_path: arcade.Texture,
                 scale: float = 1.8) -> None:
        """Initializes target position paths and configures the sprite scale
        factor.

        Args:
            center_x (float): Initial horizontal screen position.
            center_y (float): Initial vertical screen position.
            parent_view (arcade.View): View structure managing this asset.
            sprite_path (arcade.Texture): Texture resource reference for the
            glasses.
            scale (float): Bounding box scale multiplier.
        """

        super().__init__(path_or_texture=sprite_path,
                         center_x=center_x,
                         center_y=center_y,
                         scale=scale)

        self.parent_view = parent_view
        self.sprite_path = sprite_path

    def on_update(self, delta_time: float) -> None:
        """Lerps position values toward Pac-Man's eye coordinates.

        Args:
            delta_time (float): Delta frame phase step value.
        """
        # Move the glasses into pacman eyes
        target_x = ScreenSettings.WIDTH // 2 - 292
        target_y = 407

        self.center_x += (target_x - self.center_x) * 0.03
        self.center_y += (target_y - self.center_y) * 0.03

        if (abs(self.center_x - target_x) < 0.5
           and abs(self.center_y - target_y) < 0.5):
            self.center_x = target_x
            self.center_y = target_y


class PacmanVictory(arcade.Sprite):
    """
    Victory screen illustration component showcasing the Pac-Man character.
    """
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View,
                 scale: float = 2.2,
                 anchor_x: str = "center") -> None:
        """Registers anchor points and sizes the victory illustration asset.

        Args:
            center_x (float): Center horizontal pixel coordinate.
            center_y (float): Center vertical pixel coordinate.
            sprite_path (Path): System directory address targeting image files.
            parent_view (arcade.View): View configuration context wrapper.
            scale (float): Geometric rendering resolution factor.
            anchor_x (str): Horizontal boundary anchor lock mode.
        """

        super().__init__(path_or_texture=sprite_path,
                         scale=scale, anchor_x=anchor_x)

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class Victory(arcade.Sprite):
    """
    Overlay title banner text sprite displaying the main 'VICTORY' graphic
    message.
    """
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View,
                 scale: float = 1.5,
                 anchor_x: str = "center") -> None:
        """Initializes positioning fields for the text graphic asset.

        Args:
            center_x (float): Center horizontal pixel coordinate.
            center_y (float): Center vertical pixel coordinate.
            sprite_path (Path): System path targeting structural title
            graphics.
            parent_view (arcade.View): Active window rendering layout phase.
            scale (float): Aspect ratio resolution scaling factor.
            anchor_x (str): Text horizontal bounds lock definition.
        """

        super().__init__(path_or_texture=sprite_path,
                         scale=scale, anchor_x=anchor_x)

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class FinishScreen(BaseMenu):
    """Endgame scoreboard view that logs rankings and captures final player
    names.

    Inherits from BaseMenu to handle data validation pipelines and player
    scoring profiles.
    """
    def __init__(self, score: str, filename: str,
                 previous_view: arcade.View) -> None:
        """Saves player scores and takes an application screen capture to use
        as a background.

        Args:
            score (str): Number tracking total match points converted to
            string format.
            filename (str): Target system database path destination.
            previous_view (arcade.View): The active gameplay loop state
            container.
        """
        super().__init__()
        self.player_name = ""
        self.score = score
        self.filename = filename
        self.previous_view = previous_view
        image = arcade.get_image()
        self.background = arcade.Texture(image)

    def build_ui(self) -> None:
        """
        Populates the layout engine with Victory banners and text graphic
        instances.
        """

        # Set the 'Victory' sprite
        victory = Victory(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=580,
            sprite_path=self.window.asset_manager.textures["victory_screen"],
            parent_view=self)

        # Set the pacman winner sprite
        pacman = PacmanVictory(
            center_x=ScreenSettings.WIDTH // 2 - 300,
            center_y=380,
            sprite_path=self.window.asset_manager.textures["pacman_victory"],
            parent_view=self)

        # Write some text
        score = arcade.Text(text="SCORE", x=ScreenSettings.WIDTH // 2, y=410,
                            color=arcade.color.WHITE, font_size=40,
                            font_name="Press Start 2P",
                            anchor_x="center")
        nb = arcade.Text(text=str((int(self.score))),
                         x=ScreenSettings.WIDTH // 2, y=335,
                         color=arcade.color.YELLOW, font_size=40,
                         font_name="Press Start 2P",
                         anchor_x="center")
        enter_name = arcade.Text(text="SAVE YOUR NAME",
                                 x=ScreenSettings.WIDTH // 2, y=230,
                                 color=arcade.color.WHITE, font_size=40,
                                 font_name="Press Start 2P",
                                 anchor_x="center")
        glasses = Glasses(center_x=100, center_y=ScreenSettings.HEIGHT-50,
                          sprite_path=(
                            self.window.asset_manager.textures["glasses"]),
                          parent_view=self)

        # Add all texts on a text list and all buttons on a button list
        self.text_lst.append(score)
        self.text_lst.append(nb)
        self.text_lst.append(enter_name)
        self.button_list.append(victory)
        self.button_list.append(pacman)
        self.button_list.append(glasses)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # Enter name to save the score in the highscores list

        if len(self.player_name) < 10:
            # User can only use alpha characters
            if arcade.key.A <= symbol <= arcade.key.Z:
                maj = modifiers & arcade.key.MOD_CAPSLOCK
                self.player_name += chr(symbol).upper() if maj else chr(symbol)
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_0 or symbol == arcade.key.KEY_0:
                self.player_name += "0"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_1 or symbol == arcade.key.KEY_1:
                self.player_name += "1"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_2 or symbol == arcade.key.KEY_2:
                self.player_name += "2"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_3 or symbol == arcade.key.KEY_3:
                self.player_name += "3"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_4 or symbol == arcade.key.KEY_4:
                self.player_name += "4"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_5 or symbol == arcade.key.KEY_5:
                self.player_name += "5"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_6 or symbol == arcade.key.KEY_6:
                self.player_name += "6"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_7 or symbol == arcade.key.KEY_7:
                self.player_name += "7"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_8 or symbol == arcade.key.KEY_8:
                self.player_name += "8"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.NUM_9 or symbol == arcade.key.KEY_9:
                self.player_name += "9"
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
            if symbol == arcade.key.SPACE:
                self.player_name += " "
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)

        if self.player_name:
            # Delete a character
            if symbol == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]
                if self.text_lst:
                    self.text_lst.pop()

            if symbol == arcade.key.ENTER:
                # Press enter to return on main menu, it saves the name and
                # highscore on the highscores list
                from src.renderer.ui.main_menu import MainMenu

                save_score_to_leaderboard(
                    self.filename, self.player_name,
                    float(self.score),
                    self.previous_view.code_found
                )

                if self.window:
                    self.window.show_view(MainMenu())

    def on_draw(self) -> None:
        self.clear()

        # Draw the game background image
        if self.background:
            arcade.draw_texture_rect(self.background,
                                     arcade.XYWH(self.window.width / 2,
                                                 self.window.height / 2,
                                                 self.window.width,
                                                 self.window.height))

        # Draw a black rectangle with an opacity
        arcade.draw_rect_filled(arcade.XYWH(self.window.width / 2,
                                            self.window.height / 2,
                                            self.window.width,
                                            self.window.height),
                                (0, 0, 0, 180))

        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

    def on_update(self, delta_time: float) -> None:
        self.button_list.update()
        for sprite in self.button_list:
            if isinstance(sprite, Glasses):
                sprite.on_update(delta_time)
