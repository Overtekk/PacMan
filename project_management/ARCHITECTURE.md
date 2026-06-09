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
- Boolean to know if the power related to the super pacgum is activated or not
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
- Update enemy state
- State machine : wait, wander, chase, runaway, respawn
- Enemy move :
	- check walls and corridors
	- move only on corridors
	- avoid loops
- Raycasting
- Chase player
- Runaway from player
- Move
- Revive
- Make a choice
- Go to position
```

#### Fox_brain.py
```python
class FoxBrain(EnemyBrain):
- Update the fox by checking its state and its coordinates
- Update coordinates
- Get radius
```

#### StateMachine.py
```python
class EnemyState(Enum):
- state machine : wait, wander, chase, runaway, respawn, search
```

### entity.py
```python
class Entity(ABC):
- Initialise entity with spawn point, sprite path, calculator and scale
- Logical coordinates
- Create the sprite
- Sync visual position with logical position

class Movable(Entity):
- Initialise movable with spawn point, sprite sheet, calculator, scale and speed
- Update
- Respawn
- Reset animation
- Update animation
- Die

class Enemy(Movable):
- Initialise enemy with spawn point, differents sprites sheets, maze bitmap, calculator, player, scale, speed, boolean to know if it is edible and its state
- Update
- Die
- Update animation
- Update sprite

class Collectible(Enemy):
- Initialise collectible with spawn point, sprite, calculator, scale and score
- Score
- Update
```

### player.py
```python
class Player(Movable):
- Initialise player with spawn point, sprite sheet, calculator, scale, speed
- Update
- Die
- Increase cheat speed
- Decrease cheat speed
- Update animation
- Update sprite facing
```

## src/game_engine

### collision_manager.py
```python
class CollisionManager():
- Initialise Collision Manager with player reference, enemies references, pacgums, super pacgums, maze bitmap, calculator, state manager, audio manager
- Update :
	- check collisions walls-player
	- check collisions enemies-walls
	- check collisions enemies-player
	- check collisions player-collectibles
	- check enemy state
	- force player to die
	- kill player if an enemy is colliding with him
	- get the collectible if it collides with the player
	- check if all pacgums are eaten
- kill player
- kill enemy
- collect collectible
- activate superpacgum
- entity collisions logic : get the exact center of the current tile, verify if player near the center, if the player is not moving, do nothing, check if there is a wall in front, check if the player has reached or passed the center on their movment axis
- check collisions with enemy
- check collision with collectibles
- check for collisions
- snap to grid : calculate the exact center of the current tile
- get tile center : calculate x and y center
```

### game_engine.py
```python
class GameEngine(arcade.View):
- get the global config
- instanciate class instance : game renderer, game state, audio manager, game state manager, level manager
- initialise private variables, easter egg variables and cheat variables
- update : cap the delta time to avoid crash and teleportation if game is frozen, update the renderer, call the timer for the konami code (cheat menu), do something for each state :
	- state SETUP : nothing
	- state STARTING : game start, timer start and put camera on center
	- state PAUSE : call _state_pause function
	- state PLAYING : call _state_play function
	- state RESPAWN : call _state_respawn function
	- state FINISH : call win function in state manager
- on_draw : clear, render the game, render the enemy dying screen, render texts
- on_show_view : clear the screen, call the setup method
- on_key_press : check if player do the konami code, check if player press ESCAPE to have pause menu, check if player want to move (UP, DOWN, RIGHT, LEFT or W A S D),
others keys for debug mode
- setup : reset the game data, create the level, render the maze, instanciate the collision manager
- cheat_skip_current_level
- _state_paused : animation when enemy died, animation for next level, animation for dying
- _state_play : super pacgums managing, main timer, collisions checker
- _super_pacgum_timer_manager : check if a pacgum have been activate, start timer, check for the timer ending
- _enemies_blinking
- main timer manager
- collision manager
- _state_respawn : reset the player, reset all enemies, restart the game
- _timer_start : save the current second, time elapsed, new second
- timer konami code
- setup entities : create a reference of all movable entities, keep cheats value between levels, list containing all enemies sprites, utils, enemy rendering, render the player
- setup start
- setup collectibles
- reset entities
- change entities movement
- show score text
- play level music
```

### game_settings.py
```python
class GameState(Enum):
- Set differents game states : setup, starting, playing, respawn, pause, finish

class LevelState(Enum):
- set differents level states : level_completed, player_died, enemy_died, continue
```

### gamestate_manager.py
```python
class GameStateManager():
- Initialise game state manager with game window, parent view and audio manager
- live : security check, death trigger
- score
- time left : reset the timer to default value, security check, times out trigger
- current level index
- win : security, trigger victory screen
- pause game : call pause menu
```

### level_manager.py
```python
Instanciate player scale, enemies scale, pacgums scale, siper pacgum scale

class LevelManager():
- create level : store the maze width and height in the class, create the level, create the calculator, create all entities, create all collectibles
- create maze level : Instanciate the MazeFactory object, create the maze, store the maze in bytes for later circulations
- create entity : get the spawn positions of al entities, create the player and enemies
- create collectibles
- create pacgum : list of coords where pacgums can't spawn, get each corners of the mae and add it to the forbidden list, traverse all case, ignore closed cells, ignore pair coords to avoid duplication, convert grid coords to pixels coords, check if the coords are not forbidden, create the collectible and add it to the list with a chance %
- create super pacgum : Get the coordinates of each corners, create a super pacgum for each corner
- get spawn positions : placing player, get coordinates in pixel, placing enemies
- find valid position : find valid start position
- get corners coords pixels
- get raw coords

```

## src/leaderboard

## src/maze

## src/parser

## src/renderer

## src/utils

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
