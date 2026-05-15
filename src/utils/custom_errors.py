# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  custom_errors.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 09:28:52 by roandrie        #+#    #+#               #
#  Updated: 2026/05/15 09:35:24 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


class MazeGenerationError(Exception):
    pass


class ConfigError(Exception):
    pass
