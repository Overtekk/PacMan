# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheat_menu.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:43:51 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:21:11 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.renderer.screen_settings import ScreenSettings
from src import game_config
from src.utils import print_log


class BackButton(BaseButton):
    """
    Button subclass managing transitions out of submenus back into previous
    states.
    """
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> None:
        """Restores focus to the parent view object container layer."""
        if self.parent_view.window:
            self.parent_view.window.show_view(self.parent_view)


class ExtraTime(BaseButton):
    """
    Modifier shortcut component injecting duration steps into round clocks.
    """
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_on: arcade.Texture
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_off = self.texture
        self.texture_on = texture_on

        # Check state of the button
        if hasattr(self.parent_view, 'previous_view'):
            if self.parent_view.previous_view.extra_time_activate:
                self.texture = self.texture_on

        self.floating_texts: list[dict[str, Any]] = []

    def on_click(self) -> None:
        """
        Injects time metrics and constructs floating text score components.
        """
        self.texture = self.texture_on
        if hasattr(self.parent_view, 'previous_view'):
            self.parent_view.previous_view.extra_time_activate = True

        current_menu = self.parent_view.window.current_view
        click_x = getattr(current_menu, "last_click_x", self.center_x)
        click_y = getattr(current_menu, "last_click_y", self.center_y)

        new_text: arcade.Text = arcade.Text(
            "+50", click_x, click_y, arcade.color.WHITE_SMOKE, 22,
            1, "center", "Kaph", True, True
        )

        self.floating_texts.append({"text_obj": new_text, "timer": 1.0})

        self._activate_cheat()

    def on_update(self, delta_time: float) -> None:
        """
        Updates font positioning parameters and alpha fading steps over time.
        """
        for item in reversed(self.floating_texts):
            item["timer"] -= delta_time

            if item["timer"] <= 0.0:
                self.floating_texts.remove(item)
            else:
                item["text_obj"].y += 50 * delta_time

                alpha: int = int((item["timer"] / 1.0) * 255)
                item["text_obj"].color = (255, 255, 255, alpha)

    def _activate_cheat(self) -> None:
        """Adjusts engine level timers directly."""
        if game_config.debug_mode:
            print_log("Cheat mode: +50 seconds")

        if hasattr(self.parent_view, 'previous_view'):
            self.parent_view.previous_view.state_manager.time_left += 50


class SpeedUpButton(BaseButton):
    """Button item updating mobile character scalar velocity fields."""
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_on: arcade.Texture
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_off = self.texture
        self.texture_on = texture_on

        # Check state of the button
        if hasattr(self.parent_view, 'previous_view'):
            if self.parent_view.previous_view.speed_up_activate:
                self.texture = self.texture_on

        self.floating_texts: list[dict[str, Any]] = []

    def on_click(self) -> None:
        """
        Applies velocity modifications and schedules dynamic tracking overlays.
        """
        self.texture = self.texture_on
        if hasattr(self.parent_view, 'previous_view'):
            self.parent_view.previous_view.speed_up_activate = True

        current_menu = self.parent_view.window.current_view
        click_x = getattr(current_menu, "last_click_x", self.center_x)
        click_y = getattr(current_menu, "last_click_y", self.center_y)

        new_text: arcade.Text = arcade.Text(
            "+10", click_x, click_y, arcade.color.WHITE_SMOKE, 22,
            1, "center", "Kaph", True, True
        )

        self.floating_texts.append({"text_obj": new_text, "timer": 1.0})

        self._activate_cheat()

    def on_update(self, delta_time: float) -> None:
        """
        Controls displacement physics vectors for visual floating tracking
        indicators.
        """
        for item in reversed(self.floating_texts):
            item["timer"] -= delta_time

            if item["timer"] <= 0.0:
                self.floating_texts.remove(item)
            else:
                item["text_obj"].y += 50 * delta_time

                alpha: int = int((item["timer"] / 1.0) * 255)
                item["text_obj"].color = (255, 255, 255, alpha)

    def _activate_cheat(self) -> None:
        """Modifies core actor step dimensions directly."""
        if game_config.debug_mode:
            print_log("Cheat mode: +10 speed")

        if hasattr(self.parent_view, 'previous_view'):
            self.parent_view.previous_view.player.increase_cheat_speed(10)


class NextLevelButton(BaseButton):
    """Interactive button designed to force map layout phase transitions."""
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_on: arcade.Texture
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_off = self.texture
        self.texture_on = texture_on

        # Check state of the button
        if hasattr(self.parent_view, 'previous_view'):
            if self.parent_view.previous_view.cheat_skip_level:
                self.texture = self.texture_on

    def on_click(self) -> None:
        """Aborts standard layout processing loops to clear maps instantly."""
        if hasattr(self.parent_view, 'previous_view'):
            if not self.parent_view.previous_view.cheat_skip_level:
                self.texture = self.texture_on
                self.parent_view.previous_view.cheat_skip_level = True
                self._activate_cheat()

    def _activate_cheat(self) -> None:
        """Forces level skip actions and refreshes active views."""
        if game_config.debug_mode:
            print_log("Cheat mode: Skipping level")

        if hasattr(self.parent_view, 'previous_view'):
            self.parent_view.previous_view.cheat_skip_current_level()
            if self.parent_view.window:
                self.parent_view.window.show_view(
                    self.parent_view.previous_view)


class FreezeGhostButton(BaseButton):
    """Button controlling flags that lock enemy pathfinding routines."""
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_on: arcade.Texture
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_off = self.texture
        self.texture_on = texture_on

        # Check state of the button
        if hasattr(self.parent_view, 'previous_view'):
            if self.parent_view.previous_view.is_cheat_freeze_active:
                self.texture = self.texture_on

    def on_click(self) -> None:
        """Toggles AI state parameters across active tracking dictionaries."""
        if hasattr(self.parent_view, 'previous_view'):
            if self.parent_view.previous_view.is_cheat_freeze_active:
                self.texture = self.texture_off
                self.parent_view.previous_view.is_cheat_freeze_active = False
                self._disable_cheat()

            else:
                self.texture = self.texture_on
                if hasattr(self.parent_view, 'previous_view'):
                    parent = self.parent_view.previous_view
                    parent.is_cheat_freeze_active = True
                    self._activate_cheat()

    def _activate_cheat(self) -> None:
        """Locks all enemy movement fields."""
        if game_config.debug_mode:
            print_log("Cheat mode: FREEZE on")

        if hasattr(self.parent_view, 'previous_view'):
            enemy_list = (
                self.parent_view.previous_view.level_manager.enemies_list)

        for enemy in enemy_list.values():
            enemy.can_move = False

    def _disable_cheat(self) -> None:
        """Unlocks ghost actors, forcing them to re-evaluate pathing grids."""
        if game_config.debug_mode:
            print_log("Cheat mode: FREEZE off")

        if hasattr(self.parent_view, 'previous_view'):
            enemy_list = (
                self.parent_view.previous_view.level_manager.enemies_list)

        for enemy in enemy_list.values():
            enemy.can_move = True
            enemy.brain.force_move()


class ExtraLivesButton(BaseButton):
    """
    Cheat interface component managing the user's remaining lives counter.
    """
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_on: arcade.Texture
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_off = self.texture
        self.texture_on = texture_on

        # Check state of the button
        if hasattr(self.parent_view, 'previous_view'):
            if self.parent_view.previous_view.extra_life_activate:
                self.texture = self.texture_on

        self.floating_texts: list[dict[str, Any]] = []

    def on_click(self) -> None:
        """
        Increments available engine life pools and triggers tracking indicators.
        """
        self.texture = self.texture_on
        if hasattr(self.parent_view, 'previous_view'):
            self.parent_view.previous_view.extra_life_activate = True

        current_menu = self.parent_view.window.current_view
        click_x = getattr(current_menu, "last_click_x", self.center_x)
        click_y = getattr(current_menu, "last_click_y", self.center_y)

        new_text: arcade.Text = arcade.Text(
            "+1", click_x, click_y, arcade.color.WHITE_SMOKE, 22,
            1, "center", "Kaph", True, True
        )

        self.floating_texts.append({"text_obj": new_text, "timer": 1.0})

        self._activate_cheat()

    def on_update(self, delta_time: float) -> None:
        """Manages vertical trajectory and transparency tracking formulas."""
        for item in reversed(self.floating_texts):
            item["timer"] -= delta_time

            if item["timer"] <= 0.0:
                self.floating_texts.remove(item)
            else:
                item["text_obj"].y += 50 * delta_time

                alpha: int = int((item["timer"] / 1.0) * 255)
                item["text_obj"].color = (255, 255, 255, alpha)

    def _activate_cheat(self) -> None:
        """Increments player life pools inside the core state manager."""
        if game_config.debug_mode:
            print_log("Cheat mode: +1 life")

        if hasattr(self.parent_view, 'previous_view'):
            self.parent_view.previous_view.state_manager.live += 1


class InvincibilityButton(BaseButton):
    """Bypasses collision vulnerability checks to prevent player damage."""
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            texture_on: arcade.Texture
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.texture_off = self.texture
        self.texture_on = texture_on

        # Check state of the button
        if hasattr(self.parent_view, 'previous_view'):
            if self.parent_view.previous_view.is_cheat_invincible_active:
                self.texture = self.texture_on

    def on_click(self) -> None:
        """Toggles invincibility states inside active player objects."""
        if hasattr(self.parent_view, 'previous_view'):
            if self.parent_view.previous_view.is_cheat_invincible_active:
                self.texture = self.texture_off
                self.parent_view.previous_view.is_cheat_invincible_active = (
                    False)
                self._disable_cheat()

            else:
                self.texture = self.texture_on
                if hasattr(self.parent_view, 'previous_view'):
                    parent = self.parent_view.previous_view
                    parent.is_cheat_invincible_active = (
                        True)
                    self._activate_cheat()

    def _activate_cheat(self) -> None:
        """Sets the player invincibility flag to True."""
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY on")

        if hasattr(self.parent_view, 'previous_view'):
            self.parent_view.previous_view.player.cheat_invincible = True

    def _disable_cheat(self) -> None:
        """Sets the player invincibility flag to False."""
        if game_config.debug_mode:
            print_log("Cheat mode: INVINCIBILITY off")

        if hasattr(self.parent_view, 'previous_view'):
            self.parent_view.previous_view.player.cheat_invincible = False


class CheatMenu(BaseMenu):
    """Control dashboard view mapping modifier hotkeys and toggle buttons.

    Inherits from BaseMenu and handles keyboard navigation sequences alongside
    standard mouse clicks.
    """
    def __init__(
        self, previous_view: arcade.View, background: arcade.Texture
    ) -> None:
        super().__init__()

        self.previous_view = previous_view
        self.background = background
        self.y = 0

    def build_ui(self) -> None:
        """
        Assembles and positions all cheat options onto the active canvas layout.
        """
        # Create all the cheat mode buttons
        self.invincibility = InvincibilityButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=600,
            sprite_path=(
                self.window.asset_manager.textures["invincibility_off"]
            ),
            parent_view=self.previous_view,
            texture_on=arcade.load_texture(
                self.window.asset_manager.textures["invincibility_on"]
            )
        )

        self.extra_lives = ExtraLivesButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=500,
            sprite_path=(
                self.window.asset_manager.textures["extra_lives_off"]
            ),
            parent_view=self.previous_view,
            texture_on=arcade.load_texture(
                self.window.asset_manager.textures["extra_lives_on"]
            )
        )

        self.freeze_ghost = FreezeGhostButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=400,
            sprite_path=(
                self.window.asset_manager.textures["freeze_ghost_off"]
            ),
            parent_view=self.previous_view,
            texture_on=arcade.load_texture(
                self.window.asset_manager.textures["freeze_ghost_on"]
            )
        )

        self.next_level = NextLevelButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=300,
            sprite_path=(
                self.window.asset_manager.textures["next_level_off"]
            ),
            parent_view=self.previous_view,
            texture_on=arcade.load_texture(
                self.window.asset_manager.textures["next_level_on"]
            )
        )

        self.extra_time = ExtraTime(
            center_x=(ScreenSettings.WIDTH // 2) + 200,
            center_y=200,
            sprite_path=(
                self.window.asset_manager.textures["extra_time_off"]
            ),
            parent_view=self.previous_view,
            texture_on=arcade.load_texture(
                self.window.asset_manager.textures["extra_time_on"]))
        self.button_list.append(self.extra_time)

        self.speed_up = SpeedUpButton(
            center_x=(ScreenSettings.WIDTH // 2) - 200,
            center_y=200,
            sprite_path=(
                self.window.asset_manager.textures["speed_up_off"]
            ),
            parent_view=self.previous_view,
            texture_on=arcade.load_texture(
                self.window.asset_manager.textures["speed_up_on"]))
        self.button_list.append(self.speed_up)

        self.back = BackButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=100,
            sprite_path=(
                self.window.asset_manager.textures["return_button"]
            ),
            parent_view=self.previous_view,
        )
        # Add all buttons on a button list
        self.button_list.append(self.invincibility)
        self.button_list.append(self.extra_lives)
        self.button_list.append(self.freeze_ghost)
        self.button_list.append(self.next_level)
        self.button_list.append(self.back)

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        """Processes directional keyboard inputs to navigate menu options.

        Args:
            symbol (int): Code representing the pressed key.
            _modifiers (int): Active modifier keys (unused).
        """
        if symbol == arcade.key.ESCAPE:
            if self.previous_view:
                self.window.show_view(self.previous_view)

        if symbol == arcade.key.DOWN:
            self.y += 1
        if symbol == arcade.key.UP:
            self.y -= 1

        if self.y < 0:
            self.y = 7
        if self.y == 8:
            self.y = 1
        if self.y == 1:
            self.invincibility.check_hover(self.invincibility.center_x,
                                           self.invincibility.center_y)
        else:
            self.invincibility.color = arcade.color.WHITE
        if self.y == 2:
            self.extra_lives.check_hover(self.extra_lives.center_x,
                                         self.extra_lives.center_y)
        else:
            self.extra_lives.color = arcade.color.WHITE
        if self.y == 3:
            self.freeze_ghost.check_hover(self.freeze_ghost.center_x,
                                          self.freeze_ghost.center_y)
        else:
            self.freeze_ghost.color = arcade.color.WHITE
        if self.y == 4:
            self.next_level.check_hover(self.next_level.center_x,
                                        self.next_level.center_y)
        else:
            self.next_level.color = arcade.color.WHITE
        if self.y == 5:
            self.speed_up.check_hover(self.speed_up.center_x,
                                      self.speed_up.center_y)
        else:
            self.speed_up.color = arcade.color.WHITE
        if self.y == 6:
            self.extra_time.check_hover(self.extra_time.center_x,
                                        self.extra_time.center_y)
        else:
            self.extra_time.color = arcade.color.WHITE
        if self.y == 7:
            self.back.check_hover(self.back.center_x, self.back.center_y)
        else:
            self.back.color = arcade.color.WHITE

        if symbol == arcade.key.ENTER or symbol == arcade.key.SPACE:
            if self.y == 1:
                self.invincibility.on_click()
            if self.y == 2:
                self.extra_lives.on_click()
            if self.y == 3:
                self.freeze_ghost.on_click()
            if self.y == 4:
                self.next_level.on_click()
            if self.y == 5:
                self.speed_up.on_click()
            if self.y == 6:
                self.extra_time.on_click()
            if self.y == 7:
                self.back.on_click()

    def on_draw(self) -> None:
        """Renders the blurred background texture and buttons on screen."""
        self.clear()

        # Draw the game background image
        if self.background:
            arcade.draw_texture_rect(
                self.background, arcade.XYWH(
                    self.window.width / 2, self.window.height / 2,
                    self.window.width, self.window.height)
            )

        # Draw a black rectangle with an opacity
        arcade.draw_rect_filled(
            arcade.XYWH(
                self.window.width / 2, self.window.height / 2,
                self.window.width, self.window.height),
            (0, 0, 0, 180)
        )

        # Draw the buttons
        self.button_list.draw()

        # Draw texts
        for button in self.button_list:
            if hasattr(button, 'floating_texts'):
                for item in button.floating_texts:
                    item["text_obj"].draw()

    def on_update(self, delta_time: float) -> None:
        """Dispatches game logic updates across all registered sprites.

        Args:
            delta_time (float): High-precision interval tracking elapsed frame
            phases.
        """
        self.button_list.update()

        for sprite in self.button_list:
            if hasattr(sprite, "on_update"):
                sprite.on_update(delta_time)
