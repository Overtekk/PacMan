# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_engine.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:20:06 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 11:59:01 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
from src.maze import MazeFactory
from src.renderer.maze_renderer import GameRenderer
from src.renderer.screen_settings import ScreenSettings


class GameEngine(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.config = self.window.game_config
        self.game_renderer = GameRenderer()
    # main loop of the game, orchestor
    # move all entity
    # verify gamestate, levelmanager

    def update(delta: float) -> None:
        pass

    def on_show_view(self) -> None:
        self.clear()
        self.setup()

    def setup(self) -> None:
        # level = self.window.game_config.level[0]

        factory = MazeFactory()
        wall_data = factory.generate_maze(
            15, 15,
            self.window.asset_manager.textures,
            ScreenSettings.WIDTH,ScreenSettings.HEIGHT,
            self.game_renderer
        )

        self.game_renderer.wall_generator(wall_data)
        self.game_renderer.draw()



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
