# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_menu.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:37:31 by roandrie        #+#    #+#               #
#  Updated: 2026/06/05 16:57:15 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from .intro_screen import IntroScreen
from src.audio import AudioManager
from src.renderer.ui.highscores_screen import HighscoresScreen
from src.renderer.ui.instructions_screen import InstructionsScreen
import math
from src.renderer.screen_settings import ScreenSettings
from src.utils import load_sprite_sheet


class Pursuit(arcade.Sprite):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 parent_view: arcade.View,
                 textures_list: list[arcade.Texture],
                 scale: float = 1.8) -> None:

        super().__init__(path_or_texture=textures_list[0],
                         center_x=center_x,
                         center_y=center_y,
                         scale=scale)

        self.parent_view = parent_view
        self.textures_list = textures_list

    def on_update(self, delta_time: float) -> None:
        # Move the ghosts, if they go out of the screen they come back on the
        # other side
        self.center_x += self.change_x
        if self.center_x > ScreenSettings.WIDTH + (self.width / 2):
            self.center_x = -30


class Pacman(arcade.Sprite):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 parent_view: arcade.View,
                 textures_list: list[arcade.Texture],
                 scale: float = 1.8) -> None:

        super().__init__(path_or_texture=textures_list[0],
                         center_x=center_x,
                         center_y=center_y,
                         scale=scale)

        self.parent_view = parent_view
        self.textures_list = textures_list
        self.current_texture_index = 0
        self.animation_time = 0.0
        self.animation_speed = 0.1

    def on_update(self, delta_time: float) -> None:
        # Move the pacman, if he goes out of the screen he comes back on the
        # other side
        self.center_x += self.change_x
        if self.center_x > ScreenSettings.WIDTH + (self.width / 2):
            self.center_x = -30

        # Animate pacman beack and wings
        self.animation_time += delta_time
        if self.animation_time >= self.animation_speed:
            self.animation_time -= self.animation_speed
            self.current_texture_index = ((self.current_texture_index + 1)
                                          % len(self.textures_list))
            self.texture = self.textures_list[self.current_texture_index]


class LogoButton(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View,
                 scale: float = 1.3) -> None:

        super().__init__(center_x=center_x,
                         center_y=center_y,
                         sprite_path=sprite_path,
                         parent_view=parent_view)

        self.scale = scale
        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view
        self.is_landing = False
        self.total_time = 0.0
        self.gullman = False
        self.sprite_path = sprite_path

    def on_update(self, delta_time: float) -> None:
        # Animate logo
        self.total_time += delta_time
        if self.is_landing:
            if abs(self.scale_x - 1.0) < 0.01:
                self.scale_x = 1.0
                self.scale_y = 1.0
                self.is_landing = False
        else:
            t = self.total_time
            self.scale_x = 1.0 + math.sin(t * 3) * 0.05
            self.scale_y = 1.0 + math.cos(t * 3) * 0.05

    def on_click(self) -> None:
        # Easter egg : change logo clicking on it
        if self.gullman is False:
            path = self.parent_view.window.asset_manager.textures["gullman"]
        else:
            path = self.parent_view.window.asset_manager.textures["logo"]
        self.texture = arcade.load_texture(path)
        self.gullman = not self.gullman
        if (hasattr(self.parent_view, 'musics')
           and hasattr(self.parent_view, 'i')):
            song = self.parent_view.musics[self.parent_view.i]
        if hasattr(self.parent_view, 'audio_manager'):
            self.parent_view.audio_manager.stop_sound(song)
        if (hasattr(self.parent_view, 'musics')
           and hasattr(self.parent_view, 'i')):
            if self.parent_view.i + 1 >= len(self.parent_view.musics):
                self.parent_view.i = 0
            else:
                self.parent_view.i += 1
        if hasattr(self.parent_view, '_play_music'):
            self.parent_view._play_music()

    def check_hover(self, x: float, y: float) -> None:
        # Cancel the light gray color when the mouse is on the sprite to hide
        # the easter egg
        pass


class CheatButton(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x,
                         center_y=center_y,
                         sprite_path=sprite_path,
                         parent_view=parent_view)

    def on_click(self) -> None:
        # Go on cheat menu
        from src.renderer.ui.cheat_menu import CheatMenu
        if hasattr(self.parent_view, 'background'):
            cheat = CheatMenu(previous_view=self.parent_view,
                              background=self.parent_view.background)
        if self.parent_view.window:
            self.parent_view.window.show_view(cheat)


class ExitButton(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x,
                         center_y=center_y,
                         sprite_path=sprite_path,
                         parent_view=parent_view)

    def on_click(self) -> None:
        # Close arcade
        arcade.exit()
        exit()


class InstructionsButton(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x,
                         center_y=center_y,
                         sprite_path=sprite_path,
                         parent_view=parent_view)

    def on_click(self) -> None:
        # Go on instructions menu
        instructions = InstructionsScreen(previous_view=self.parent_view)
        if self.parent_view.window:
            self.parent_view.window.show_view(instructions)


class HighscoresButton(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View,) -> None:

        super().__init__(center_x=center_x,
                         center_y=center_y,
                         sprite_path=sprite_path,
                         parent_view=parent_view,)

    def on_click(self) -> None:
        # Go on highscores menu
        if self.parent_view.window:
            self.parent_view.window.show_view(
                HighscoresScreen(previous_view=self.parent_view)
            )


class PlayButton(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x,
                         center_y=center_y,
                         sprite_path=sprite_path,
                         parent_view=parent_view)

    def on_click(self) -> None:
        # Stop the menu music
        song = self.parent_view.musics[self.parent_view.i]
        self.parent_view.audio_manager.stop_sound(song)

        # Start the Intro screen instead of the game
        intro = IntroScreen(previous_view=self.parent_view)
        self.parent_view.window.show_view(intro)


class MainMenu(BaseMenu):
    # Initialise a count of key A pressed
    count_touch_A: int = 0

    def __init__(self) -> None:
        super().__init__()
        # Set a beach background
        self.background: arcade.Texture = arcade.load_texture(
            self.window.asset_manager.textures["ocean"])
        self.menu_time: float = 0.0
        self.audio_manager: AudioManager = self.window.audio_player

        self.musics = ['music_mainmenu', 'music_joy', 'music_cave',
                       'music_suspens', 'music_suspens2', 'music_strange',
                       'music_jungle', 'music_pacman']
        self.time_musics = [66, 38, 52, 52, 52, 52, 52, 52, 33]
        self.i = 0
        self.y = 2

        self._play_music()

    def build_ui(self) -> None:
        # Create buttons

        self.logo_button = LogoButton(
            center_x=ScreenSettings.WIDTH // 2, center_y=600,
            sprite_path=self.window.asset_manager.textures["logo"],
            parent_view=self)

        self.play_button = PlayButton(
            center_x=ScreenSettings.WIDTH // 2, center_y=475,
            sprite_path=self.window.asset_manager.textures["start_button"],
            parent_view=self)

        self.highscores_button = HighscoresButton(
            center_x=ScreenSettings.WIDTH // 2, center_y=375,
            sprite_path=(
                self.window.asset_manager.textures["highscores_button"]),
            parent_view=self)

        self.instructions_button = InstructionsButton(
            center_x=ScreenSettings.WIDTH // 2, center_y=275,
            sprite_path=(
                self.window.asset_manager.textures["instructions_button"]),
            parent_view=self)

        # Create the secret way to have the cheat mode
        if MainMenu.count_touch_A >= 3:
            self.audio_manager.play_sound('bruit')

            self.button_list.clear()
            cheat_button = CheatButton(
                center_x=ScreenSettings.WIDTH // 2, center_y=175,
                sprite_path=self.window.asset_manager.textures["cheat_button"],
                parent_view=self)
            self.exit_button = ExitButton(
                center_x=ScreenSettings.WIDTH // 2, center_y=75,
                sprite_path=self.window.asset_manager.textures["exit_button"],
                parent_view=self)
            self.button_list.append(cheat_button)
        else:
            self.exit_button = ExitButton(
                center_x=ScreenSettings.WIDTH // 2, center_y=175,
                sprite_path=self.window.asset_manager.textures["exit_button"],
                parent_view=self)

        # Create an animation on the background
        self.animation()

        # Add all buttons on a button list
        self.button_list.append(self.logo_button)
        self.button_list.append(self.play_button)
        self.button_list.append(self.highscores_button)
        self.button_list.append(self.instructions_button)
        self.button_list.append(self.exit_button)

    def animation(self) -> None:
        # Animate Pacman
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["player"],
            sprite_width=int(192/6), sprite_height=32, sprites_columns=6,
            sprites_count=6)
        pacman = Pacman(center_x=-30, center_y=120,
                        textures_list=textures_list, parent_view=self)

        # Animate cat ghost
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["enemy_cat_move"],
            sprite_width=int(128/4), sprite_height=32, sprites_columns=4,
            sprites_count=4)
        cat = Pursuit(center_x=-110, center_y=120,
                      textures_list=textures_list, parent_view=self)
        self.button_list.append(cat)
        cat.change_x = 1000 / 750

        # Animate gox ghost
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["enemy_fox_move"],
            sprite_width=int(128/4), sprite_height=32, sprites_columns=4,
            sprites_count=4)
        fox = Pursuit(center_x=-190, center_y=120,
                      textures_list=textures_list, parent_view=self)
        self.button_list.append(fox)
        fox.change_x = 1000 / 750

        # Animate rat ghost
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["enemy_rat_move"],
            sprite_width=int(128/4), sprite_height=32, sprites_columns=4,
            sprites_count=4)
        rat = Pursuit(center_x=-270, center_y=120,
                      textures_list=textures_list, parent_view=self)
        self.button_list.append(rat)
        rat.change_x = 1000 / 750

        # Animate dog ghost
        textures_list = load_sprite_sheet(
            textures=self.window.asset_manager.textures["enemy_dog_move"],
            sprite_width=int(128/4), sprite_height=32, sprites_columns=4,
            sprites_count=4)
        dog = Pursuit(center_x=-350, center_y=120,
                      textures_list=textures_list, parent_view=self)
        self.button_list.append(dog)
        dog.change_x = 1000 / 750
        self.button_list.append(pacman)
        pacman.change_x = 1000 / 700

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            # Close arcade
            arcade.exit()
            exit()

        if symbol == arcade.key.A:
            # With 3 A : activate cheat mode
            MainMenu.count_touch_A += 1
            if MainMenu.count_touch_A == 3:
                self.build_ui()

        if symbol == arcade.key.DOWN:
            self.y += 1
        if symbol == arcade.key.UP:
            self.y -= 1

        if self.y < 0:
            self.y = 4
        if self.y == 5:
            self.y = 0
        if self.y == 1:
            self.play_button.check_hover(self.play_button.center_x,
                                         self.play_button.center_y)
        else:
            self.play_button.color = arcade.color.WHITE
        if self.y == 2:
            self.highscores_button.check_hover(self.highscores_button.center_x,
                                               self.highscores_button.center_y)
        else:
            self.highscores_button.color = arcade.color.WHITE
        if self.y == 3:
            self.instructions_button.check_hover(
                self.instructions_button.center_x,
                self.instructions_button.center_y)
        else:
            self.instructions_button.color = arcade.color.WHITE
        if self.y == 4:
            self.exit_button.check_hover(self.exit_button.center_x,
                                         self.exit_button.center_y)
        else:
            self.exit_button.color = arcade.color.WHITE

        if symbol == arcade.key.ENTER or symbol == arcade.key.SPACE:
            if self.y == 0:
                self.logo_button.on_click()
            if self.y == 1:
                self.play_button.on_click()
            if self.y == 2:
                self.highscores_button.on_click()
            if self.y == 3:
                self.instructions_button.on_click()
            if self.y == 4:
                self.exit_button.on_click()

    def on_update(self, delta_time: float) -> None:
        # Update for animation
        self.menu_time += delta_time
        self.button_list.update()
        for sprite in self.button_list:
            if hasattr(sprite, "on_update"):
                sprite.on_update(delta_time)

        self._music_duration -= int(delta_time)

        if self._music_duration <= 0.0:
            self._play_music()

    def on_draw(self) -> None:
        self.clear()

        # Draw the beach background
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT)
        )

        # Draw all the sprites
        self.button_list.draw()

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _play_music(self) -> None:
        self._music_duration = self.time_musics[self.i]
        self.audio_manager.play_sound(
            str(self.musics[self.i]), 0.8, True
        )
