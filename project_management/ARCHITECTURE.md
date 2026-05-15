# ARCHITECTURE — functions, class, methods
#### *anacharp + roandrie*

---

## assets
↳ *logo.png*\
↳ **font**\
‎ ‎ ‎ ‎ ↳ *custom_font.ttf*\
↳ **sprites**\
‎ ‎ ‎ ‎ ↳ **player**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *player.png*\
‎ ‎ ‎ ‎ ↳ **ennemies**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_rat.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_rat_eatable.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_rat_dead.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_fox.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_fox_eatable.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_fox_dead.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_dog.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_dog_eatable.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_dog_dead.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_cat.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_cat_eatable.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *enemy_cat_dead.png*\
‎ ‎ ‎ ‎ ↳ **collectibles**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *pacgum.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *super_pacgum.png*\
‎ ‎ ‎ ‎ ↳ **maze**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *corner_wall.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *four_wall.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *triple_wall.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *double_wall.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *wall.png*\
‎ ‎ ‎ ‎ ↳ **main menu**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *logo.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *start.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *instructions.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *highscores.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *exit.png*\
‎ ‎ ‎ ‎ ↳ **pause**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *pause.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *resume.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *return.png*\
‎ ‎ ‎ ‎ ↳ **end**\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *victory.png*\
‎ ‎ ‎ ‎  ‎  ‎  ‎  ‎ ↳ *game_over.png*\


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
