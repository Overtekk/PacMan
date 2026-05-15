# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac-man.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/12 16:50:43 by roandrie        #+#    #+#               #
#  Updated: 2026/05/15 10:34:01 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from src.utils import print_error

from src.parser import load_arguments


def main() -> int:
    try:

        load_arguments()
        # load arguments
        # load_config()
        # load leaderboard
        # vérifier présente des sprites
        # vérifier présence du mazegenerator
        # call game engine qui créer maze, entity, collectibles basé sur la config
        # lance arcade.run()
        # appel gamewindow pour lancer le main menu
        # jeu
        return 0

    except ValueError as e:
        print_error(e)
        return 1

    except Exception as e:
        print_error(f"Critical error: {e}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print_error("\nProgram interrupted by user.")
        sys.exit(130)
