# RISKS — Bug, problem
#### *anacharp + roandrie*

---
Parsing:
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


bugs :
- lorsqu'on mange un burger on ne peut plus manger de pacgums pendant un certain moment (j'ai pas test avec un autre burger)
- a un moment un fantome est devenu bleu et ne pouvait plus manger ni etre mange, manger un burger n'a pas debuguer la situation
- dans le run-debug souvent le chat avait son rayon rouge au debut puis apres il n'en n'avait plus alors que les autres le gardaient tout du long
- on ne peut pas spam gauche droite avec le pacman qui fait exactement gauche droite au moment ou on appuie, manque de fluidite, on peut pas manier le pacman comme on voudrait
- alors jai mange un burger, jarrivai pas a mager les pacgums et du coup jai essaye de manger un burger, jai aussi mange un fantome mais le burger jai pas pu et ca a fait crash le jeu avec le message suivant :
```bash
Traceback (most recent call last):
  File "/goinfre/anacharp/pacmanito/pac-man.py", line 69, in <module>
    sys.exit(main())
             ~~~~^^
  File "/goinfre/anacharp/pacmanito/pac-man.py", line 54, in main
    arcade.run()
    ~~~~~~~~~~^^
  File "/goinfre/anacharp/pacmanito/.venv/lib/python3.14/site-packages/arcade/window_commands.py", line 152, in run
    pyglet.app.run(None)
    ~~~~~~~~~~~~~~^^^^^^
  File "/goinfre/anacharp/pacmanito/.venv/lib/python3.14/site-packages/pyglet/app/__init__.py", line 81, in run
    event_loop.run(interval)
    ~~~~~~~~~~~~~~^^^^^^^^^^
  File "/goinfre/anacharp/pacmanito/.venv/lib/python3.14/site-packages/pyglet/app/base.py", line 164, in run
    timeout = self.idle()
  File "/goinfre/anacharp/pacmanito/.venv/lib/python3.14/site-packages/pyglet/app/base.py", line 232, in idle
    self.clock.call_scheduled_functions(dt)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^
  File "/goinfre/anacharp/pacmanito/.venv/lib/python3.14/site-packages/pyglet/clock.py", line 217, in call_scheduled_functions
    item.func(now - item.last_ts, *item.args, **item.kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/goinfre/anacharp/pacmanito/.venv/lib/python3.14/site-packages/arcade/application.py", line 545, in _dispatch_frame
    self._dispatch_updates(delta_time)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/goinfre/anacharp/pacmanito/.venv/lib/python3.14/site-packages/arcade/application.py", line 579, in _dispatch_updates
    self.dispatch_event("on_update", GLOBAL_CLOCK.delta_time)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/goinfre/anacharp/pacmanito/.venv/lib/python3.14/site-packages/pyglet/window/__init__.py", line 686, in dispatch_event
    super().dispatch_event(*args)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "/goinfre/anacharp/pacmanito/.venv/lib/python3.14/site-packages/pyglet/event.py", line 364, in dispatch_event
    if handler(*args):
       ~~~~~~~^^^^^^^
  File "/goinfre/anacharp/pacmanito/src/game_engine/game_engine.py", line 122, in on_update
    s_pacgum.update(delta_time)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/goinfre/anacharp/pacmanito/src/entity/collectibles/super_pacgum.py", line 64, in update
    self._deactivate_effect()
    ~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/goinfre/anacharp/pacmanito/src/entity/collectibles/super_pacgum.py", line 129, in _deactivate_effect
    if game_config._mode:
       ^^^^^^^^^^^^^^^^^
AttributeError: module 'src.game_config' has no attribute '_mode'
```

