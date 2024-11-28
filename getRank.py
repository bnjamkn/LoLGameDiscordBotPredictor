import os
from pathlib import Path
import requests
import time

from dotenv import load_dotenv

current_dir = Path(__file__).resolve(
).parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

api_key = os.getenv("APIKEY")

# Assign values to all ranks


def getRank(player):
    api_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player}".format(
        player=player) + "?api_key=" + api_key
    response = requests.get(api_url)
    playerInfo = response.json()
    encryptedId = playerInfo["id"]

    time.sleep(1.0)

    rank_api_url = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedId}".format(
        encryptedId=encryptedId) + "?api_key=" + api_key

    response = requests.get(rank_api_url)
    playerInfo = response.json()

    # Checks if there is a solo queue rank and at its index, then saves it to variables rank and tier
    rank = None
    tier = None

    for rank in playerInfo:
        if rank["queueType"] == "RANKED_SOLO_5x5":
            soloRank = rank

    if rank != None:
        rank = soloRank["rank"]
        tier = soloRank["tier"]

    playerRank = tier, rank

    seasonWR = (playerInfo[0]["wins"]) / \
        (playerInfo[0]["wins"] + playerInfo[0]["losses"])

    return tier, rank, seasonWR


getRank("whatchugonnado")
