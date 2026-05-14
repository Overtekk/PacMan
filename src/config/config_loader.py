# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_loader.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 16:57:57 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 19:17:28 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path

from .config_schema import GameConfig


def load_config(filepath: Path) -> GameConfig:
    GameConfig.model_validate_json(filepath)

    # Verify if data folder exist, if exist, check permission
    # Verify if config file exist, if exist, check permission
    # If no data folder, create it
    # If config file do not exist, create it or error

    # -- CONFIG --
    # check if json is valid
    # check all keys, add default ones if invalid or do not exist
    # allows comments with '#'
    # if invalid exist, ignore it

    # return GameConfig with all instance validate and config send by the user
