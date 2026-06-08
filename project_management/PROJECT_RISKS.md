# RISKS — Bug, problem
#### *anacharp + roandrie*

---

### Risks matrice

| Risk | Probability | Impacts | criticality |
| :--: | :---------: | :-----: | :---------: |
| A-Maze-ing package interface incompatible | Average | High | 🔴Critical |
| Configuration modified during evaluation | High | High | 🔴Critical |
| Game crashes without a clear message | Average | High | 🔴Critical |
| Mypy/flake8 error | Average | High | 🔴Critical |
| Poor error handling | Weak | High | 🟠High |
| Incomplete cheat mode | Weak | Average | 🟡Moderate |
| A team member unavailable during a period | Weak | Average | 🟡Moderate |
| High scores corrupted or lost (invalid JSON file) | Weak | Weak | 🟢Weak |

### Analysis and possible mitigation

## 🔴 A-Maze-ing package interface incompatible
**Description**: The package is provided by 42 and may change between the time it is received and the peer review (the subject specifies that it will be reinstalled during the review).

**Mitigation**:
- Read documentation and test all functions
- Clear error handling
- Never modify the package

## 🔴 Configuration modified during evaluation
**Description**: The subject explicitly states that the configuration will be modified during the defense. Invalid, missing, or out-of-bounds values ​​will likely be injected.

**Mitigation**:
- Defaults values implementation in case of invalid or missing values
- Testing with broken values (missing key, negative value, empty file, missing file...)
- Handle :
	- comments
	- lives minimum
	- pacgum_points minimum
	- super pacgum_points minimum
	- ghost_points minimum
	- level_max_time minimum
	- width level minimum
	- height level minimum
	- unknown keys ignored
	- highscore filename must start with data/ and end with .json and write have a file name before .json
	- if a level is empty : defaut values
	- can't give a list empty of levels
	- if a key is missing : defaut values
	- if all keys are missing : defaut values
	- json valid
	- json empty : {}

## 🔴 Game crashes without a clear message
**Description**: The game must not crash.

**Mitigation**:
- Testing the game and report bugs
- Fix bugs

## 🔴 Mypy/flake8 error
**Description**: Ignoring typing and linting during development to speed things up, then discovering a lot of errors.

**Mitigation**:
- `make lint-strict` implementation
- Add the type hints at the same time as the code, not after
- Do not use # type: ignore without a documented reason

**Warning indicator**: More than 7 mypy errors on 08/06/2026

## 🟠 Poor error handling
**Description**: An uncaught exception during the demo (modified configuration, missing file, generator error) = direct penalty depending on the subject.

**Mitigation**:
- Every exception must log a clear message AND continue properly
- Test the error scenarios in the TEST_PLAN

## 🟡 Incomplete cheat mode
**Description**: The cheat mode is explicitly evaluated during peer review. Any missing or buggy features are immediately noticeable.

**Mitigation**:
- List all the cheat functions and test them one by one
- Provide a clear interface to activate each function (documented dedicated keys)

## 🟡 A team member unavailable during a period
**Description**: Illness, exams, personal constraints.

**Mitigation**:
- Both members are familiar with the entire code (systematic cross-review)

## 🟢 High scores corrupted or lost (invalid JSON file)
**Description**: The highscore JSON file may be missing, empty, or malformed.

**Mitigation**:
- `config` must handle all these cases: missing file → create a new one, invalid content → reset cleanly with log
- Explicitly test these cases in unit tests




bugs :
- a un moment un fantome est devenu bleu et ne pouvait plus manger ni etre mange, manger un burger n'a pas debuguer la situation
- dans le run-debug souvent le chat avait son rayon rouge au debut puis apres il n'en n'avait plus alors que les autres le gardaient tout du long
- on ne peut pas spam gauche droite avec le pacman qui fait exactement gauche droite au moment ou on appuie, manque de fluidite, on peut pas manier le pacman comme on voudrait
- quand un ghost apparait alors qu'un autre burger a ete mange il ne nait pas bleu (jsp si c'est normal??)
- manger un burger en mode invincible desactive le mode invinsible (jsp si c'est normal??)
- les ennemis tournent en rond et se bloquent (aussi lorsqu'ils sont morts et essaient de retourner a leur spawn point)
- des fois des fantomes ne me tuent pas alors qu'ils sont dans leur skin de tueur, souvent quand jai mange plusieurs burgers et/ou qu'ils sont deja morts -> jarrive pas a identifier si le probleme est le fait de manger plusieurs burgers, ou si c'est parce qu'ils ont ete tues, ou les 2 en meme temps
-  cheat next level crash si le next level c'est finish screen
- des fois ca lag quand je passe sur un fantome qui est invisible car je l'ai mage ou alors c'est quand les fantomes passent de mangeables a pas mangeables (en tout cas ca bug pas tout le temps quand je passe sur un fantome invisible donc c'est surement la deuxieme option, ce constat a ete fait apres avoir fait mypy donc a check si ya une diff entre la version avant mypy et celle apres mypy)

**Last update**: *08/06/2026*
