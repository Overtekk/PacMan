# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_engine.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:20:06 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 17:25:54 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from src.renderer.maze_renderer import GameRenderer
from .level_manager import LevelManager
from .collision_manager import CollisionManager


class GameEngine(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.initialized = False
        self.config = self.window.game_config
        self.game_renderer = GameRenderer()

        self.level_manager = LevelManager(
            game_window=self.window
        )

        self._game_paused: bool = False

    def on_update(self, delta_time: float) -> None:
        if self._game_paused:
            return

        # Check for collisions
        self.coll_manager.update()

        # Update all entities
        self.player.update(delta_time)

    def on_draw(self) -> None:
        self.clear()

        # Render the game
        self.game_renderer.draw()

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player._next_direction = (0, 1)

        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player._next_direction = (0, -1)

        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player._next_direction = (-1, 0)

        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player._next_direction = (1, 0)


    def on_show_view(self) -> None:
        # Clear the screen
        self.clear()

        # Call the setup method
        if not self.initialized:
            self.initialized = True
            self.setup()

    def setup(self) -> None:
        level_index: int = 0

        # Create the level
        level: list[list[int]] = self.level_manager.create_level(
            level_name=self.config.level[level_index].name,
            maze_width=self.config.level[level_index].width,
            maze_height=self.config.level[level_index].height
        )

        self.player = self.level_manager.player
        self.cat_enemy = self.level_manager.enemies_list["cat_enemy"]
        self.fox_enemy = self.level_manager.enemies_list["fox_enemy"]
        self.rat_enemy = self.level_manager.enemies_list["rat_enemy"]
        self.dog_enemy = self.level_manager.enemies_list["dog_enemy"]

        # Generate the walls rendering
        self.game_renderer.wall_generator(level)
        # Generate entities rendering
        self.game_renderer.setup_entities(self.player.sprite)
        self.game_renderer.setup_entities(self.cat_enemy.sprite)
        self.game_renderer.setup_entities(self.fox_enemy.sprite)
        self.game_renderer.setup_entities(self.rat_enemy.sprite)
        self.game_renderer.setup_entities(self.dog_enemy.sprite)

        # Temp: authorize the player to move
        self.player._can_move = True

        # Instanciate the CollisionManager
        self.coll_manager: CollisionManager = CollisionManager(
            self.player, self.level_manager.enemies_list,
            self.level_manager.byte_maze,
            self.level_manager.factory.offset_x,
            self.level_manager.factory.offset_y,
            self.level_manager.factory.tile_size,
            self.level_manager.maze_height
        )

    @property
    def game_paused(self) -> bool:
        return self._game_paused

    @game_paused.setter
    def game_paused(self, new_value: bool) -> None:
        self._game_paused = new_value



        # === ÉTAPE 1 : INITIALISATION DE L'ÉTAT DU JEU (GameStateManager) ===
        # - Instancier (ou réinitialiser) le GameStateManager.
        # - Configurer le score à 0.
        # - Récupérer le nombre de vies max depuis self.window.game_config et l'assigner.
        # - Définir le niveau courant (commencer à l'index 0).

        # === ÉTAPE 2 : LECTURE DE LA CONFIGURATION DU NIVEAU ===
        # - Extraire les données du niveau actuel (width, height) depuis self.window.game_config.level[index_niveau_courant].
        # - Extraire la seed (si présente) pour la génération.

        # === ÉTAPE 3 : GÉNÉRATION DU LABYRINTHE (LevelManager) ===
        # - Instancier le LevelManager.
        # - Appeler sa méthode de génération en lui passant les dimensions extraites à l'étape 2.
        # - Le LevelManager doit construire ses SpriteLists (murs, pac-gums) en demandant les chemins des images à self.window.sprites_list.

        # === ÉTAPE 4 : PLACEMENT DES ENTITÉS MOBILES ===
        # - Déterminer les coordonnées de départ du joueur et des ennemis (idéalement fournies par le LevelManager en fonction du labyrinthe généré).
        # - Instancier le Player et le placer dans une SpriteList dédiée au joueur.
        # - Instancier les entités ennemies (Chat, Chien, etc.) et les placer dans une SpriteList dédiée aux ennemis.

        # === ÉTAPE 5 : PARAMÉTRAGE DES COLLISIONS (CollisionManager) ===
        # - Instancier le CollisionManager.
        # - Lui transmettre les références des différentes SpriteLists (Joueur, Murs, Pac-gums, Ennemis) pour qu'il puisse vérifier les interactions dans on_update().

        # === ÉTAPE 6 : PRÉPARATION VISUELLE ET SONORE ===
        # - (Optionnel) Lancer un chronomètre ou un état "Ready!" avant d'autoriser les mouvements.
        # - (Optionnel) Charger et lancer la musique du niveau via un AudioLoader si implémenté.
