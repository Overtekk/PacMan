# TEAM - Team organization
#### *anacharp + roandrie*

---

### Team Members

| Login | Main role | Identified strengths |
| :---: | :-------: | :------------------: |
| roandrie | Architecture referent & quality | Arcade, game engine, A-Maze-ing integration |
| anacharp | Renderer referent | Config, scoring, highscores, overlays |

### Module distribution

| Module | Main manager |
| :----: | :----------: |
| `pac-man.py` | roandrie |
| `project_management` | anacharp |
| `audio` | roandrie |
| `config` | anacharp |
| `entity` | roandrie |
| `game_engine` | roandrie |
| `leaderboard` | ancharp |
| `maze` | anacharp |
| `parser` | anacharp |
| `renderer` | anacharp |
| `utils` | roandrie |
| `Makefile` | roandrie |
| `Readme.md` | anacharp |

### Collaboration rules
**Git**
- main branch `main` - always stable
- developpement on features branchs : `feature/branch_name`
- never push on main branch -> merge via Pull Request (or verbal agreement between both members)
- english commits with a clear message

**Decision-making**
- minor technical decisions: each person decides on their own module
- structural technical decisions: agreement of both members required

### Technical decisions
| Decision | Explenation |
| -------- | ----------- |
| Graphics library: Python Arcade | Modern, well-documented, suitable for 2D games, already used by both members of the group |
| Highscores : local JSON | Simple, portable, required by the subject, no external dependencies |
| Packaging : UV | Executes the program in the environment without needing to be physically present in it, already used by both members of the group |
| End of timer behavior | Loose a life |
| Ghost behavior : One algorithm per ghost, one algorithm if ghost chase and another if ghost is chased | More fun in game, more difficulty |
| Deployment platform :  Itch.io | It's free |

### Blocking points

| Blocking case | Solution |
| ------------- | -------- |
| The maze's appearance wasn't ideal because the corners were missing when simply adding walls | Create a sprite for corners and place them under certain specific conditions |

**Last update**: *08/06/2026*
