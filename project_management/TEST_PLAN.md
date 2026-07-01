# TEST WITH MORE OR LESS THAT 10 LEVELS IN THE CONFIG FILE
# IN GAME RETURN = RETURN TO GAME, NOT RETURN TO MAIN MENU (EXIT = LEAVE GAME OR RETURN TO MAIN MENU)

# TEST_PLAN
#### *anacharp + roandrie*

## 1. Launch and configuration
### 1.1 Nominal launch

| Scenario | Indent | Expected result | Status |
| -------- | ------ | --------------- | ------ |
| Normal launch | `uv run python pac-man.py data/config.json` | Game starts, main menu displayed | ✅ |
| Missing argument | `uv run python pac-man.py` | Clear error message | ✅ |
| Too many arguments | `uv run python pac-man.py a.json b.json` | Clear error message | ❌ |
| Missing file | `uv run python pac-man.py missing.json` | Clear error message | ✅ |
| not a json file | `uv run python pac-man.py README.md` | Clear error message | ✅ |

### 1.2 Configuration

| Scenario | Indent | Expected result | Status |
| -------- | ------ | --------------- | ------ |
| Missing key `lives` | Delete 'lives' on config.json | Clear error message, set defaults values and start the game | ✅ |
| Negative value `lives: -1` | `"lives": -1` | Clear error message, set defaults values and start the game | ✅ |
| Value too high | `"lives: 10000"` | Clear error message, set defaults values and start the game | ✅ |
| Wrong type `lives: three` | Clear error message, set defaults values and start the game | ✅ |
| Unknown key | `"foo": "bar"` | Ignore this key and start the game | ✅ |
| Empty json | {} | Clear error message, set defaults values and start the game | ✅ |
| Comments | `# comment` | Ignore comments and start the game | ✅ |
| Negatives points | `"points_per_pacgum": -5` | Clear error message, set defaults values and start the game |  ✅ |
| Invalid seed | `"seed": "abc"` | Clear error message, set defaults values and start the game | ❌ |
| Timer to 0 | `"level_max_time": 0` | Clear error message, set defaults values and start the game | ✅ |

### 2. Maze Generation

| Scenario | Expected result | Status |
| -------- | --------------- | ------ |
| Level 1 with seed | Same maze each time | ✅ |
| Other levels with random seed | other levels are random | ✅ |
| Maze with PERFECT=False | Not only one path on the maze | ✅ |
| Width and height configuration | The maze respect width and height | ✅ |
| A-Maze-Ing package fail | Clear error message | ❌ |

### 3. Player

| Scenario | Expected result | Status |
| -------- | --------------- | ------ |
| Move up | Pac-man can move up | ✅ |
| Move down | Pac-man can move down| ✅ |
| Move to the right | Pac-man can move to the right | ✅ |
| Move to the left | Pac-man can move to the left | ✅ |
| Wall collision | Pac-man can't go on a wall | ✅ |
| Start position | Pac-man start on maze center | ✅ |
| Ghost collision | Pac-man loose a life and reappears on maze center | ✅ |
| Loose last live | Game-over | ✅ |
| Reappearition after death | Reappear on maze center, ghosts reappear on corners| ✅ |

### 4. Ghosts

| Scenario | Expected result | Status |
| -------- | --------------- | ------ |
| Move autonomous | 4 ghosts move | ✅ |
| Can't go on walls | Can only move on corridors | ✅ |
| Edible after super-pacgum | Change of skin, run away the player | ✅ |
| Eating and edible ghost | ghost deasappear, score update, and ghost reappear after some time | ✅ |
| Corner reappearation | ghosts reappear on his start corner after some time | ✅ |
| End of edible mode | ghosts regain their basic skin and behavior| ✅ |

### 5. Pacgums and scoring

| Scenario | Expected result | Status |
| -------- | --------------- | ------ |
| Eat a pacgum | Score +(config value), pacgum desappear | ✅ |
| Eat a super-pacgum | Score +(config value), super-pacgum desappear | ✅ |
| Eat a ghost | Score +(config value) | ✅ |
|All pacgums are eaten | Next level or game victory if it was the last level | ✅ |
| Keep score between levels | Score on level N is the same on the begining of level N+1 | ✅ |
| Restore lives in new levels | If the player lost a live on the first level and goes to the second level, his lives are restored | ✅ |

### 6. Progression and levels

| Scenario | Expected result | Status |
| -------- | --------------- | ------ |
| Level completed | Next level or victory screen if there is no more levels | ✅ |
| 10 levels | All levels are playable without crashes | ✅ |
| End of last level | Victory screen | ✅ |
| Timer is on 0 | Loose a life | ✅ |
| Timer visible during the game | Time up to date in real time | ✅ |


### 7. User Interface
| Scenario | Expected result | Status |
| -------- | --------------- | ------ |
| Main menu at startup | Buttons : start, highscores, instructions, exit | ✅ |
| Start button | Start the first level | ✅ |
| Highscores button | Show top 10 with names and scores | ✅ |
| Instructions button | Show rules and commands | ✅ |
| Quit button | Close the game | ✅ |
| HUD in-game | Score, lives, level | ✅ |
| Pause | Game suspended, pause menu displayed | ✅ |
| Return from pause menu | Return to the game extactly at the same moment you suspended it before | ✅ |
| Exit from pause menu to main menu | Give up the main and go back ot the main menu | ✅ |
| Game Over screen | Final score displayed, input for player name | ✅ |
| Victory screen | Final score displayed, victory message and input for player name | ✅ |
| Input player name | Can't write more than 10 characters | ✅ |
| Alphanumeric characters | Only alphanumeric and spaces | ✅ |

### 8. Highscores
| Scenario | Expected result | Status |
| -------- | --------------- | ------ |
| Save a new highscore | Score saved on json | ✅ |
| Highscores loading | Top 10 on main menu | ✅ |
| Score on top 10 | Put the score on good position | ✅ |
| Score out of the top 10 | Don't save it | ✅ |
| Missing highscore file | Create one, no crash | ✅ |
| Highscore file corrupted | Reanitialise it with a clear error message, no crash | ✅ |
| 10 scores already on highscore file | Replace the last one | ✅ |

### 9. Cheat mode

| Scenario | Expected result | Status |
| -------- | --------------- | ------ |
| Invincibility | Click on menu | Ghost can't touch the player | ✅ |
| Next level | Click on menu | Go to the next level | ✅ |
| Freeze ghost | Click on menu | All ghost stop moving | ✅ |
| Extra lives | Click on menu | +1 live per click | ✅ |
| Speed up | Click on menu | Pac-man move faster | ✅ |
| Cheat desactivate | Click on a cheat activated | Remove the cheat effect | ✅ |
| Additional cheats | Click on more than one cheats on the menu | Activate clicked cheats simultaneously | ✅ |

### 10. Code quality

| Verification | Indent | Expected result | Status |
| ------------ | ------ | --------------- | ------ |
| make install | `make install` | Dependencies installation without error | ✅ |
| make run | `make run` | start the game | ✅ |
| make lint | `make lint` | 0 mypy error and 0 flake8 error | ❌ |
| make lint-strict | `make lint-strict` | 0 mypy error and 0 flake8 error | ❌ |
| make clean | `make clean` | delete `__pycache__` and `.mypy_cache` | ❌ |
| make debug | `make debug` | game start on debug mode (pdb) | ❌ |

**Last update**: *08/06/2026*
