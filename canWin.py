import os
from pathlib import Path
import requests  # pip install requests
from didWin import didWin
from getRank import getRank
import time
from dotenv import load_dotenv  # pip install python-dotenv

current_dir = Path(__file__).resolve(
).parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

api_key = os.getenv("APIKEY")


# def canWin(playerName):

player = "belmin"  # = playerName

# api_url
summoner = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{namn}".format(
    namn=player)

# fetch response from the summoner (information)
resp = requests.get(summoner + "?api_key=" + api_key)
# fetch puuid (universal riot id)
puuid = resp.json()["puuid"]
# account id
accountId = resp.json()["accountId"]
# encrypted summoner id
encryptedId = resp.json()["id"]

# live match
liveGame = "https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + encryptedId

# fetch players in the live match
liveGameRequest = requests.get(liveGame + "?api_key=" + api_key)
liveGameStats = liveGameRequest.json()
participants = liveGameStats["participants"]

# save the names of all players in the match
playerNames = [name["summonerName"] for name in participants]

playerCount = 1
redWins = 0
blueWins = 0

blueTeamTier = 0
blueTeamRank = 0
blueTeamWR = 0

redTeamTier = 0
redTeamRank = 0
redTeamWR = 0

for player in playerNames:

    summoner = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{namn}".format(
        namn=player)
    resp = requests.get(summoner + "?api_key=" + api_key)
    puuid = resp.json()["puuid"]

    # Fetch latest 10 games with puuid
    matches = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuidTmp}/ids?start=0&count=10".format(
        puuidTmp=puuid) + "&api_key=" + api_key

    # Sleep to get around request limits with basic riot api key
    time.sleep(1.0)

    resp = requests.get(matches)
    matchList = resp.json()

    # Fetch current form (wr and kd) TODO kd
    wins = 0
    for match in matchList:
        time.sleep(1.0)
        if (didWin(puuid, match) == True):
            wins += 1

    playerTier, playerRank, playerWR = getRank(player)

    tierValue = 0
    rankValue = 0

    # fix this shit by making a dictionary later
    if playerTier != None:
        if playerTier == "Iron":
            tierValue = 1
        elif playerTier == "Bronze":
            tierValue = 2
        elif playerTier == "Silver":
            tierValue = 3
        elif playerTier == "Gold":
            tierValue = 4
        elif playerTier == "PLatinum":
            tierValue = 5
        elif playerTier == "Masters":
            tierValue = 6
        elif playerTier == "Grandmasters":
            tierValue = 7
        elif playerTier == "Challenger":
            tierValue = 8

    if playerRank != None:
        if playerRank == "IV":
            rankValue = 1
        elif playerRank == "III":
            rankValue = 2
        elif playerRank == "II":
            rankValue = 3
        elif playerRank == "I":
            rankValue = 4

    # Checks if the player is on either red or blue team, then assigns the points to the player's team
    if (playerCount <= 4):
        blueWins += wins
        blueTeamTier += tierValue
        blueTeamRank += rankValue
        blueTeamWR += playerWR

    elif (playerCount >= 5):
        redWins += wins
        redTeamTier += tierValue
        redTeamRank += rankValue
        redTeamWR += playerWR

    playerCount += 1


blueTeam = {
    "form": blueWins / 100,
    "averageTier": blueTeamTier / 5,
    "averageRank": blueTeamRank / 5,
    "wr": blueTeamWR / 5
}

redTeam = {
    "form": redWins / 100,
    "averageTier": redTeamTier / 5,
    "averageRank": redTeamRank / 5,
    "wr": redTeamWR / 5
}

#   return redWins, blueWins

# print(canWin("stuart littie"))


# TODO get Kills and Deaths here
# Find rank??? Create a rank point system and find average rank of team
# Make if statement to find out if chosen player is on red or blue team¨
# Compare variables to see which team is stronger
