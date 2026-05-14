# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac-man.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/12 16:50:43 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 21:25:25 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from src.utils import print_error

from src.config import load_config


def main() -> int:
    try:

        pass
        # load arguments
        # load_config()
        # load leaderboard
        # vérifier présente des sprites
        # vérifier présence du mazegenerator
        # call game engine qui créer maze, entity, collectibles basé sur la config
        # lance arcade.run()
        # appel gamewindow pour lancer le main menu
        # jeu

    except Exception as e:
        print_error(e)


if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print_error("\nProgram interrupted by user.")
        sys.exit(130)
