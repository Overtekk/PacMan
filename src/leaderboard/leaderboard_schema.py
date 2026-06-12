# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  leaderboard_schema.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 17:55:42 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:13:17 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field


class PlayerScore(BaseModel):
    """Data Validation Model representing an individual historical attempt
    record.

    Attributes:
        player_name: String identifying the profile or moniker of the actor.
        player_score: Floating numerical metric tracking total accumulated
        points.
    """
    player_name: str = Field(
        description="Name of the player",
    )
    player_score: float = Field(
        description="Score of the player"
    )


class Leaderboard(BaseModel):
    """Root Serialization Matrix managing archival scoreboard rankings
    collections.

    Attributes:
        scores: Sequence array tracking validated PlayerScore database node
        objects.
    """
    scores: list[PlayerScore] = Field(
        description="List of player scores"
    )
