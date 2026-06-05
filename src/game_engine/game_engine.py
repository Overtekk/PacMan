# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_engine.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:20:06 by roandrie        #+#    #+#               #
#  Updated: 2026/06/05 16:21:32 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from .level_manager import LevelManager
from .collision_manager import CollisionManager
from .game_settings import GameState, LevelState
from .gamestate_manager import GameStateManager
from src import game_config
from src.utils import print_log
from src.renderer import GameRenderer
from src.config import GameConfig
from src.entity import EnemyState
from src.renderer.screen_settings import CollectiblesType
from src.audio import AudioManager
from src.renderer.screen_settings import ScreenSettings


# Number of seconds before the level start (player and enemies movement) or
# between lose
TIMER_LEVEL_START: float = 3.0
KONAMI_CODE: list[Any] = [
    arcade.key.UP, arcade.key.UP, arcade.key.DOWN, arcade.key.DOWN,
    arcade.key.LEFT, arcade.key.RIGHT, arcade.key.LEFT, arcade.key.RIGHT,
    arcade.key.B, arcade.key.A]
CODE_TIMER: float = 5.0


class GameEngine(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        # Get the global config
        self.config: GameConfig = self.window.game_config

        # Instanciate class instance
        self.game_renderer: GameRenderer = GameRenderer(self.window)
        self.game_state: GameState = GameState.SETUP
        self.audio_manager: AudioManager = self.window.audio_player
        self.state_manager: GameStateManager = (
            GameStateManager(self.window, self, self.audio_manager)
        )
        self.level_manager: LevelManager = LevelManager(self.window)

        # -- Private variable --
        self._first_launch: bool = True
        self._pacgum_timer: float = 0.0
        self._timer_pause: float = 4.0
        self._next_level: bool = False
        self._finish: bool = False
        self._enemy_died: bool = False
        self._floating_texts: list[dict[str, arcade.Text]] = {}
        self._text_score_showed: bool = False
        self._dying_screen_fading: int = 0
        self._level_index: int = -1

        # - Easter Egg -
        self._code: list[Any] = []
        self._index: int = 0
        self._timer_code: float = 0.0
        self._code_found: bool = False

        # - Cheat
        self.is_cheat_invincible_active: bool = False
        self.is_cheat_freeze_active: bool = False
        self.extra_life_activate: bool = False
        self.extra_time_activate: bool = False
        self.speed_up_activate: bool = False
        self.cheat_skip_level: bool = False

    @property
    def code_found(self) -> bool:
        return self._code_found

    def on_update(self, delta_time: float) -> None:
        # Update the renderer
        self.game_renderer.update(delta_time)
        self.game_renderer.update_ui(
            self.state_manager.score,
            self.state_manager.time_left,
            self.state_manager.live,
            self.state_manager.current_level_index
        )

        # Call the timer for the konami code (cheat menu)
        self._timer_konami_code(delta_time)

        # ---------- NOTHING HAPPENS ----------
        if self.game_state == GameState.SETUP:
            pass

        # ---------- GAME START ----------
        elif self.game_state == GameState.STARTING:
            self.game_renderer.replace()
            self.game_renderer.dezoom()
            self._timer_start(delta_time)

        # ---------- GAME PAUSED ----------
        elif self.game_state == GameState.PAUSE:
            self._state_paused(delta_time)

        # ---------- GAME PLAYING ----------
        elif self.game_state == GameState.PLAYING:
            self._state_play(delta_time)

        # ---------- LIVE LOOSE ----------
        elif self.game_state == GameState.RESPAWN:
            self._state_respawn()

        # ---------- GAME FINISHED ----------
        elif self.game_state == GameState.FINISH:
            if self._finish:
                self.state_manager.win()

    def on_draw(self) -> None:
        # Clear the clear
        self.clear()

        # Render the game
        self.game_renderer.draw()

        # Render the enemy dying screen
        arcade.draw_lrbt_rectangle_filled(
            0.0, ScreenSettings.WIDTH, 0.0, ScreenSettings.HEIGHT,
            (35, 68, 176, self._dying_screen_fading)
        )

        # Render texts
        for text in self._floating_texts.values():
            text.draw()

    def on_show_view(self) -> None:
        # Clear the screen
        self.clear()

        # Call the setup method
        if self._first_launch:
            self._first_launch = False
            self.setup(first_instance=True)

        else:
            self.game_renderer.draw()

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if self.game_state == GameState.STARTING:
            if symbol == arcade.key.SPACE:
                self.game_renderer.gui_camera.zoom = 1.0
                self._current_timer_start = 0.0

        elif self.game_state == GameState.PLAYING:
            # Konami code
            if not self._code_found:
                if symbol == KONAMI_CODE[self._index]:
                    self._code.append(KONAMI_CODE[self._index])
                    self._index += 1
                    self._timer_code = 0

                    if self._code == KONAMI_CODE:
                        self.audio_manager.play_sound('oh_oh', 1.0)
                        self._code_found = True
                        print("🫦")

                elif self._index > 0 and symbol != KONAMI_CODE[self._index]:
                    self._code.clear()
                    self._index = 0
                    self._timer_code = 0

                elif game_config.debug_mode:
                    if symbol == arcade.key.SLASH:
                        self._code_found = True
                        print("🫦")

            # Gameplay
            if symbol == arcade.key.ESCAPE:
                self.audio_manager.pause_sound(self.level_sound)
                self.state_manager.pause_game()

            elif symbol == arcade.key.UP or symbol == arcade.key.W:
                self.player._next_direction = (0, 1)

            elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
                self.player._next_direction = (0, -1)

            elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
                self.player._next_direction = (-1, 0)

            elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
                self.player._next_direction = (1, 0)

            elif symbol == arcade.key.R and game_config.debug_mode:
                print_log("Debug: activate died!")
                self.coll_manager.debug_force_death = True

            elif symbol == arcade.key.P and game_config.debug_mode:
                print_log("Debug: activate chase mode!")
                for enemy_obj in self.level_manager.enemies_list.values():
                    enemy_obj.mode = EnemyState.CHASE

            elif symbol == arcade.key.N and game_config.debug_mode:
                if self.player.cheat_invincible:
                    print_log("Debug: disable invincibility!")
                    self.player.cheat_invincible = False
                else:
                    print_log("Debug: activate invincibility!")
                    self.player.cheat_invincible = True

            elif symbol == arcade.key.EQUAL and game_config.debug_mode:
                self.player.speed += 10
                print_log(
                    f"Debug: change player speed to: {self.player.speed}"
                )

            elif symbol == arcade.key.MINUS and game_config.debug_mode:
                if self.player.speed <= 50:
                    self.player.speed = 50
                else:
                    self.player.speed -= 10
                    print_log(
                        f"Debug: change player speed to: {self.player.speed}"
                    )

    def setup(self, first_instance: bool = False) -> None:
        if first_instance:
            self.state_manager.current_level_index = 0
            self.state_manager.score = 0

        # Reset game data
        self.state_manager.live = self.config.live
        self.state_manager.time_left = self.config.level_max_time

        # Create the level
        level_index: int = self.state_manager.current_level_index

        try:
            level: list[list[int]] = self.level_manager.create_level(
                maze_width=self.config.level[level_index].width,
                maze_height=self.config.level[level_index].height,
                first_instance=first_instance
            )
        except IndexError:
            self._finish = True
            self.game_state = GameState.FINISH
            return

        # Render the maze
        self.game_renderer.wall_generator(level)
        self._setup_entities()
        self._setup_collectibles()

        # Instanciate the Collision Manager
        self.coll_manager: CollisionManager = CollisionManager(
            self.player, self.level_manager.enemies_list,
            self.enemies_sprite_list,
            self.pacgum_sprite_list, self.super_pacgum_sprite_list,
            self.level_manager.maze_bitmap,
            self.level_manager.calculator,
            self.state_manager, self.audio_manager
        )

        self._current_timer_start: float = TIMER_LEVEL_START
        self.game_state = GameState.STARTING

    def cheat_skip_current_level(self) -> None:
        self.cheat_skip_level = False

        self.audio_manager.stop_all_sounds()
        self.audio_manager.play_sound('levelcompleted', 0.2)

        self.state_manager.current_level_index += 1
        self._next_level = True
        self._timer_pause = 3

        self._change_entities_movement(False)

        self.game_state = GameState.PAUSE

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _state_paused(self, delta_time: float) -> None:
        self._timer_pause -= delta_time

        # Animation when enemy died
        if self._enemy_died:
            self.player.sprite.visible = False

            if not self._text_score_showed:
                self._dying_screen_fading = 20
                self._show_score_text(self.player.x, self.player.y, 'score')
                self._text_score_showed = True
                self.audio_manager.play_sound('points', 0.3)

            if self._timer_pause < 0.0:
                del self._floating_texts['score']
                self._dying_screen_fading = 0
                self.player.sprite.visible = True
                self._text_score_showed = False
                self._timer_pause = 4.0
                self._enemy_died = False
                self.audio_manager.play_sound('enemydied', 0.3)
                self.game_state = GameState.PLAYING
                self._change_entities_movement(True)

        # Animation for next level
        elif self._next_level:
            self.player.sprite.angle += 100 * delta_time
            self.game_renderer.zoom(self.player.sprite)

            if self._timer_pause < 0.0:
                self._timer_pause = 4.0
                self._next_level = False
                self.setup(False)

        # Animation for dying
        else:
            sc_x, sc_y = self.player.sprite.scale
            reduction = 0.5 * delta_time
            if sc_x - reduction > 0.0 or sc_y - reduction > 0.0:
                self.player.sprite.scale = (sc_x - reduction, sc_y - reduction)

            if self._timer_pause < 0.0:
                self.player.die(delta_time)
                self._timer_pause = 4.0
                self.player.sprite.scale = self._player_scale
                self.game_state = GameState.RESPAWN

    def _state_play(self, delta_time: float) -> None:
        # - SUPER PACGUM MANAGING -
        self._super_pacgum_timer_manager(delta_time)

        # - MAIN TIMER -
        self._main_timer_manager(delta_time)

        # - COLLISIONS CHECKER -
        collision_result: LevelState = self.coll_manager.update(delta_time)
        self._collision_manager(collision_result, delta_time)

    def _super_pacgum_timer_manager(self, delta_time: float) -> None:
        # Check if a pacgum have been activate
        if self._pacgum_timer > 0.0:
            # Start the timer
            self._pacgum_timer -= delta_time

            self.audio_manager.pause_sound(self.level_sound)

            self._enemies_blinking()

            # Check for the timer ending
            if self._pacgum_timer <= 0.0:
                self._pacgum_timer = 0.0
                self.player.invincible = False

                if game_config.debug_mode:
                    print_log("DISABLE SUPERPACGUM")

                self.audio_manager.stop_sound('music_invincible')
                self.audio_manager.resume_sound(self.level_sound)

                for enemy_obj in self.level_manager.enemies_list.values():
                    if enemy_obj.mode == EnemyState.RUNAWAY:
                        enemy_obj.mode = EnemyState.WANDER
                        enemy_obj.have_respawned = False

                    enemy_obj.is_edible = False
                    enemy_obj.sprite.color = (255, 255, 255)
                    enemy_obj.speed = self.level_manager.enemy_speed

    def _enemies_blinking(self) -> None:
        BLINK_SPEED: float = 0.30

        if 0.0 < self._pacgum_timer <= 3.0:
            is_blinking: bool = ((self._pacgum_timer %
                                  (BLINK_SPEED * 2)) < BLINK_SPEED)

            for enemy_obj in self.level_manager.enemies_list.values():
                if enemy_obj.mode == EnemyState.RUNAWAY:
                    if is_blinking:
                        enemy_obj.sprite.color = (255, 255, 255)
                    else:
                        enemy_obj.sprite.color = (64, 99, 193)

    def _main_timer_manager(self, delta_time: float) -> None:
        self.state_manager.time_left -= delta_time

        if int(self.state_manager.time_left) <= 0:
            self.state_manager.time_left = self.config.level_max_time
            self.player.can_move = False
            self.game_state = GameState.PAUSE

    def _collision_manager(
        self, collision_result: LevelState, delta_time: float
    ) -> None:
        # Player have completed the level
        if collision_result == LevelState.LEVEL_COMPLETED:
            self.audio_manager.stop_all_sounds()
            self.audio_manager.play_random_sound(
                ['gg1', 'gg2', 'gg3', 'gg4'], 1.0
            )
            self.audio_manager.play_sound(
                'levelcompleted', 0.2
            )
            self.state_manager.current_level_index += 1
            self._next_level = True
            self._timer_pause = 3.5

            self._change_entities_movement(False)

            self.game_state = GameState.PAUSE

        # Player have died
        elif collision_result is LevelState.PLAYER_DIED:
            self.player.can_move = False
            self.game_state = GameState.PAUSE

        # An enemy have died
        elif collision_result is LevelState.ENEMY_DIED:
            self._change_entities_movement(False)
            self._enemy_died = True
            self.game_state = GameState.PAUSE
            self._timer_pause = 3.0

        # Continue the game
        else:
            self.player.update(delta_time)

            for enemy_obj in self.level_manager.enemies_list.values():
                enemy_obj.update(delta_time)

            for s_pacgum in self.level_manager.super_pacgums_list:
                if s_pacgum.is_activate:
                    s_pacgum.update(delta_time)

    def _state_respawn(self) -> None:
        # Reset the player
        self._reset_entities(self.player)

        # Reset all enemies
        for enemy_obj in self.level_manager.enemies_list.values():
            enemy_obj.respawn()
            self._reset_entities(enemy_obj)

        # Restart the game
        self._current_timer_start = TIMER_LEVEL_START
        self.game_state = GameState.STARTING

    def _timer_start(self, delta_time: float) -> None:
        # Save the current second
        previous_second: int = int(self._current_timer_start) + 1

        # Time elapsed
        self._current_timer_start -= delta_time

        # New second
        current_second: int = int(self._current_timer_start) + 1

        if current_second != previous_second and current_second > 0:
            if current_second == 3:
                self.audio_manager.play_sound('start_three', 1.0)
            elif current_second == 2:
                self.audio_manager.play_sound('start_two', 1.0)
            elif current_second == 1:
                self.audio_manager.play_sound('start_one', 1.0)

            if game_config.debug_mode:
                print(f"Game starting in: {current_second}")
            self.game_renderer.trigger_time_text(str(current_second))

        if self._current_timer_start <= 0.0:
            self.audio_manager.play_sound('start_go', 1.0)
            if game_config.debug_mode:
                print_log("Game started")
            self.game_renderer.trigger_time_text("GO!", True)

            self._setup_start()

    def _timer_konami_code(self, delta_time: float) -> None:
        if self._index > 0 and not self._code_found:
            self._timer_code += delta_time

            if self._timer_code > CODE_TIMER:
                self._timer_code = 0
                self._index = 0
                self._code.clear()

    def _setup_entities(self) -> None:

        # Create a reference of all movable entities
        self.player = self.level_manager.player
        self.cat_enemy = self.level_manager.enemies_list["cat_enemy"]
        self.fox_enemy = self.level_manager.enemies_list["fox_enemy"]
        self.rat_enemy = self.level_manager.enemies_list["rat_enemy"]
        self.dog_enemy = self.level_manager.enemies_list["dog_enemy"]

        # Keep cheats value between levels
        if self.is_cheat_invincible_active:
            self.player.cheat_invincible = True

        # List containing all enemies sprites
        self.enemies_sprite_list: arcade.SpriteList[Any] = arcade.SpriteList()

        # utils
        self._player_scale = self.player.sprite.scale

        # Enemy rendering
        for enemy_obj in self.level_manager.enemies_list.values():
            # Store the sprite
            self.enemies_sprite_list.append(enemy_obj.sprite)
            # Render the sprites on screen
            self.game_renderer.setup_entities(enemy_obj.sprite)
            enemy_obj.mode = EnemyState.WAIT

        # Render the player
        self.game_renderer.setup_entities(self.player.sprite)

    def _setup_start(self) -> None:
        self.game_state = GameState.PLAYING

        self._change_entities_movement(True)
        if self.state_manager.current_level_index != self._level_index:
            self._play_level_music(self.state_manager.current_level_index)
            self._level_index = self.state_manager.current_level_index

        if self.is_cheat_freeze_active:
            for enemy in self.level_manager.enemies_list.values():
                enemy.can_move = False

        for enemy_obj in self.level_manager.enemies_list.values():
            enemy_obj.mode = EnemyState.WANDER

    def _setup_collectibles(self) -> None:
        # List containing all super_pacgums sprites
        self.super_pacgum_sprite_list: arcade.SpriteList[Any] = (
            arcade.SpriteList()
        )

        for colletible_obj in self.level_manager.super_pacgums_list:
            # Store the sprite
            self.super_pacgum_sprite_list.append(colletible_obj.sprite)
            # Render the sprites on screen
            self.game_renderer.setup_collectibles(
                colletible_obj.sprite, CollectiblesType.SUPER_PACGUM
            )

        # List containing all pacgums sprites
        self.pacgum_sprite_list: arcade.SpriteList[Any] = (
            arcade.SpriteList()
        )

        for collectible_obj in self.level_manager.pacgums_list:
            # Store the sprite
            self.pacgum_sprite_list.append(collectible_obj.sprite)
            # Render the sprites of screen
            self.game_renderer.setup_collectibles(
                collectible_obj.sprite, CollectiblesType.PACGUM
            )

    def _reset_entities(self, entity: Any) -> None:
        # Block movement
        entity.can_move = False

        # Reset positions
        entity.current_direction = (0.0, 0.0)
        entity._next_direction = (0.0, 0.0)
        entity.sprite.color = (255, 255, 255)

        # Reset sprites direction
        entity.reset_animation()

        # Reset the player
        if hasattr(entity, 'invincible'):
            entity.invincible = False
            entity.speed = self.player.speed

        # Reset enemy
        if hasattr(entity, 'mode'):
            entity.mode = EnemyState.WAIT
            entity.speed = self.level_manager.enemy_speed
            entity.sprite.alpha = 255
        if hasattr(entity, 'is_edible'):
            entity.is_edible = False

    def _change_entities_movement(self, movement: bool) -> None:
        self.player.can_move = movement
        for enemy in self.level_manager.enemies_list.values():
            enemy.can_move = movement

    def _show_score_text(self, x: float, y: float, txt_name: str) -> None:
        score_text: arcade.Text = arcade.Text(
            text=f'{self.config.ghost_points}', x=x, y=y,
            color=arcade.color.BLEU_DE_FRANCE, font_size=20,
            align='center', font_name='Press Start 2P', bold=False,
            anchor_x='center', anchor_y='center'
        )
        self._floating_texts[txt_name] = score_text

    def _play_level_music(self, level_index: int) -> None:
        # +1 because we start at the index 0
        self.level_sound: str = f'music_level{level_index + 1}'

        self.audio_manager.play_sound(
            self.level_sound, 0.4, True
        )
