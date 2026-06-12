# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_renderer.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:18:31 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:33:30 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from src import game_config
from src.renderer.screen_settings import ScreenSettings, CollectiblesType
from src.renderer.ui.ui_screen import UIScreen
from src.entity import EnemyState


class Wall(arcade.Sprite):
    """An Arcade sprite representing a single wall tile in the maze.

    Scales itself automatically to fit the given tile size.

    Attributes:
        angle (float): Rotation of the wall sprite in degrees.
        scale (float): Scale factor computed from tile size vs texture width.
    """
    def __init__(
        self,
        sprite_path: str,
        angle: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        tile_size: int = 0
    ) -> None:
        """Initialize a Wall sprite.

        Args:
            sprite_path (str): Path to the wall texture file.
            angle (float, optional): Rotation in degrees. Defaults to 0.
            center_x (float, optional): Horizontal pixel position. Defaults to
            0.
            center_y (float, optional): Vertical pixel position. Defaults to 0.
            tile_size (int, optional): Target tile size in pixels used to
                compute the scale. Defaults to 0.
        """

        super().__init__(
            sprite_path,
            center_x=center_x,
            center_y=center_y
        )

        self.angle = angle
        self.scale = tile_size / self.texture.width


class GameRenderer():
    """Handles all visual rendering for the gameplay screen.

    Manages separate SpriteLists for walls, entities, pacgums, and super
    pacgums, as well as the countdown text overlay, background, HUD, and
    the 2D camera used for zoom and pan transitions.

    Attributes:
        walls (arcade.SpriteList): Wall tile sprites.
        entities (arcade.SpriteList): Player and enemy sprites.
        pacgums (arcade.SpriteList): Regular pacgum sprites.
        super_pacgums (arcade.SpriteList): Super pacgum sprites.
        gui_camera (arcade.camera.Camera2D): Camera used for zoom transitions.
        ui_screen (UIScreen): HUD overlay (score, lives, timer, level).
    """
    def __init__(self, window: arcade.Window) -> None:
        """Initialize the GameRenderer.

        Args:
            window (arcade.Window): The game window, used to access the
                asset manager for textures.
        """
        self.window = window

        # Objects
        self.walls: arcade.SpriteList[Any] = arcade.SpriteList()
        self.entities: arcade.SpriteList[Any] = arcade.SpriteList()
        self.pacgums: arcade.SpriteList[Any] = arcade.SpriteList()
        self.super_pacgums: arcade.SpriteList[Any] = arcade.SpriteList()

        # Text
        self.timer_text: str = ""
        self.timer_size: float = 0.0

        self.timer_text_obj: arcade.Text = arcade.Text(
            text=self.timer_text,
            x=ScreenSettings.WIDTH / 2, y=ScreenSettings.HEIGHT / 2,
            color=arcade.color.WHITE_SMOKE, font_size=int(self.timer_size),
            anchor_x="center", anchor_y="center", font_name="fibberish"
        )

        self.background = arcade.load_texture(
            self.window.asset_manager.textures["ocean"]
        )

        # UI
        self.ui_screen = UIScreen("0", "0", 0, 1)
        self.next_ui = False

        self.gui_camera = arcade.camera.Camera2D()
        self.gui_zoom = self.gui_camera.zoom

    def draw(self) -> None:
        """Draw all game elements to the screen.

        Renders the background, collectibles, walls, entities, debug raycasts
        (if debug mode is on), the countdown text, and the HUD.
        """
        self.gui_camera.use()
        dark_tint = arcade.types.Color(140, 140, 140)
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(
                0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT
            ),
            color=dark_tint
        )
        self.pacgums.draw()
        self.super_pacgums.draw()
        self.walls.draw()
        self.entities.draw()

        if game_config.debug_mode:
            for entity in self.entities:
                if (hasattr(entity, 'parent')
                        and hasattr(entity.parent, '_debug_raycast')):
                    if (entity.parent.current_direction != (0.0, 0.0) and
                            entity.parent.mode in [EnemyState.WANDER,
                                                   EnemyState.SEARCH]):

                        arcade.draw_line(
                            start_x=entity.center_x, start_y=entity.center_y,
                            end_x=entity.parent._debug_raycast[0],
                            end_y=entity.parent._debug_raycast[1],
                            color=arcade.color.RED_DEVIL
                        )

        if self.timer_size > 0 and self.timer_text:
            self.timer_text_obj.draw()
        self.ui_screen.on_draw()

    def update(self, delta_time: float) -> None:
        """Animate the countdown text shrinking effect.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.
        """
        REDUCE_SIZE_PIXELS: float = 150.0
        if self.timer_size > 0:
            if self.instant_text:
                self.timer_size -= (REDUCE_SIZE_PIXELS * delta_time) * 4
                self.timer_text_obj.font_size = self.timer_size
            else:
                self.timer_size -= REDUCE_SIZE_PIXELS * delta_time
                self.timer_text_obj.font_size = self.timer_size

            if self.timer_size < 0:
                self.timer_size = 0
        self.timer_text_obj.text = self.timer_text

    def wall_generator(
        self,
        wall_data: list[tuple[str, float, float, float, float]],
    ) -> None:
        """Clear all sprite lists and rebuild the wall layer from raw data.

        Also clears collectibles and entities so the renderer is ready for
        a new level.

        Args:
            wall_data (list[tuple[str, float, float, float, float]]): Each
                tuple contains (sprite_path, angle, x, y, tile_size).
        """
        self.walls.clear()
        self.pacgums.clear()
        self.super_pacgums.clear()
        self.entities.clear()
        for sprite_path, angle, x, y, tile_size in wall_data:
            wall = Wall(sprite_path, angle, x, y, int(tile_size))
            self.walls.append(wall)
        self.next_ui = True

    def setup_entities(self, entity_sprite: arcade.Sprite) -> None:
        """Add an entity sprite to the entities render list.

        Args:
            entity_sprite (arcade.Sprite): The sprite to register for rendering.
        """
        self.entities.append(entity_sprite)

    def setup_collectibles(
        self, collectible_sprite: arcade.Sprite, collectible_type: Any
    ) -> None:
        """Add a collectible sprite to the appropriate render list.

        Args:
            collectible_sprite (arcade.Sprite): The sprite to register.
            collectible_type (CollectiblesType): Determines which list to use
                (PACGUM or SUPER_PACGUM).
        """
        if collectible_type == CollectiblesType.PACGUM:
            self.pacgums.append(collectible_sprite)

        elif collectible_type == CollectiblesType.SUPER_PACGUM:
            self.super_pacgums.append(collectible_sprite)

    def trigger_time_text(self, text: str, instant_text: bool = False) -> None:
        """Display a large countdown or status text in the center of the
        screen.

        Args:
            text (str): The string to display (e.g. "3", "2", "1", "GO!").
            instant_text (bool, optional): If True, the text shrinks four times
                faster. Defaults to False.
        """
        TEXT_SIZE: float = 250.0

        self.timer_text = text
        self.timer_size = TEXT_SIZE
        self.instant_text = instant_text

    def zoom(self, player_obj: arcade.Sprite) -> None:
        """Snap the camera to the player and incrementally zoom in.

        Args:
            player_obj (arcade.Sprite): The player sprite to centre on.
        """
        x, y = self.gui_camera.position
        # if (player_obj.center_x <= ScreenSettings.WIDTH // 2
        #    and player_obj.center_y <= ScreenSettings.HEIGHT // 2):
        #     if x > player_obj.center_x:
        #         x -= 1
        #     if y > player_obj.center_y:
        #         y -= 1
        # if (player_obj.center_x > ScreenSettings.WIDTH // 2
        #    and player_obj.center_y > ScreenSettings.HEIGHT // 2):
        #     if x < player_obj.center_x:
        #         x += 1
        #     if y < player_obj.center_y:
        #         y += 1
        # if (player_obj.center_x <= ScreenSettings.WIDTH // 2
        #    and player_obj.center_y > ScreenSettings.HEIGHT // 2):
        #     if x > player_obj.center_x:
        #         x -= 1
        #     if y < player_obj.center_y:
        #         y += 1
        # if (player_obj.center_x > ScreenSettings.WIDTH // 2
        #    and player_obj.center_y <= ScreenSettings.HEIGHT // 2):
        #     if x < player_obj.center_x:
        #         x += 1
        #     if y > player_obj.center_y:
        #         y -= 1
        self.gui_camera.position = (player_obj.center_x, player_obj.center_y)
        self.gui_camera.zoom += 0.05

    def replace(self) -> None:
        """Reset the camera position to the centre of the screen."""
        self.gui_camera.position = (ScreenSettings.WIDTH // 2,
                                    ScreenSettings.HEIGHT // 2)

    def dezoom(self) -> None:
        """Incrementally zoom the camera back out to the default level (1.0).

        Should be called each frame during the level-start transition.
        """
        if self.gui_camera.zoom > 1.0:
            self.gui_camera.zoom -= 0.10
        else:
            self.gui_camera.zoom = 1.0
            self.gui_camera.position = (
                ScreenSettings.WIDTH // 2, ScreenSettings.HEIGHT // 2
            )

    def update_ui(self, score: str, time: str, live: int, level: int) -> None:
        """Push updated game state values to the HUD.

        Args:
            score (str): Current score as a string.
            time (str): Remaining time as a string.
            live (int): Current number of lives.
            level (int): Current level index.
        """
        self.ui_screen.update(score, time, live, level)

        if self.next_ui:
            self.next_ui = False
