# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_config.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 14:04:22 by roandrie        #+#    #+#               #
#  Updated: 2026/06/09 11:56:42 by roandrie        ###   ########.fr        #
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
enemy_chase_speed: float = 51
enemy_angry_speed: float = 50

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
