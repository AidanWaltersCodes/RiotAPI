"""File for getting my information from RIOT API"""

import requests
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PUUID = os.getenv("PUUID")
playerName = "TheFiery1"

"""Class for summoner object"""
class Summoner:
    def __init__(self, name):
        self.name = name
        self.level = getSummonerLevel(name)       
        self.iD = getSummonerID(name)
        self.PUUID = getPUUID(name)

    def __str__(self) -> str:
        return f"{self.name}, level {self.level}, ID: {self.iD}, PUUID: {self.PUUID}"



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



def getRank(name) -> str:
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
    leaguePoints = summonerData[0].get("leaguePoints")

    if tier == None:
        tier = summonerData[1].get("tier")
        rank = summonerData[1].get("rank")
        leaguePoints = summonerData[1].get("leaguePoints")

    
    return (f"{tier} {rank} {leaguePoints} LP")

def getRankedWinrate(name) -> str:
    
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
    
    wins = float(summonerData[0].get("wins"))
    losses = float(summonerData[0].get("losses"))

    if tier == None:
        wins = float(summonerData[1].get("wins"))
        losses = float(summonerData[1].get("losses"))

    #Calculate Winrate
    winrate = round((wins / (wins + losses))*100, 2)
    return f"{winrate}"


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

    
    
    return(f"{getChampionName(championId)}")



def getPUUID(name):
    encryptedSummonerId = getSummonerID(name)    
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/{encryptedSummonerId}?api_key={API_KEY}"
    response = requests.get(url)
    userData = response.json()
    #print(userData)
    PUUID = userData["puuid"]
    return PUUID


def championPie(name, amount):
    #Get PUUID to gather the user's champion mastery info
    PUUID = getPUUID(name)
    account_url = (f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{PUUID}?api_key={API_KEY}")
    masteryResponse = requests.get(account_url) #Request GET
    
    if masteryResponse.status_code != 200:
        print(masteryResponse.status_code)
        return None

    masteryData = masteryResponse.json()

    if len(masteryData) < amount:
        return("Try a smaller amount of champions!")

    #Only get the amount of masteries specified
    #Use a mastery name array to hold the arrays of the corresponding masteries
    masteryData = masteryData[0:amount]
    masteryNames = [0] * amount
    masteryPoints = [0] * amount
    
    #populate array for labels/champ names
    for i in range(amount):
        championId = masteryData[i]['championId']
        masteryNames[i] = getChampionName(championId)
        masteryPoints[i] = masteryData[i]['championPoints']
    
    fig, ax = plt.subplots()
    ax.pie(masteryPoints, labels=masteryNames, autopct='%1.1f%%', radius=1.2)
    ax.set(aspect="equal")
    ax.set_title(f"Champion Pie for {name} Top {amount} Masteries", y=1.075)
    plt.show()

    return("Success!")

    

def getChampionName(championId) -> str:
    #URL for champion data file
    url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json"
    response = requests.get(url)
    championData = response.json() #Parse content as JSON

    #Loop through json file and check each champion for a key match to the id
    for i in range(len(championData["data"])):
        champion = list(championData["data"].keys())[i]
        if championData["data"][champion].get("key") == str(championId):
            foundChamp = champion
            break
    return foundChamp

summoner1 = Summoner(playerName)
summoner2 = Summoner('ryzalkorz')


