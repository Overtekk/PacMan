# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  leaderboard_schema.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 17:55:42 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 17:58:26 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field


class PlayerScore(BaseModel):
    player_name: str = Field(
        description="Name of the player",
    )
    player_score: float = Field(
        description="Score of the player"
    )


class Leaderboard(BaseModel):
    scores: list[PlayerScore] = Field(
        description="List of player scores"
    )
