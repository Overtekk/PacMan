*This project has been created as part of the 42 curriculum by roandrie*

<p align="center">
  <img src="assets/logo.png" width="260" />
</p>
<h3 align="center">
  <em>Recreate the famous arcade game Pac-man!</em>
</h3>

---

<div align="center">
  <img src="https://img.shields.io/badge/SCORE-None-%235CB338?style=for-the-badge&logo=42&logoColor=white"/>
  <img src="https://img.shields.io/badge/COMPLETED-No-%23007ACC?style=for-the-badge&logo=calendar&logoColor=white"/>
</div>

## ⚠️ Disclaimer

- **Full Portfolio:** This repository focuses on this specific project. You can find my entire 42 curriculum 👉 [here](https://github.com/Overtekk/42).
- **Subject Rules:** I strictly follow the rules regarding 42 subjects; I cannot share the PDFs, but I explain the concepts in this README.
- **Archive State:** The code is preserved exactly as it was during evaluation (graded state). I do not update it, so you can see my progress and mistakes from that time.
- **Academic Integrity:** I encourage you to try the project yourself first. Use this repo only as a reference, not for copy-pasting. Be patient, you will succeed.

---

## ✏️ Quick Start

```bash
make  # install all dependencies and run the script

uv sync  # alternatively you can also use this
uv run python pac-man.py config.json

# Or create a virtual environement and launch it using:
python3 -m venv .venv
source venv/bin/activate
python3 pac-man.py config.json
```
> [!NOTE]
> If you don't have `uv` installed, run `make install`

---

## 📂 Description

The goal of this project is to create a complete and playable **Pac-Man** game in python, using object-oriented programming and a modular, reusable architecture.

The game must support:
- a custom configuration file to set the game parameters.
- a level generation based on an external `A-Maze-ing` package (see my github: https://github.com/Overtekk/A_Maze_ing for more informations on it).
- a highscore system that keep informations between differents games.
- a graphical UI.
- a cheat mode.
- a deployment to a public gaming platform for demonstration.

### 📝 Rules:

- Must be written in **Python >=3.10**.
- Must adhere to the **flake8** and **mypy** standard.
- Crash and leaks must be properly managed. All errors must be handled gracefully.
- Code must include type hints and docstrings *[(following PEP 257)](https://peps.python.org/pep-0257/)*

### 📮 Makefile:

This project must have a Makefile and the following rules:
- **install**: install project dependencies using **pip**, **uv** etc...
- **run**: execute the main script of the project.
- **debug**: run the main script in debug mode using Python's pdb.
- **clean**: Remove temporary files or caches.
- **lint**: execute the commands `flake8` . and `mypy . --warn-return-any
--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
--check-untyped-defs`.
- **lint**: execute the commands `flake8 .` and `mypy . --strict`.

---

## 💡 Instructions

### 1. Git clone this repository:
```bash
git clone https://github.com/Overtekk/Call_me_Maybe.git
```

### 2. Run the program
```bash
make  # install all dependencies and run the script
```
> [!NOTE]
> If you don't have `uv` installed, run `make install`

You can also use those commands:
```bash
uv sync  # alternatively you can also use this
uv run python pac-man.py config.json

# Or create a virtual environement and launch it using:
python3 -m venv .venv
source venv/bin/activate
python3 pac-man.py config.json
```

---

## ⚙️ How it works?

### Configuration

The configuration file is verified throught a strict schema. If any of the key is missing, invalid or if the value is incorrect *(e.g.: lives: -1)* the default config will be instancied instead.

| Key | Information | Default value |
| :-: | :---------: | :-----------: |
| `highscore_filename` | file where the highscore file (in json) will be stored | *data/leaderboard.json* |
| `lives` | number of lives of the player | *3* |
| `pacgum_points` | points given when pacgum is collected | *10* |
| `super_pacgum_points` | points given when super pacgum is collected | *50* |
| `ghosts_points` | points given when a ghost is eaten | *200* |
| `seed` | seed for the first level | *koala* |
| `level_max_time` | duration, in seconds, to complete a level | *180* |
| `level` | array of levels (max: 10) | *see below* |

> [!NOTE]
> If any key is missing, the default one will be used.
> If a config file is invalid, defaults values will be used.

### Level configuration

This section detail how a level, in the `level` section, works:

| Key | Information |
| :-: | :---------: |
| `name` | name of the level |
| `width` | width of the maze |
| `height` | height of the maze |

**Defaults configuration files**

<details>
    <summary style="cursor: pointer; font-weight: bold; color: #2196F3;">
        Click to see the default configuration
    </summary>

```json
{
    "highscore_filename": "data/leaderboard.json",
    "lives": 3,
    "pacgum_points": 10,
    "super_pacgum_points": 50,
    "ghost_points": 200,
    "seed": "koala",
    "level_max_time": 180.0,
    "level": [
        {
            "name": "level_1",
            "width": 20,
            "height": 10
        },
        {
            "name": "level_2",
            "width": 18,
            "height": 12
        },
        {
            "name": "level_3",
            "width": 10,
            "height": 10
        },
        {
            "name": "level_4",
            "width": 10,
            "height": 20
        },
        {
            "name": "level_5",
            "width": 15,
            "height": 21
        },
        {
            "name": "level_6",
            "width": 14,
            "height": 10
        },
        {
            "name": "level_7",
            "width": 15,
            "height": 10
        },
        {
            "name": "level_8",
            "width": 12,
            "height": 16
        },
        {
            "name": "level_9",
            "width": 14,
            "height": 10
        },
        {
            "name": "level_10",
            "width": 20,
            "height": 20
        }
    ]
}
```
</details>

### Highscore

The highscore system is stored in a json file. If the file doesn't exist or if the permissions are wrong, a new file will be created (or an error).\
The user can enter his name when the game is finished. It can only write 10 characters, only alphanumeric ones.\

When a new user is entered. The file will verified if there are 10 or more entries. If there is more, all score will be sorted (from the highest, to the lowest), and the lowest ones will be removed.\
It also check if scores are valid, just in case.

Json is the more efficient way and provides tools to check everything in the fasted way.

### Maze Generation package

The generation of the maze is used thanks to the A-Maze-Ing packages given to us.

### Implementation & General Software Architecture

The game use a lot of inheritance and abstract class. Each folder, in the `src` folder have been designed to be clear and precise for it's use.

`renderer`:
All things for the rendering system are here. Two mains abstract class are init here:
- `base_button.py`: abstract class for all buttons
- `base_menu.py`: abstract class for all menus

In there, the main rendering window is initialize and all the rendering are made here.

`maze`:
The creation of the maze throught the A-Maze-ing package is made in this folder.

`game_engine`:
The core mechanics of the game works here:
- `game_engine.py`: main engine of the game that created all the other instance and check is everything works. It's the main orchestra.
- `collision_manager.py`: manage all collisions of the game.
- `gamestate_manager.py`: manage the states of the game and what happens during each states.
- `level_manager.py`: init each levels, entities and collectibles.

`audio`:
The audio in managed in this folder throught custom play sound, play random soud, pause or stop sounds methods.

`entity`:
All entities logics are implemented here. There are 4 abtracts classes:
- **Entity**: the main class for all entities that have sprite, positions.
- **Movable**: inherit from **entity** and allow entities to moves.
- **Enemy**: inherit from **movable** and have all the logics for an enemy type.
- **Collectible**: inherit from **entity** and have the logics for a collectible type.

This folder also contains the 'brain logic' for enemies and the different algorithms.

## Algorithms

Each enemies have a different algorithm trought a state machine.\

| State Name | Meaning |
| :--------: | :-----: |
| **WAIT** | Wait and do not move |
| **WANDER** | Wander randomly around the maze |
| **CHASE** | Follow the player and have a chance to lose it |
| **RUNAWAY** | Make a 180turn, become slower and wander randomly |
| **RESPAWN** | Goes to the spawnpoint (automatically teleport after a certain time if stuck) |
| **SEARCH** | Search for the player with a specific algorithm |
| **ANGRY** | Specific to the **Fox Enemy**, will chase the player until level is completed or player have lost |

**Cat Enemy**: The cat enemy use the **[A* algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)** and always knows the player position. It will always search for it but move a bit slower.

**Dog Enemy**: It knows the player position and try to goes to it using the **[Euclidian Distance](https://en.wikipedia.org/wiki/Euclidean_distance)**, but it have 60% to take the wrong path. When only 30% of collectibles are left on the maze, the percentage is inversed.

**Fox Enemy**: The player have a radius around him *(0.19%)*. When outside, the fox will goes to the player using the **Euclidian Distance**, and when inside it will wander randomly. If there are less than 30% of collectibles left on the maze, it will be angry and always chase the player with less speed than the normal chase.

**Rat Enemy**: Wander randomly around the maze.

**Raycast**:\
Each enemy have a raycast of **2 cases** in front of it. If the player is found inside, the enemy will switch to the **Chase State** and will chase the player.

**Chase State**:\
When in chase state. The enemy will move faster and will follow the player using the **Euclidian Distance**. When the player is not seen in the **raycast vision** of the enemy, enemy will have a certain chance of lose it. When the player is outside the **raycast vision** for a certain time, the enemy will switch to the **wander/search state**.

### Project Management

Project Management was made during the project. Each days, each members write what it have done in the **PROJECT_PLAN**.\
We try to follow the expected planning but the project was more complex that will tought.

---

## 📚 Resources

### Documentation for Arcade library
| Resource | Description |
| :------: | :---------: |
| [Arcade API](https://api.arcade.academy/en/3.3.3/index.html) | Official API of Arcade library |
|[Arcade Colors](https://api.arcade.academy/en/2.6.17/arcade.color.html)| Official colors of Arcade library |

### StateMachine
| Resource | Description |
| :------: | :---------: |
| [Medium](https://medium.com/@eveciana21/enemy-ai-states-using-fsm-7fe3b3d05c4a) | Tiny documentation (more example) of how to do a state machine in python |

### Documentation for Enum
| Resource | Description |
| :------: | :---------: |
| [Official Python Doc](https://docs.python.org/3/library/enum.html) | Documentation about the enum |

### Math
| Resource | Description |
| :------: | :---------: |
| [Eitca (french)](https://fr.eitca.org/intelligence-artificielle/eitc-ai-mlp-machine-learning-avec-python/programmation-de-l%27apprentissage-automatique/programmation-de-l%27algorithme-des-k-plus-proches-voisins/examen-examen-programmation-propre-algorithme-des-k-voisins-les-plus-proches/comment-calculer-la-distance-euclidienne-entre-deux-points-de-donn%C3%A9es-%C3%A0-l%27aide-d%27op%C3%A9rations-Python-de-base/) | Help for calculating the distance between two points using the euclidean distance |

### Algorithms
| Resource | Description |
| :------: | :---------: |
| [Datacamp (french)](https://www.datacamp.com/fr/tutorial/a-star-algorithm?dc_referrer=https%3A%2F%2Fwww.google.com%2F) | How to implement the A* algorithm |
| [geeksforgeeks](https://www.geeksforgeeks.org/python/a-search-algorithm-in-python/) | What is the A* algorithm and how to implement it |

### Other
| Resource | Description |
| :------: | :---------: |
| [Github of sousampere](https://github.com/sousampere) | Help with project management |
| [Arcadeblogger - Pacman documentary](https://arcadeblogger.com/2016/03/12/the-development-of-pacman/) | Documentary of the conception of Pacman |
| [Pacman Fandom](https://pacman.fandom.com/wiki/Maze_Ghost_AI_Behaviors) | Documentary for all ghost AI behaviors |

### IA was use to:
- **Refactoring** ― help to write better understand code, type hints some part of the code.
- **Help with the Arcade library** ― since the documentation is not well done, IA have helped to better understand what we can do and how.
- **Debugging** ― when bug occurs and we didn't know what cause did, IA help us understanding what goes wrong.

---
