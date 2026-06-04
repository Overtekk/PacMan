# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_config.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 14:04:22 by roandrie        #+#    #+#               #
#  Updated: 2026/06/04 11:03:13 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

debug_mode: bool = False

# :-----:
#  SPEED
# :-----:

player_speed: float = 200.0
chase_speed: float = 10

enemy_speed: float = 115.0
ennemy_speed_reduction: float = 20.0

# :-----:
#  TIMER
# :-----:

player_revive_time: float = 10
enemy_check_res_timer: float = 20

# :--------:
#  POWER-UP
# :--------:

time_power_up: float = 8.0
