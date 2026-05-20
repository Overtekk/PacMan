# PROJECT_PLAN — rewind of all we did each days
### *anacharp + roandrie*

---

### 20/05/2026

- anacharp
	- pause menu modification
	- sprites modification
	- implementation of ESC use on menus
	- block 42 coordinates for pacman spawn
	- add rules and assets presentation on instructions menu

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
