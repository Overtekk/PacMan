# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_config.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 14:04:22 by roandrie        #+#    #+#               #
#  Updated: 2026/06/11 11:24:54 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

debug_mode: bool = False
delta_time_cap: float = 0.05

# :-----:
#  SPEED
# :-----:

player_speed: float = 170.0

enemy_speed: float = 115.0
ennemy_speed_reduction: float = 20.0
enemy_speed_respawn: float = 20.0

# :-----:
#  TIMER
# :-----:

player_revive_time: float = 10
enemy_check_res_timer: float = 20

# :--------:
#  POWER-UP
# :--------:

time_power_up: float = 8.0

# :-----:
#  BRAIN
# :-----:

raycasting_max_distance: int = 2
fox_detection_radius: float = 0.19 # Percentage
