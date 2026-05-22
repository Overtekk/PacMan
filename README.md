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

### 📖 Configuration file:

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

    <pre style="background-color: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 5px; overflow-x: auto; font-family: 'Courier New', Courier, monospace; margin-top: 10px;">
<code>{
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
}</code>
    </pre>
</details>

---

## 💡 Instructions

### 1. Git clone this repository:
```bash
git clone https://github.com/Overtekk/Call_me_Maybe.git
```

### 2. Install dependencies:
```bash
make  # install all dependencies and run the script

uv sync  # alternatively you can also use this
```
> [!NOTE]
> If you don't have `uv` installed, run `make install`

---

## ⚙️ How it works?

### Configuration

todo

### Maze Generation package

todo

### Implementation

todo

### General Software Architecture

todo

###

Project Management

---

## 📚 Resources

### Documentation
| Resource | Description |
| :------: | :---------: |

### Other
| Resource | Description |
| :------: | :---------: |
| [Github of sousampere](https://github.com/sousampere) | Help with project management |
| [Arcadeblogger - Pacman documentary](https://arcadeblogger.com/2016/03/12/the-development-of-pacman/) | Documentary of the conception of Pacman |

### IA was use to:
- todo

---
