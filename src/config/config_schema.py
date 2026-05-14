# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_schema.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 17:33:19 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 17:37:09 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field


class LevelConfig(BaseModel):
    name: str = Field(
        default="level_name",
        description="Name of a level"
    )
    width: int = Field(
        default="20",
        description="Width of a level"
    )
    height: int = Field(
        default=20,
        description="Height of a level"
    )


class GameConfig(BaseModel):
    highscore_filename: str = Field(
        default="data/leaderboard.json",
        description="File including all scores"
    )
    lives: int = Field(
        default=3,
        description="Number of lives of the player"
    )
    pacgum_points: int = Field(
        default=10,
        description="Points earned with pacgum"
    )
    super_pacgum_points: int = Field(
        default=50,
        description="Points earned with super_pacgum"
    )
    ghost_points: int = Field(
        default=200,
        description="Points earned when eat ghost"
    )
    seed: str = Field(
        default="koala",
        description="Seed used for the first level"
    )
    level_max_time: float = Field(
        default=180.0,
        description="Time for completing a level"
    )
    level: list[LevelConfig] = Field(
        description="List of all levels"
    )
