# PROJECT_PLAN — rewind of all we did each days
### *anacharp + roandrie*

---

### 26/05/2026
- roandrie
	- Change sprites for all enemies: they now have 3 states (move/eatable/died)
	-  Update enemies sprites: they don't have an animation now. They only change the sprite based on the direction, so their eyes are facing the good direction
	- Add spawning of pacgums throught the maze (60% of chance, one pacgum will always spawn)
	- Add spawing of super pacgums in each corner of the maze

### 25/05/2026
- roandrie
	- Player lose a live when collide with a enemy
	- The first level is generated with a seed
	- Add timer before the game start and between respawn. Rendered on screen with a little animation.
	- Reset entities positions (sprites, facing) when respawning
	- Add 2 new fonts
	- Add new argument: --debug and run debug in Makefile
	- Add a debug button ('R') to kill the player for testing purpose
	- Add new states for the enemy
	- Add the respawn algo for the enemies (finding the way to their spawnpoint)
	- Add the SuperCalculator() to convert pixel to grid (for now), more easily to do that avoiding copy-paste the same code 3 times

	- Change: in config_loader, mandatory keys "lives" in now "live"
	- Change: new game_state and use of auto() instead of writing value by hand
	- Change: remove the unused dict in the font resources_loader
	- Change: add new enemy states and use of auto()

	- Fix: in config, the key "level_max_time" was named "Level max_time"
	- Fix: crash when player have no live left and the game over screen wasn't show
	- Fix: in the game over screen, score now need a int so it can be converted to a string when score text is created

### 22/05/2026
- roandrie
	- Add new class: FontLoader() > check if font is available and load it using arcade.load_font()
	- Change the file "renderer/sprites_loader" to "utils/resources_loader.py", since it's purpose is to load the resources for the game.
	- Refactor code to add the new change
	- Add collision detection between player/enemy
	- Rename "maze_renderer" to "game_renderer"
	- Refactor the game_engine.py
	- Transform the function in "collision_manager.py": "_player_collisions_logic" to "_entity_collisions_logic". The code is now modular for all entities
	- Delete the "move()" function in the Movable abstract class since all entities will use the buffer
	- Add walls collisions detection for all entities
	- Start the GameState Manager logic: add the game_data dictionnary containing all informations about the current game
- anacharp
	- implementation of the return to game option in the pause menu
	- connection between the game engine and the pause menu
	- fixed the issue of returning to the game when pressing "Start" in the main menu after quitting a game using the pause menu
	- make the overlays of the pause menu, game_over screen, and finish screen transparent so we can see our game in the background
	- instructions improvement
	- prevent players from validating an empty name
	- beginning of the UI screen : lives, score and timer displays

### 21/05/2026
- roandrie
	- collision manager
	- refactor the maze factory to calculate the screen offsets and tilesets
- anacharp
	- connection between ends screens and leaderboard
	- upgrade ends screens
	- create sprites and modification of other sprites
	- font implementation for finish screen and game over screen -> have to load it out of finish_screen et game_over_screen...

### 20/05/2026

- anacharp
	- pause menu modification
	- sprites modification
	- implementation of ESC use on menus
	- block 42 coordinates for pacman spawn
	- add rules and assets presentation on instructions menu
	- enter a name on game over screen and finish screen
- roandrie
	- LevelManager completed for player and enemies
	- start the player logic and collisions manager

### 19/05/2026

- anacharp
	- create an ascii maze
	- create a dictionary with informations about wall for each coordinates of the maze that will be use for ghosts algorithms
	- create pause menu, victory menu, game_over menu and cheat menu
	- create cheat menu sprites
- roandrie
	- creating the level manager
	- rendering for the player and ennemis in the maze
	- refactor some part of the code


### 18/05/2026

- anacharp
	- maze and enemy sprite modifications
	- maze improvements
	- high score menu and instructions
- roandrie
	- logic for the player and tests for it
	- logic for the enemy and tests for it (only the beginning, cat have a random algo)


### 17/05/2026

- roandrie
	- refactor the code
	- start the base of the player logic


### 15/05/2026

- anacharp
	- work on config validation and error handling with graceful fallback to default config
	- work on maze rendering and wall sprite scaling
	- work on leaderboard loading, creation and corruption recovery
	- makefile modification
	- created a new sprite asset
	- add more buttons on main menu
- roandrie
	- work on leaderboard logic : save player score, name can only be 10 characters, remove negative score, sort by highest score, keep only the 10 best scores
	- link between config and game engine
	- implement the maze factory and prevent crash if mazegenerator module is not imported
	- introduce button logic and setup for game engine
	- implement a sprite loader checking if a sprite exist and returning a dict containing the path of each sprites


### 14/05/2026

- roandrie created the all architecture of the project (no coding) including:
	- the config file and the config schema (todo: config parsing)
	- arguments parser
	- leaderboard schema and raw functions (may change)
	- maze loader and maze generation
	- entity abstract class and player, enemies, collectible class
	- game main render with all menu
	- structure of the game engine
	- add the game window and the start of the logic, and also the screen settings
	- mazegenerator imported to the project
	- add commentary to know what to do next

### 13/05/2026

- anacharp still working on the game sprites
- roandrie still working on the main architecture of the project

### 12/05/2026

- Start of the project.
- Reading the subject and starting thinking what to do.
- anacharp starts working on the game sprites.
- roandrie create the github, the main architecture of the project and start writing the project_management.
