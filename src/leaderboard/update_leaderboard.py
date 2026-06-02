# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  update_leaderboard.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 17:53:46 by roandrie        #+#    #+#               #
#  Updated: 2026/06/02 17:39:40 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import json


def save_score_to_leaderboard(
    file: str, player_name: str, score: float, cheater_or_not: bool
) -> None:

    # If player_name is too long, cut the characters
    if len(player_name) > 10:
        player_name = player_name[0:10]

    # If score is negative by magic trick, put it to 0
    if score < 0:
        score = 0

    # Store the data
    if cheater_or_not is True:
        cheater_name = f"CHEATER {player_name}"
        player_data: dict[str, Any] = {
            "player_name": cheater_name,
            "player_score": int(score)
        }
    else:
        player_data: dict[str, Any] = {
            "player_name": player_name,
            "player_score": int(score)
        }

    # Get all the leaderboard
    data: Any = open_leaderboard(file)

    # Verify if there is not negative number JUST IN CASE
    data = _verify_score(data)

    # Verify that the player doesn´t exist. If so, change only his score
    exist: bool = False
    for player in data["scores"]:
        if player["player_name"] == player_name:
            player["player_score"] = score
            exist = True
            break

    if not exist:
        data["scores"].append(player_data)

    # Remove the lower score if there are more than 10 entries
    if len(data["scores"]) >= 10:
        while len(data["scores"]) != 10:
            data["scores"].remove(_find_lowest_score(data["scores"]))

    # Sort the leaderboard from the highest score to the lowest
    data = _sort_leaderboard(data)

    # Open and write in the json output
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def open_leaderboard(file: str) -> Any:

    with open(file, 'r', encoding='utf-8') as f:
        data: Any = json.load(f)

    return data


def _find_lowest_score(data: dict[dict[str, Any]]) -> dict[str, Any]:
    weakest_player: dict[str, Any] = {
        "player_name": "",
        "player_score": float('+inf')
    }

    for player in data:
        if player["player_score"] < weakest_player["player_score"]:
            weakest_player["player_name"] = player["player_name"]
            weakest_player["player_score"] = player["player_score"]

    return weakest_player


def _sort_leaderboard(
    data: dict[str, list[dict[str, Any]]]
) -> dict[str, list[dict[str, Any]]]:

    data["scores"].sort(
        key=lambda player: player["player_score"], reverse=True
    )
    return data


def _verify_score(
    data: dict[str, list[dict[str, Any]]]
) -> dict[str, list[dict[str, Any]]]:

    data["scores"] = [player for player in data["scores"]
                      if player["player_score"] >= 0]

    return data
