# ARCHITECTURE — functions, class, methods
#### *anacharp + roandrie*

---

## pacman.py
```python
main():
- Check the argument, load and check the config
- Check if sprites are available and store them
- Load fonts, audios, leaderboard
- Check if the maze generator is installed
- Create the game window
- Launch the main loop for the game
```

## src/audio
### AudioManager.py
```python
class AudioManager():
	- List all active sounds
	- Play sound
	- Play random sound
	- Pause sound
	- Resume sound
	- Stop sound
	- Stop all sounds
	- Init audio
	- Sound not found error
```

## src/config
### config_loader.py
```python
load_config(filepath):
- Create the path object
- Check 'data' folder
- Check permissions of 'data' folder
- Check if config file exist
- Check if config file is a json
- Check permissions
- Check for missing keys
- Pydantic validation

create_default_config()

print_default_error_message(error)
```

### config_schema.py
```python
class LevelConfig(BaseModel):
	- default level config

DEFAULT_LEVELS: list[LevelConfig]:
- 10 levels configured by default

class GameConfig(BaseModel):
	- default game config
```

## src/entity

### src/entity/collectibles

#### pac_gum.py
```python
class Pacgum(Collectible):
	- Initialise pacgums with the score, the scale, the sprite path, the spawn point and a calculator
```
#### super_pacgum.py
```python
class SuperPacgum(Collectible):
	- Initialise super pacgums with the score, the scale, the sprite path, the spawn point and a calculator
	- is_activate(self)
```

### src/entity/enemies

#### cat_enemy.py
```python
class CatEnemy(Enemy):
	- Initialise cat with speed, scale, player, spawn point, differents sprites, the maze bitmap, the calculator and a boolean to know if it is edible or not
```

#### dog_enemy.py
```python
class DogEnemy(Enemy):
	- Initialise dog with speed, scale, player, spawn point, differents sprites, the maze bitmap, the calculator and a boolean to know if it is edible or not
```

#### fox_enemy.py
```python
class FoxEnemy(Enemy):
	- Initialise fox with speed, scale, player, spawn point, differents sprites, the maze bitmap, the calculator and a boolean to know if it is edible or not
```

#### rat_enemy.py
```python
class RatEnemy(Enemy):
	- Initialise rat with speed, scale, player, spawn point, differents sprites, the maze bitmap, the calculator and a boolean to know if it is edible or not
```

### src/entity/logics

#### brain.py
```python
class EnemyBrain():
	- update(self, delta_time):
		- update enemy state
		- call raycasting function
	- _state_machine(self, delta_time):
		- wait,
		- wander,
		- chase,
		- runaway,
		- respawn
	- _get_available_moves(self):
		- check walls and corridors
		- move only on corridors
		- avoid loops
	- _raycasting(self)
	- _chase_player(self, delta_time)
	- _runaway_from_player(self)
	- _return_to_spawnpoint(self)
	- _move(self)
	- _revive(self, delta_time)
	- _apply_momentum_choice(self, open_walls)
	- _go_to_position(self, pos_x, pos_y)
```

#### Fox_brain.py
```python
class FoxBrain(EnemyBrain):
	- update(self, delta_time):
		- update the fox by checking its state and its coordinates
	- _update_coords(self)
	- _get_radius(self)
```

#### StateMachine.py
```python
class EnemyState(Enum):
	- state machine :
		- wait,
		- wander,
		- chase,
		- runaway,
		- respawn,
		- search
```

### entity.py
```python
class Entity(ABC):
	- Initialise entity with spawn point, sprite path, calculator and scale
	- Logical coordinates
	- Create the sprite
	- Sync visual position with logical position
	- x(self, new_value)
	- y(self, new_value)

class Movable(Entity):
	- Initialise movable with spawn point, sprite sheet, calculator, scale and speed
	- update(self, delta_time)
	- respawn(self)
	- reset_animation(self)
	- _update_animation(self, delta_time)
	- die(self, delta_time)

class Enemy(Movable):
	- Initialise enemy with spawn point, differents sprites sheets, maze bitmap, calculator, player, scale, speed, boolean to know if it is edible and its state
	- is_edible(self, value)
	- mode(self, new_state)
	- died(self)
	- have_respawned(self)
	- update(self, delta_time)
	- die(self, delta_time)
	- _update_animation(self, delta_time)
	- _update_sprite(self)

class Collectible(Enemy):
	- Initialise collectible with spawn point, sprite, calculator, scale and score
	- score(self)
	- update(self, delta_time)
```

### player.py
```python
class Player(Movable):
	- Initialise player with spawn point, sprite sheet, calculator, scale, speed
	- update(self, delta_time)
	- die(self, _delta_time)
	- increase_cheat_speed(self, value)
	- decrease_cheat_speed(self, value)
	- _update_animation(self, delta_time)
	- _update_sprite_facing(self)
```

## src/game_engine

### collision_manager.py
```python
class CollisionManager():
	- Initialise Collision Manager with player reference, enemies references, pacgums, super pacgums, maze bitmap, calculator, state manager, audio manager
	- update(self, delta_time):
		- check collisions walls-player
		- check collisions enemies-walls
		- check collisions enemies-player
		- check collisions player-collectibles
		- check enemy state
		- force player to die
		- kill player if an enemy is colliding with him
		- get the collectible if it collides with the player
		- check if all pacgums are eaten
	- _kill_player(self)
	- _kill_enemy(self, enemy, delta_time)
	- _collect_collectible(self, collectible)
	- _activate_superpacgum(self)
	- _entity_collisions_logic(self, entity):
		- get the exact center of the current tile,
		- verify if player near the center,
		- if the player is not moving, do nothing,
		- check if there is a wall in front,
		- check if the player has reached or passed the center on their movment axis
	- _check_collisions_with_enemy(self)
	- _check_collision_with_collectibles(self)
	- _check_for_collisions(self, entity, direction)
	- _snap_to_grid(self, entity, direction):
		- calculate the exact center of the current tile
	- _get_tile_center(self, entity):
		- calculate x and y center
```

### game_engine.py
```python
class GameEngine(arcade.View):
	- get the global config
	- instanciate class instance :
		- game renderer,
		- game state,
		- audio manager,
		- game state manager,
		- level manager
	- initialise private variables, easter egg variables and cheat variables
	- on_update(self, delta_time):
		- cap the delta time to avoid crash and teleportation if game is frozen,
		- update the renderer, call the timer for the konami code (cheat menu),
		- do something for each state :
			- state SETUP : nothing
			- state STARTING : game start, timer start and put camera on center
			- state PAUSE : call _state_pause function
			- state PLAYING : call _state_play function
			- state RESPAWN : call _state_respawn function
			- state FINISH : call win function in state manager
	- on_draw(self):
		- clear,
		- render the game,
		- render the enemy dying screen,
		- render texts
	- on_show_view(self):
		- clear the screen,
		- call the setup method
	- on_key_press(self, symbol, _modifiers):
		- check if player do the konami code,
		- check if player press ESCAPE to have pause menu,
		- check if player want to move (UP, DOWN, RIGHT, LEFT or W A S D),
		- others keys for debug mode
	- setup(self, first_instance):
		- reset the game data,
		- create the level,
		- render the maze,
		- instanciate the collision manager
	- cheat_skip_current_level(self)
	- _state_paused(self, delta_time):
		- animation when enemy died,
		- animation for next level,
		- animation for dying
	- _state_play(self, delta_time):
		- super pacgums managing,
		- main timer,
		- collisions checker
	- _super_pacgum_timer_manager(self, delta_time):
		- check if a pacgum have been activate,
		- start timer,
		- check for the timer ending
	- _enemies_blinking(self)
	- _main_timer_manager(self, delta_time)
	- _collision_manager(self, collision_result, delta_time)
	- _state_respawn(self):
		- reset the player,
		- reset all enemies,
		- restart the game
	- _timer_start(self, delta_time):
		- save the current second,
		- time elapsed,
		- new second
	-  _timer_konami_code(self, delta_time)
	- _setup_entities(self):
		- create a reference of all movable entities,
		- keep cheats value between levels,
		- list containing all enemies sprites,
		- utils,
		- enemy rendering,
		- render the player
	- _setup_start(self)
	- _setup_collectibles(self)
	- _reset_entities(self, entity)
	- _change_entities_movement(self, movement)
	- _show_score_text(self, x, y, txt_name)
	- _play_level_music(self, level_index)
```

### game_settings.py
```python
class GameState(Enum):
	- Set differents game states :
		- setup,
		- starting,
		- playing,
		- respawn,
		- pause,
		- finish

class LevelState(Enum):
	- set differents level states :
		- level_completed,
		- player_died,
		- enemy_died,
		- continue
```

### gamestate_manager.py
```python
class GameStateManager():
	- Initialize game state manager with game window, parent view and audio manager
	- live(self, new_value):
		- security check,
		- death trigger
	- score(self, new_value)
	- time_left(self, new_value, reset_timer):
		- reset the timer to default value,
		- security check,
		- times out trigger
	- current_level_index(self, new_index)
	- win(self):
		- security,
		- trigger victory screen
	- pause_game(self):
		- call pause menu
```

### level_manager.py
```python
Instanciate player scale, enemies scale, pacgums scale, siper pacgum scale

class LevelManager():
	- create_level(self, maze_width, maze_height, first_instance):
		- store the maze width and height in the class,
		- create the level, create the calculator,
		- create all entities, create all collectibles
	- _create_maze_level(self, first_instance):
		- Instanciate the MazeFactory object, create the maze,
		- store the maze in bytes for later circulations
	- _create_entity(self):
		- get the spawn positions of al entities,
		- create the player and enemies
	- _create_collectibles(self)
	- _create_pacgum(self):
		- list of coords where pacgums can't spawn,
		- get each corners of the mae and add it to the forbidden list,
		- traverse all case, ignore closed cells, ignore pair coords to avoid duplication,
		- convert grid coords to pixels coords,
		- check if the coords are not forbidden,
		- create the collectible and add it to the list with a chance %
	- _create_super_pacgum(self):
		- Get the coordinates of each corners,
		- create a super pacgum for each corner
	- _get_spawn_positions(self):
		- placing player,
		- get coordinates in pixel,
		- placing enemies
	- _find_valid_position(self, entity_name, start_coords):
		- find valid start position
	- _get_corners_coords_pixels(self)
	- _get_raw_coords(self, entity_name, coords)
```

## src/leaderboard

### extract_leaderboard.py
```python
- extract_leaderboard(filepath_str):
	- check if folder exist
	- check if we can read the folder
	- check if the file exist
	- check if the file is a json
	- if all is good, extract the file content, put it on a dictionary and return it
```

### leaderboard_loader.py
```python
- leaderboard_loader(filepath_str):
	- if folder doesn't exist, create it
	- check if we have permissions to read / write on the file
	- check if the file exist, if not, create it
	- check if the file is a json
	- check if the content of the json file is valid, if not, create a new leaderboard file
- create_leaderboard_file(filepath)
```

### leaderboard_schema.py
```python
class PlayerScore(BaseModel):
- model for the player score
class Leaderboard(BaseModel):
- model for the leaderboard file
```

### update_leaderboard.py
```python
- save_score_to_leaderboard(file, player_name, score, cheater_or_not):
	- check the lenght of the player name and cut it to have maximum 10 characters,
	- if score is negative put it to 0,
	- store the data on a dictionary,
	- get all the leaderboard content,
	- verify if there is not negative number, verify that the player doesn't exist,
	- if so, change only his score, remove the lower score if there are more than 10 entries,
	- sort the leaderboard from the hiighest score to te lowest,
	- open an write in the json output
- open_leaderboard(file)
- _find_lowest_score(data)
- sort_leaderboard(data)
- _verify_score(data)
```

## src/maze

### load_mazegenerator.py
```python
_check_mazegenerator_file():
	- check if folder exist
	- check if filepath exist
load_mazegenerator():
	- check resources files on the computer
	- check if installed in python files
```

### maze_factory.py
```python
WALL_SPRITES : instanciate all wall sprites
class MazeFactory:
- generate_maze(self, width, height, textures, screen_width, screen_height, seed):
	- calculate the tile size
	- calculate the screen offsets
	- instanciate the generator and generate the maze
	- convert the string into integer
	- create the list to store all informations
	- create the maze data
- get_pixel_coordinates(self, col, row)
- generate_bytes_maze(grid, width, height):
	- calculate grid dimensions
	- initialization: fill all walls with byte '1'
	- init dictionary containing walls bytes
	- bytes verifications: global define
	- coordinates of the center of the cell in the new grid
	- create the corridors if walls do not exist
	- convert in dictionnary of strings
	- block open cells inside the 42
```

## src/parser

### argument_parser.py
```python
class RichArgumentParser(argparse.ArgumentParser):
	- error(self, message):
		- print error message
load_arguments() :
	- create the parser object
	- add the config argument
```

## src/renderer

### renderer/ui

#### base_button.py
```python
class BaseButton(arcade.Sprite, ABC):
	- Initialize button with center_x, center_y, sprite path, parent view, scale
	- start_shake(self, duration)
	- on_update(self, delta_time)
	- check_hover(self, x, y)
	- on_click(self)
```

#### base_menu.py
```python
class BaseMenu(arcade.View, ABC):
	- on_draw(self)
	- on_mouse_motion(self, x, y, _dx, _dy)
	- on_mouse_press(self, x, y, button, _modifiers)
	- on_show_view(self)
	- on_key_press(self, symbol, modifiers)
	- build_ui(self)
```

#### cheat_menu.py
```python
class BackButton(BaseButton):
	- Initialize button with center_x, center_y, sprite path, parent view
	- on_click(self):
		- go back on parent view window

class ExtraTime(BaseButton):
	- Initialize button with center_x, center_y, sprite path, parent view
	- on_click(self):
		- add time

class SpeedUpButton(BaseButton):
	- Initialize button with center_x, center_y, sprite path, parent view
	- on_click(self):
		- increase speed player

class NextLevelButton(BaseButton):
	- Initialize button with center_x, center_y, sprite path, parent view
	- on_click(self):
		- go to the next level

class FreezeGhostButton(BaseButton):
	- Initialize button with center_x, center_y, sprite path, parent view
	- on_click(self):
		- freeze the ghosts

class ExtraLivesButton(BaseButton):
	- Initialize button with center_x, center_y, sprite path, parent view
	- on_click(self):
		- add lives for the player

class InvincibilityButton(BaseButton):
	- Initialize button with center_x, center_y, sprite path, parent view
	- on_click(self):
		- the player become invincible

class CheatMenu(BaseMenu):
	- Initialize cheat menu with previous view and background
	- build_ui(self):
		- create all the cheat mode buttons
		- add all cheat mode buttons on a button list
	- on_key_press(self, symbol, _modifiers):
		- menu navigation with keys pressed
		- press ESCAPE key go back to the previous view
	- on_draw(self):
		- draw the game background image
		- draw a black rectangle with an opacity
		- draw buttons
		- draw texts
	- on_update(self, delta_time)
```

#### finish_screen.py
```python
class Glasses(arcade.Sprite):
	- Initialize glasses with center_x, center_y, sprite path, parent view and scale
	- on_update(self, delta_time):
		- glasses animation

class PacmanVictory(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view, scale and anchor_x

class Victory(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view, scale and anchor_x

class FinishScreen(BaseMenu):
	- Initialize finish screen with score, filename and previous view
	- build_ui(self):
		- set the victory sprite
		- set the pacman winner sprite
		- write some text
		- add everything on button list and text list
	- on_key_press(self, symbol, modifiers):
		- enter name to save the score in the highscores list
		- user can only user alphanumeric characters and spaces
		- user can delete a character and press enter to go back to the main menu and register its score on the leaderboard
	- on_draw(self):
		- draw the game background image
		- draw a black rectangle with an opacity
		- draw texts and buttons
	- on_update(self, delta_time)
```

#### game_over_screen.py
```python
class GhostsWin(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view, scale and anchor_x

class DeadPacman(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view, scale and anchor_x

class GameOver(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view, scale and anchor_x

class GameOverScreen(BaseMenu):
	- Initialize finish screen with score, filename and previous view
	- build_ui(self):
		- set the game over sprite
		- set funny sprites
		- write some text
		- add everything on button list and text list
	- on_key_press(self, symbol, modifiers):
		- enter name to save the score in the highscores list
		- user can only user alphanumeric characters and spaces
		- user can delete a character and press enter to go back to the main menu and register its score on the leaderboard
	- on_draw(self):
		- draw the game background image
		- draw a black rectangle with an opacity
		- draw texts and buttons
	- on_update(self, delta_time)
```

#### highscores_screen.py
```python
class HighscoresButton(BaseButton):
	- Initialize sprite with center_x, center_y, sprite path, parent view, scale and anchor_x
	- on_click(self):
		- go back on previous view

class HighscoresScreen(BaseMenu):
	- Initialize highscore screen with previous view
	- Initialize the beach background
	- build_ui(self):
		- create highscore button to go back to main menu
		- put the leaderboard content on a text list
	- on_key_press(self, symbol, _modifiers):
		- menu navigation with keys pressed
		- press ESCAPE key go back to the previous view
	- on_draw(self):
		- draw the beach background
	- on_update(self, delta_time):
		- update highscore sprite to check if user touch it or not
```

#### instructions_screen.py
```python
class Ghosts(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view and scale

class Pacman(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view and scale

class Assets(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view and scale

class Instructions(BaseButton):
	- Initialize sprite with center_x, center_y, sprite path, parent view
	- on_click(self):
		- go back on previous view

class InstructionsScreen(BaseMenu):
	- Initialize instructions screen with previous view
	- Initialize the beach background
	- build_ui(self):
		- create all sprites
		- put the leaderboard content on a text list
	- on_key_press(self, symbol, _modifiers):
		- menu navigation with keys pressed
		- press ESCAPE key go back to the previous view
	- write_ghosts(self):
		- create ghosts sprites and write there names
	- write_pacgums(self):
		- create pacgum and super pacgum sprites and write there names
	- write_player(self):
		- create pacman psrite and write it's name
	- write_commands(self):
		- write commands text
	- write_rules(self):
		- write rules text
	- on_draw(self):
		- draw the beach background
		- draw all the sprites and texts
	- on_update(self, delta_time):
		- update instructions sprite to check if user touch it or not
```

#### intro_screen.py
```python
class CallBackground(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view, scale, anchor_x and anchor_y

class SeagullSprite(arcade.Sprite):
	- Initialize sprite with center_x, center_y, sprite path, parent view, scale, anchor_x and anchor_y
	- update_animation(self, delta_time, is_speaking, *args, **kwargs)

class IntroScreen(BaseMenu):
	- Initialize intro screen with previous view
	- Create dialogues
	- build_ui(self):
		- create the backgroud screen
	- on_update(self, delta_time)
	- on_key_press(self, symbol, _modifiers)
	- on_draw(self):
		- draw background and sprites
	- _on_pause_finished(self)
	- _next_dialogue(self)
	- _load_dialogue(self, dialogue_index, text_speed)
	- _finish_typing(self)
	- _create_ui_elements(self)
```

#### logo.py
```python
class DisplayLogo(arcade.Sprite):
	- Initialize logo with center_x, center_y, sprite path, parent view, scale, anchor_x and anchor_y

class LogoScreen(BaseMenu):
	- Initialize logo screen with previous view
	- on_update(self, delta_time):
		- remove opacity based on time
		- remove opacity
		- re-add opacity
	- build_ui(self)
	- on_draw(self):
		- draw elements
		- draw black rectangle
	- on_key_press(self, symbol, _modifiers)
	- _create_elements(self):
		- init the audios elements
		- create texts
		- create images
	- _play_sound(self)
```

#### main_menu.py
```python
class Pursuit(arcade.Sprite):
	- Initialize logo with center_x, center_y, sprite path, parent view, scale
	- on_update(self, delta_time: float):
		- Move the ghosts, if they go out of the screen they come back on the other side

class Pacman(arcade.Sprite):
	- Initialize logo with center_x, center_y, sprite path, parent view, scale
	- on_update(self, delta_time: float):
		- move pacman, if he goes out of the screen he comes back on the other side
		- animate pacman beack and wings

class LogoButton(BaseButton):
	- Initialize logo with center_x, center_y, sprite path, parent view, scale
	- on_update(self, delta_time):
		- animate logo
	- on_click(self):
		- change logo clicking on it
	- check_hover(self, x, y):
		- cancel the light gray color when the mouse is on the sprite to hide the easter egg

# class CheatButton(BaseButton):
# 	- Initialize logo with center_x, center_y, sprite path, parent view
# 	- on_click(self)

class ExitButton(BaseButton):
	- Initialize logo with center_x, center_y, sprite path, parent view
	- on_click(self):
		- close arcade window

class InstructionsButton(BaseButton):
	- Initialize logo with center_x, center_y, sprite path, parent view
	- on_click(self):
		- go on instructions menu

class HighscoresButton(BaseButton):
	- Initialize logo with center_x, center_y, sprite path, parent view
	- on_click(self):
		- go on highscores menu

class PlayButton(BaseButton):
	- Initialize logo with center_x, center_y, sprite path, parent view
	- on_click(self):
		- stop the menu music
		- start the intro screen

class MainMenu(BaseMenu):
	- Initialise a count of key A pressed
	- Set a beach background
	- build_ui(self):
		- Create buttons
		- create easter egg
		- Create an animation on the background
		- Add all buttons on a button list
	- animation(self):
		- animate pacman an ghosts
	- on_key_press(self, symbol, _modifiers):
		- press ESCAPE close arcade window
		- press A three times active easter egg
		- press key arrows to move on the menu and press enter to select one
	- on_update(self, delta_time):
		- update for animation
	- on_draw(self):
		- draw the beach background
		- draw all the sprites
	- _play_music(self)
```

#### pause_menu.py
```python
class GoBack(BaseButton):
	- Initialize logo with center_x, center_y, sprite path, parent view
	- on_click(self):
		- go back on main menu

class InstructionsButton(BaseButton):
	- Initialize logo with center_x, center_y, sprite path, parent view
	- on_click(self):
		- go on instructions menu

class Resume(BaseButton):
	- Initialize logo with center_x, center_y, sprite path, parent view
	- on_click(self):
		- go back on game

class Cheat(BaseButton):
	- Initialize logo with center_x, center_y, sprite path, parent view, background
	- on_click(self):
		- go on cheat menu

class PauseMenu(BaseMenu):
	- Initialize pause menu with previous view
	- init the audios elements
	- build_ui(self):
		- create buttons
		- put buttons on a button list
		- create the cheat button if KONAMI code have been entered
	- on_key_press(self, symbol, _modifiers):
		- go back on the game if ESCAPE pressed
		- press key arrows to move on the menu and press enter to select one
	- on_draw(self):
		- draw the game background image
		- draw a black rectangle with an opacity
		- draw buttons
	- on_update(self, delta_time):
		- update sprites to check if user touch it or not
	- create_cheat_button(self)
```

#### ui_screen.py
```python
class DisplayLives(arcade.Sprite):
	- Initialize logo with center_x, center_y, sprite path, parent view, scale, anchor_x and anchor_y

class UIScreen(BaseMenu):
	- Initialize ui screen with score, time, number of lives and level
	- Initialize the display of scores, timer and lives
	- Add it into the text list
	- build_ui(self):
		- call regenerate_lives function
	- regenerate_lives(self):
		- check the number of lives and display it
		- it can display 5 sprites
		- if there is more than 5 lives, it's write 'nb + nb_of_lives - 5'
		- when the user looses lives and there is not more than 5 lives anymore, it writes nothing except the sprites
	- on_draw(self):
		- draw sprites and texts
	- update(self, score, time, live, level):
		- update the time, the score, the number of lives and the level

```

### game_renderer.py
```python
class Wall(arcade.Sprite):
	- Initialize wall with sprite path, angle, center_x, center_y, and tile size

class GameRenderer():
	- Initialize game renderer with window
	- initialize objects and text
	- call ui screen
	- draw(self):
		- draw all entities, walls, ...
	- update(self, delta_time)
	- wall_generator(self, wall_data)
	- setup_entities(self, entity_sprite)
	- setup_collectibles(self, collectible_sprite, collectible_type)
	- trigger_time_text(self, text, instant_text)
	- zoom(self, player_obj)
	- replace(self)
	- dezoom(self)
	- update_ui(self, score, time, live, level)
```

### game_window.py
```python
class GameWindow(arcade.Window):
	- Initialize game window with the config, the sprites list and the audio list
	- screen_state(self)
	- show_main_menu(self)
```

### screen_settings.py
```python
class ScreenSettings:
	- Initialize screen width and height

class ScreenState(Enum):
	- Initialize screen states :
		- menu
		- game
		- pause
		- game over
		- leaderboard menu
		- finish
		- cheat menu

class CollectiblesType(Enum):
	- Initialize pacgum and super pacgum

```

## src/utils

### calculator.py
```python
class SuperCalculator():
	- Initialize super calculator with maze_offset_x, maze_offset_y, maze_tile_size, maze_height
	- get_pixel_to_grid_entity(self, entity):
		- convert pixels to grid
		- convert index to extended grid
	- get_pixel_to_grid_any(self, x, y):
		- convert pixels to grid
		- convert index to extendend grid
	- get_grid_to_pixel(self, x, y)
	- get_euclidean_distance(self, point1, point2)
	- check_open_wall(self, x, y, maze_bitemap)
	-
```

### check_path.py
```python
- check_path(path_str)
- check_folder(path_str)
```

### display.py
```python
- print_error(message):
	- Displays a formatted error message on the standard error stream
- print_success(message: str):
	- Display a formatted success message on the standard stream
- print_warn(message: str):
	- Display a formatted warn message on the standard error stream
- print_log(message: str):
	- Display a formatted log message on the standard stream using 'log' from
    rich. Using '_stack_offset' allow good naming for the file
- print_rule(message: str, color: str = "bold blue"):
	- Display a horizontal rule with a message at the center and with a
    specific color. If the color doesn't exist or isn't specify, the color
    bold blue will by the default color
```

### files.py
```python
- is_folder_exist(path_to_folder):
	- Check if a given path exists and is a directory
- is_file_exist(file):
	- Check if a given path exists and is a regular file
- check_file_extension(file, extension):
	- Check if a file has the intended extension
- can_read_file(file):
	- Check if a file have the permission to be read
- can_write_to_file(file):
	- Check if a file have the permission to be writted
- can_execute_file(file):
	- Check if a file have the permission to be executed
```

### resources_loader.py
```python
Initialize :
- default sprite path
- default font path
- default audio path
- requiered sprites
- requiered fonts
- requiered sounds

- check_assets_folder()

class SpritesLoader():
	- Initialize sprites loader with default path
	- check 'assets' folder
	- load_sprites(self)

class FontLoader():
	- Initialize font loader with default font
	- check 'assets' folder
	- load_fonts(self)

class AudioLoader():
	- Initialize audio loader with default audio
	- check 'assets' folder
	- load_audio(self)

- load_sprite_sheet(textures, sprite_width, sprite_height, sprites_columns, sprites_count)
```

## game_config.py
```python
Initialize :
- debug_mode
- delta_time_cap
- speed :
	- player
	- chase
	- enemy
	- ennemy_speed_reduction
	- enemy_speed_respawn
- timer:
	- player_revive_time
	- enemy_check_res_timer
- power up:
	- time_power_up
- brain:
	- raycasting_max_distance
	- fox_detection_radius
```

## assets
↳ *logo.png*\
↳ **font**\
‎ ‎ ‎ ‎ ↳ *custom_font.ttf*\
↳ **sprites**\
‎ ‎ ‎ ‎ ↳ **player**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *player.png*\
‎ ‎ ‎ ‎ ↳ **ennemies**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_rat.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_fox.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_dog.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_cat.png*\
‎ ‎ ‎ ‎ ↳ **collectibles**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *pacgum.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *super_pacgum.png*\
‎ ‎ ‎ ‎ ↳ **maze**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *corner_wall.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *four_wall.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *triple_wall.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *inside_wall.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *wall.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *heart.png*\
‎ ‎ ‎ ‎ ↳ **main menu**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *logo.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *start.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *instructions.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *highscores.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_mode.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *exit.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *ocean.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *gullman.png*\
‎ ‎ ‎ ‎ ↳ **pause**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *pause.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *resume.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *return.png*\
‎ ‎ ‎ ‎ ↳ **end**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *victory.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *game_over.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *glasses_victory.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *pacman_victory.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *dead_pacman.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *ghosts_win.png*\
‎ ‎ ‎ ‎ ↳ **cheat_menu**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_extra_lives_on.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_extra_lives_off.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_freeze_on.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_freeze_off.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_invincibility_on.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_invincibility_off.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_next_level_on.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_next_level_off.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_speed_up_on.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_speed_up_off.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_extra_time_on.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *cheat_extra_time_off.png*\


## launch script
↳ *pac-man.py*\
↳ *config.json*\
↳ *Makefile*


# src
## src/config
↳ *config_loader.py*

## src/entity
↳ *entity.py*\
↳ *player.py*\
↳ **enemy**\
‎ ‎ ‎ ‎ ↳ *rat.py*\
‎ ‎ ‎ ‎ ↳ *fox.py*\
‎ ‎ ‎ ‎ ↳ *dog.py*\
‎ ‎ ‎ ‎ ↳ *cat.py*\
↳ **collectible**\
‎ ‎ ‎ ‎ ↳ *pacgum.py*\
‎ ‎ ‎ ‎ ↳ *super_pacgum.py*

## src/game_engine
↳ *engine.py*\
↳ *pause_menu.py*\
↳ *main_menu.py*\
↳ *game_over_menu.py*\
↳ *cheat_menu.py*

## src/leaderboard
↳ *score.py*

## src/renderer
↳ *maze_renderer.py*

## src/utils
↳ *debug_mode.py*
