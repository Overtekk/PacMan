# PROJECT_PLAN — rewind of all we did each days
#### *anacharp + roandrie*

---
### 08/06/2026
- roandrie
	- Cap the delta_time is the main loop to avoid bug if the game is freezing
	- Fix the freeze when invincibility goes off
- anacharp
	- standardization
	- project risks
	- team organization
	- update timeline
	- test plan
	- clear error message if user try to run the program without uv run or without being on a venv

### 05/06/2026
- anacharp
	- standardization
	- max 10 levels
	- report bug
- roandrie
	- Change the PlayButton > instead of launching the game, it will launch the introductio and then the game
	- Add dialogue between the dad and his childs
	- Add the option to skip the introduction

### 04/06/2026
- anacharp
	- working on win level animation
		- become more smooth
		- press SPACE key on starter time dezoom
		- dezoom for finish screen
	- fix pacman disappearance so that he doesn't reappear in the same place before being teleported to the center
	- make a nice logo
	- menus navigable with the keyboard arrows
	- Change the menu music by clicking on the Pac-Man logo
- roandrie
	fix: cheats stay between levels
	fix: invincibility prevent ghosts to be eaten when they respawn
	fix: missings cheats (next level, increase time, increase speed)
	fix: increase base speed of player
	fix: crash when player active the cheat freeze ghosts

	- add musics to all levels
	- finish implementing all the cheats

### 03/06/2026
- roandrie
	- add the logo screen at the start of the game
	- add music to the main menu
	- Refactor the collision_manager.py and game_engine.py, on_update method
	- Animation when eating anime: pause, score showed, blue screen
	- Enemy now respawn after a certain time if they are stuck during the respawn state
	- Opacity of the enemy increase for the duration of the respawn state (10 seconds)

	- Fix: Bugs with the audio: duplicating, not stopping etc... (AudioManager is instantiate only once know)
	- Fix: Audiomanager can't stock a None player
	- Fix: Highscore screen now goes back to the main menu and do not create another one
- anacharp
	- Fix : bugs with ui screen switching on next level before next level creation
	- create a loop with the music from the main menu
	- Animate the level change


### 02/06/2026
- anacharp
	- according speed of the player and enemies to the size of the maze
	- according chase speed and runaway speed to the sprites speed
	- making some songs
	- changing scales
	- changing sprites
	- changing pause menu and cheat mode apparition
	- find bugs and report them
	- starting with level 1 and not level 0
	- cheater in red on leaderboard
- roandrie
	- add sounds effects in the game including:
		- eating pacgums and enemies, death, click, victory, game over, cheat menu found, starting
	- add new methods to the AudioLoader class (stop a specific sound, stop all sounds)
	- add animation for dying and for winning a level

### 01/06/2026
- roandrie
	fix: pressing escape in the 'cheat menu' in game returned to main menu
	fix: add the asset loader instead of the path for rendering the background
	fix: instructions button in game return ton main menu (TODO: go back in game)

	add:
	- in game screen in the cheat menu
	- the cheat button will appear only if the konami code is activated
	- add UI rendering (green/red button) to see if a cheat is active
	- add cheats:
		- invincible
		- extra-life
		- freeze ghosts
		- add speed
		- add time
	- move the logic of the superpacgum (timer, blinking effect) from the superpacgum class to the game engine time (fixing bugs with time)
	- add more reset values for entities so they are not stuck
	- add the AudioManager, the AudioLoader and some sounds in the game

- anacharp
	- adjust the size of the mazes and sprites correctly
	- Parsing correction to prevent errors when creating a maze larger than 42 by 42
	- Implementation of the progression to the next level up on completion of the current level; if all levels are completed, the victory overlay is displayed.
	- crash fix
	- sound effects creation

### 30/05/2026
- anacharp
	- create songs
	- put all renderer's sprites with screen width
	- find and report bugs
	- activate the cheat mode and the return on the previous view
	- standardization
	- creating a new sprite for cheat menu
	- implementation of extra lives, extra time and speed up cheats

### 29/05/2026
- anacharp
	- put the beach background on the cheat menu
	- put comments on my functions
	- standardization of renderer/ui/ files
	- modify timer easter egg on main menu
	- timer
	- display the level on the game
- roandrie
	- Refactor the enemy and entity class
	- Create a new class: EnemyBrain. It have all the logic for the enemies movement logic
	- Add the logic for eating enemy (eating, enemy returning to spawn point and waits to revive, blink effect to know when the effect is going off)
	- Add movements logic for all enemies (they have all the same algo for now)
	- Prevent enemy to be stuck on a path or in a loop
	- Finish the chase state

### 28/05/2026
- anacharp
	- bugs because of ui screen fixes
	- Updated commands in the instructions
	- Animated glasses falling over Pac-Man's eyes when the player wins
	- Changed the final score display in the end screenshots
	- Start of standardization
	- Hide cheat mode

### 27/05/2026
- anacharp
	- change lives display
	- easter egg after 2min on main menu
	- main menu animation
	- change wall sprites
	- buttons animation
- roandrie
	- Enemy have a raycast. If the player is seen on the same line, they will switch in the 'chase' state.
	- Add the logic for the 'chase' state. In this mode, they know the position of the player and will try to catch them. If the player is not and the same line and some tiny time have passed, they will switch to the 'wander' state.

### 26/05/2026
- roandrie
	- Change sprites for all enemies: they now have 3 states (move/eatable/died)
	-  Update enemies sprites: they don't have an animation now. They only change the sprite based on the direction, so their eyes are facing the good direction
	- Add spawning of pacgums throught the maze (60% of chance, one pacgum will always spawn)
	- Add spawing of super pacgums in each corner of the maze
	- Add collisions with pacgums and superpacgums: player can collect them and score increase by x points
	- Add the superpacgums ability that make the player invincible and change the state of the enemies
	- Fix a lag that occurs during gameplay (object was created each 60 frames)
- anacharp
	- change the font of the Highscore interface
	- connect the UI screen with the game renderer
	- fix the finish screen issue
	- remake Pac-Man in 32x32 resolution
	- fix the instructions
	- change the heart sprite to a feather sprite because the seagull loses its feathers
	- make the main menu logo animated
	- add an Easter egg using the main menu logo
	- create a beach-themed background and implement it in the various menus and the maze
	- fix the pause menu appearing during gameplay
	- add shadows to the Pac-Man sprites (player.png, pacman_victory.png, and dead_pacman.png)

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
