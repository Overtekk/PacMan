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
- a un moment un fantome est devenu bleu et ne pouvait plus manger ni etre mange, manger un burger n'a pas debuguer la situation
- dans le run-debug souvent le chat avait son rayon rouge au debut puis apres il n'en n'avait plus alors que les autres le gardaient tout du long
- on ne peut pas spam gauche droite avec le pacman qui fait exactement gauche droite au moment ou on appuie, manque de fluidite, on peut pas manier le pacman comme on voudrait
- quand un ghost apparait alors qu'un autre burger a ete mange il ne nait pas bleu (jsp si c'est normal??)
- manger un burger en mode invincible desactive le mode invinsible (jsp si c'est normal??)
- les ennemis tournent en rond et se bloquent (aussi lorsqu'ils sont morts et essaient de retourner a leur spawn point)
- des fois des fantomes ne me tuent pas alors qu'ils sont dans leur skin de tueur, souvent quand jai mange plusieurs burgers et/ou qu'ils sont deja morts -> jarrive pas a identifier si le probleme est le fait de manger plusieurs burgers, ou si c'est parce qu'ils ont ete tues, ou les 2 en meme temps
-  cheat next level crash si le next level c'est finish screen
