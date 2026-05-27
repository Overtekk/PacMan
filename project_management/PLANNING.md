# PLANNING — things to do
#### *anacharp + roandrie*

---

*✖️ = finished*

## Architecture conception

| Task | Member | Statut |
| :--: | :----: | :----: |
| Subject reading | anacharp, roandrie | ✖️ |
| Git setup | roandrie | ✖️ |
| Project Management | roandrie | ✖️ |
| Makefile | roandrie | ✖️ |
| Create the project environment | roandrie | |
| Implement the 'A-Maze-ing' package | roandrie | ✖️ |
| Creating the main script | roandrie | ✖️ |

## Config

| Task | Member | Statut |
| :--: | :----: | :----: |
| Create the configuration file | anacharp | ✖️ |
| Parsing | anacharp | ✖️ |
| Create the config object | anacharp | ✖️ |
| Unitary test for the config | anacharp | ✖️ |

## Sprites
| Task | Member | Statut |
| :--: | :----: | :----: |
| Creating the sprite of the player | anacharp | ✖️ |
| Creating the sprite of the enemies | anacharp | ✖️ |
| Creating the sprite of the collectibles | anacharp | ✖️ |
| Creating the sprite of the maze | anacharp | ✖️ |
| Creating the sprite of the menu | anacharp | ✖️ |
| Creating the sprite of the HUD | anacharp | ✖️ |

## Maze Generator Integration

| Task | Member | Statut |
| :--: | :----: | :----: |
| Create the Maze Loader with main script | anacharp, roandrie | ✖️ |
| Create the Maze Loader with package installer | anacharp, roandrie | ✖️ |
| Creation of the maze | anacharp | ✖️ |
| Unitary test if generation fails | anacharp, roandrie | |

## Core elements

| Task | Member | Statut |
| :--: | :----: | :----: |
| Creation of the Entity abstract class | roandrie | ✖️ |
| Creation of the player class | roandrie | ✖️ |
| Creation of the enemies class | roandrie | ✖️ |
| Creation of the collectible abstract class | roandrie | ✖️ |
| Creation of the pacgum class | roandrie | ✖️ |
| Creation of the super-pacgum class | roandrie | ✖️ |
| Finish player movements | roandrie | ✖️ |
| Finish player logic  | roandrie | |
| Implementation of algorithm of the fox enemy | roandrie | |
| Implementation of algorithm of the dog enemy | roandrie | |
| Implementation of algorithm of the rat enemy | anacharp | |
| Implementation of algorithm of the cat enemy | anacharp | |

## Player

| Task | Member | Statut |
| :--: | :----: | :----: |
| Respect walls | roandrie | |
| Use arrow keys or WASD to move | roandrie | ✖️ |
| Have 3 lives | roandrie | |
| Lose a life if touched by a ghost | roandrie | |
| Respawn in the middle of the maze | roandrie | |
| Game over if no lives left | roandrie | |
| Wins when all pacgums are eaten | roandrie | |
| Wins if all levels are completed | roandrie | |
| Creation of the score and increase score | roandrie | |
| Pacgum increase the score by X points | roandrie | |
| Super-pacgum increases the score by Y points | roandrie | |
| Eating a edible ghost increases score by Z points | roandrie | |

## Enemies

| Task | Member | Statut |
| :--: | :----: | :----: |
| Rat enemy move randomly | anacharp | |
| Cat follow the player until too close | anacharp | |
| Fox follow the players | roandrie | |
| Dog follow player and movements based on Fox | roandrie | |
| Super-pacgum make ghosts edible for short of time | roandrie | |
| Run away from the player when edible | roandrie | |
| Respawn to their corner after a while when eaten | roandrie | |
| Move to their corner when player died for a moment | roandrie | |

## Level

| Task | Member | Statut |
| :--: | :----: | :----: |
| First level is generated with a seed | anacharp | |
| Other levels are generated random | anacharp | |
| Pacgum present in corridors | anacharp | |
| Super-pacgums in the 4 corners of the maze | anacharp | |
| 4 ghosts in each corner of the maze | anacharp | ✖️ |
| Player start a the middle | anacharp | ✖️ |
| Unitary tests | roandrie | |

## Gameplay

| Task | Member | Statut |
| :--: | :----: | :----: |
| Creation of the game engine | roandrie | ✖️ |
| Creation of the main gameloop | roandrie | |
| Implementation of a timer, player lose a life | roandrie | |
| Integration of the player in the maze | anacharp, roandrie | |
| Integration of the enemis in the maze | anacharp, roandrie | |
| Implementation of levels | anacharp | |
| Implementation of scoring system | anacharp | |
| Implementation of pause and resume | anacharp | |
| Implementation of the highscore | anacharp | |

## User Interface
| Main Menu (start game, view highscores, instructions, exit) | anacharp | ✖️ |
| In-game HUD (current score, remaining lives, current level, remaining time for level) | anacharp | |
| Pause Menu (resume, return to main menu) | anacharp | ✖️ |
| Game Over Screen (final score, prompts player to enter their name) | anacharp | ✖️ |
| Victory Screen (final score, prompt player to enteir their name) | anacharp | ✖️ |

## Rendering

| Task | Member | Statut |
| :--: | :----: | :----: |
| Rendering of the maze | anacharp | ✖️ |
| Interaction between menu | anacharp | |
| Rendering of main menu | anacharp | ✖️ |
| Rendering of game HUD | anacharp | |
| Rendering of pause menu | anacharp | ✖️ |
| Rendering of game over (defeat) | anacharp | ✖️ |
| Rendering of game over (victory) | anacharp | ✖️ |
| Rendering of leaderboard | anacharp | ✖️ |
| Rendering of cheat mode | anacharp | ✖️ |
| Rendering of the player (right, left) | roandrie | ✖️ |
| Rendering of the enemies (right, left) | roandrie | ✖️ |

## Cheat mode

| Task | Member | Statut |
| :--: | :----: | :----: |
| Invincibility | roandrie | |
| Ghost freeze | roandrie | |
| Extra lives | roandrie | |
| Increase speed | roandrie | |
| Level skip | anacharp | |

## Leaderboard

| Task | Member | Statut |
| :--: | :----: | :----: |
| Choose where to be stored | anacharp, roandrie | ✖️ |
| Put name and store it | anacharp | ✖️ |
| Handles scores and store it | anacharp | ✖️ |
| Show the 10 top highscores with player names and scores in the game | anacharp | ✖️ |
| Unitary test for files errors | anacharp, roandrie | ✖️ |

## Utilitary

| Task | Member | Statut |
| :--: | :----: | :----: |
| Docstrings in all code | anacharp | |
| Flake8 & mypy friendly | roandrie | |
| Game test (everything works) | anacharp, roandrie | |
| Finish README | anacharp, roandrie | |

## Deployement

| Task | Member | Statut |
| :--: | :----: | :----: |
| Package created | roandrie | |
| Deployement on itch.io | roandrie | |


|  | roandrie | |

---

**Last update**: *22/05/2026*
