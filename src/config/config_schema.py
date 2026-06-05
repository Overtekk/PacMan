# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_schema.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 17:33:19 by roandrie        #+#    #+#               #
#  Updated: 2026/06/05 13:21:37 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field


class LevelConfig(BaseModel):
    name: str = Field(
        min_length=1,
        default="level_name",
        description="Name of a level"
    )
    width: int = Field(
        ge=4, le=42,
        default=20,
        description="Width of a level"
    )
    height: int = Field(
        ge=4, le=42,
        default=20,
        description="Height of a level"
    )


DEFAULT_LEVELS: list[LevelConfig] = [
    LevelConfig(name="Level 1", width=20, height=10),
    LevelConfig(name="Level 2", width=18, height=12),
    LevelConfig(name="Level 3", width=10, height=10),
    LevelConfig(name="Level 4", width=10, height=20),
    LevelConfig(name="Level 5", width=15, height=21),
    LevelConfig(name="Level 6", width=14, height=10),
    LevelConfig(name="Level 7", width=15, height=10),
    LevelConfig(name="Level 8", width=12, height=16),
    LevelConfig(name="Level 9", width=14, height=10),
    LevelConfig(name="Level 10", width=20, height=20),
]


class GameConfig(BaseModel):
    highscore_filename: str = Field(
        min_length=6,
        pattern=r'^data/.+\.json$',
        default="data/leaderboard.json",
        description="File including all scores"
    )
    live: int = Field(
        ge=1.0, le=9999.0,
        default=3,
        description="Number of lives of the player"
    )
    pacgum_points: float = Field(
        ge=1.0, le=9999.0,
        default=10,
        description="Points earned with pacgum"
    )
    super_pacgum_points: float = Field(
        ge=1.0, le=9999.0,
        default=50,
        description="Points earned with super_pacgum"
    )
    ghost_points: float = Field(
        ge=1.0, le=9999.0,
        default=200,
        description="Points earned when eat ghost"
    )
    seed: str = Field(
        min_length=1,
        default="koala",
        description="Seed used for the first level"
    )
    level_max_time: float = Field(
        ge=1.0, le=9999.0,
        default=180.0,
        description="Time for completing a level"
    )
    level: list[LevelConfig] = Field(
        default_factory=lambda: DEFAULT_LEVELS.copy(),
        min_length=1,
        max_length=10,
        description="List of all levels"
    )
