"""File for getting my information from RIOT API"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PUUID = os.getenv("PUUID")
playerName = "TheFiery1"


def getSummonerLevel(name) -> int:
    """
    Finds the level of a summoner based on their name
    
    Parameters:
    - name (str): The name of the account.

    Returns:
    int: The level of the account.

    """
    account_url = (f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={API_KEY}") #URL for Summoner Info
    response = requests.get(account_url) #Request GET
    if response.status_code != 200:
        return -1
    summonerData = response.json() #Parse content as JSON
    level = summonerData.get("summonerLevel")
    return level



def getSummonerID(name) -> str:
    """
    Finds the id of a summoner based on their name
    
    Parameters:
    - name (str): The name of the account.

    Returns:
    str: The id of the account.

    """
    account_url = (f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={API_KEY}")
    response = requests.get(account_url) #Request GET
    if response.status_code != 200:
        return None
    summonerData = response.json() #Parse content as JSON
    id = summonerData.get("id")
    return id



def getSummonerRankedInfo(name) -> str:
    """
    Finds the rank of a summoner based on their name and their winrate
    
    Parameters:
    - name (str): The name of the account.

    Returns:
    str: The rank of the account and what division they are in as well as their winrate
    
    """
    encryptedSummonerId = getSummonerID(name)
    account_url = (f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}?api_key={API_KEY}")
    response = requests.get(account_url) #Request GET
    if response.status_code != 200:
        print(response.status_code)
        return None
    
    summonerData = response.json() #Parse content as JSON
    
    #Gather Data
    try:
        # Check if player even plays ranked
        tier = summonerData[0].get("tier")
    except IndexError:
        return (f"{name} doesn't play ranked!")
    
    rank = summonerData[0].get("rank")
    wins = float(summonerData[0].get("wins"))
    losses = float(summonerData[0].get("losses"))

    if tier == None:
        tier = summonerData[1].get("tier")
        rank = summonerData[1].get("rank")
        wins = float(summonerData[1].get("wins"))
        losses = float(summonerData[1].get("losses"))

    #Calculate Winrate
    winrate = round((wins / (wins + losses))*100, 2)
    
    return (f"{tier} {rank} Winrate:{winrate}%")



def getFavoriteChampion(name) -> str:
    #Get PUUID to gather the user's champion mastery info
    PUUID = getPUUID(name)
    account_url = (f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{PUUID}?api_key={API_KEY}")
    masteryResponse = requests.get(account_url) #Request GET
    
    if masteryResponse.status_code != 200:
        print(masteryResponse.status_code)
        return None
    
    masteryData = masteryResponse.json()
    #print(masteryData[0])

    #From the masteryData grab the champions ID to be used to find that champion's info
    championId = (masteryData[0]['championId'])

    #URL for champion data file
    url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json"
    response = requests.get(url)
    championData = response.json() #Parse content as JSON


    #Loop through json file and check each champion for a key match to the id of the user's most used champion
    for i in range(len(championData["data"])):
        champion = list(championData["data"].keys())[i]
        if championData["data"][champion].get("key") == str(championId):
            favChamp = champion
            #print(f"found {favChamp}")
            break
    
    return(f"{champion}")



def getPUUID(name):
    encryptedSummonerId = getSummonerID(name)    
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/{encryptedSummonerId}?api_key={API_KEY}"
    response = requests.get(url)
    userData = response.json()
    #print(userData)
    PUUID = userData["puuid"]
    return PUUID


print(f"The Level is {getSummonerLevel(playerName)}")
print(f"The SummonerID is {getSummonerID(playerName)}")
print(f"The Ranked info is {getSummonerRankedInfo(playerName)}")
print(f"Their favorite champion is {getFavoriteChampion(playerName)}")

print(f"The Level is {getSummonerLevel('ryzalkorz')}")
print(f"The SummonerID is {getSummonerID('ryzalkorz')}")
print(f"The Ranked info is {getSummonerRankedInfo('ryzalkorz')}")
print(f"Their favorite champion is {getFavoriteChampion('ryzalkorz')}")

print(f"The Level is {getSummonerLevel('SirFrostington')}")
print(f"The SummonerID is {getSummonerID('SirFrostington')}")
print(f"The Ranked info is {getSummonerRankedInfo('SirFrostington')}")
print(f"Their favorite champion is {getFavoriteChampion('SirFrostington')}")

print(f"The Level is {getSummonerLevel('BADATMNK')}")
print(f"The SummonerID is {getSummonerID('BADATMNK')}")
print(f"The Ranked info is {getSummonerRankedInfo('BADATMNK')}")
print(f"Their favorite champion is {getFavoriteChampion('BADATMNK')}")

print(f"The Level is {getSummonerLevel('roberto1267')}")
print(f"The SummonerID is {getSummonerID('roberto1267')}")
print(f"The Ranked info is {getSummonerRankedInfo('roberto1267')}")
print(f"Their favorite champion is {getFavoriteChampion('roberto1267')}")

print(f"The Level is {getSummonerLevel('BobbyLoach')}")
print(f"The SummonerID is {getSummonerID('BobbyLoach')}")
print(f"The Ranked info is {getSummonerRankedInfo('BobbyLoach')}")
print(f"Their favorite champion is {getFavoriteChampion('BobbyLoach')}")


