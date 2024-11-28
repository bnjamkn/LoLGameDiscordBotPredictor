import os
from pathlib import Path
import requests

from dotenv import load_dotenv

current_dir = Path(__file__).resolve(
).parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

api_key = os.getenv("APIKEY")


def didWin(puuid, match):
    matchApi = "https://europe.api.riotgames.com/lol/match/v5/matches/" + \
        match + "?api_key=" + api_key
    response = requests.get(matchApi)
    matchData = response.json()
    participantIndex = matchData['metadata']['participants'].index(puuid)

    return matchData["info"]["participants"][participantIndex]["win"]
