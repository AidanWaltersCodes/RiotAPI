"""File for getting my information from RIOT API"""

import requests
import os
import matplotlib.pyplot as plt
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PUUID = os.getenv("PUUID")
players = {}


"""Class for summoner object"""
class Summoner:
    def __init__(self, name):
        #info tuple = getSummonerInfo
        summonerInfo = Summoner.getSummonerInfo(name)
        self.name = name
        self.level = summonerInfo[1]     
        #self.iD = summonerInfo[0]
        #self.PUUID = summonerInfo[0]
        self.tier = summonerInfo[2]
        self.division = summonerInfo[3]
        self.leaguePoints = summonerInfo[4]
        self.winRate = summonerInfo[5]

    def to_dict(self):
        if self.level == None:
            return None
        return { self.name: {
            "Level": self.level,
            "Rank": f"{self.tier} {self.division} {self.leaguePoints} LP",
            "WinRate": f"{self.winRate}%"
        }}

    def __str__(self) -> str:
        return f"{self.name}, Level {self.level}, Rank: {self.tier} {self.division} {self.leaguePoints}, Ranked WinRate: {self.winRate}"


    def getSummonerInfo(name):
        """
        Retrieves the Summoner's Tier, Rank, LP, Wins, and Losses and fills a list with the information
        """
        summonerInfo = [name] #Create list for summoner information

        encryptedSummonerId = Summoner.getSummonerID(name)
        level = Summoner.getSummonerLevel(name)

        account_url = (f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}?api_key={API_KEY}")
        response = requests.get(account_url) #Request GET
        if response.status_code != 200:
            print(response.status_code)
            return None
        
        summonerData = response.json() #Parse content as JSON
        
        try:
            # Check if player even plays ranked
            tier = summonerData[0].get("tier")
            division = summonerData[0].get("rank")
            leaguePoints = summonerData[0].get("leaguePoints")
            wins = float(summonerData[0].get("wins"))
            losses = float(summonerData[0].get("losses"))
        except IndexError:
            return (f"{name} doesn't play ranked!")
        
        

        if tier == None:
            tier = summonerData[1].get("tier")
            division = summonerData[1].get("rank")
            leaguePoints = summonerData[1].get("leaguePoints")
            wins = float(summonerData[1].get("wins"))
            losses = float(summonerData[1].get("losses"))

        

        #Calculate Winrate
        winrate = round((wins / (wins + losses))*100, 2)
        #Gather Data

        
        if tier == None:
            return None

        summonerInfo.append(level)
        summonerInfo.append(tier)
        summonerInfo.append(division)
        summonerInfo.append(leaguePoints)
        summonerInfo.append(winrate)

        
    
        return tuple(summonerInfo)


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


    def getFavoriteChampion(name) -> str:
        #Get PUUID to gather the user's champion mastery info
        PUUID = Summoner.getPUUID(name)
        account_url = (f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{PUUID}?api_key={API_KEY}")
        masteryResponse = requests.get(account_url) #Request GET
        
        if masteryResponse.status_code != 200:
            print(masteryResponse.status_code)
            return None
        
        masteryData = masteryResponse.json()
        #print(masteryData[0])

        #From the masteryData grab the champions ID to be used to find that champion's info
        championId = (masteryData[0]['championId'])

        
        
        return(f"{Summoner.getChampionName(championId)}")


    def getPUUID(name):
        encryptedSummonerId = Summoner.getSummonerID(name)    
        url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/{encryptedSummonerId}?api_key={API_KEY}"
        response = requests.get(url)
        userData = response.json()
        #print(userData)
        PUUID = userData["puuid"]
        return PUUID


    def championPie(name, amount):
        #Get PUUID to gather the user's champion mastery info
        PUUID = Summoner.getPUUID(name)
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
            masteryNames[i] = Summoner.getChampionName(championId)
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

    def addPlayerToDictionary(name, dictionary):
        """This method will create a summoner and add it to a dictionary
            Will not be added it failed"""
        
        try:
            summoner = Summoner(name)
            dictPlayer = summoner.to_dict()
        except (KeyError, TypeError):
            return -1
        
        #Add the player to the dictionary
        dictionary.update(dictPlayer)
        return dictionary
        
    def sortDictionary(type, dictionary):
        if type == 'names': #Sort summoners in alphabetical order, .lower() is used so capital letters don't affect the order
            return dict(sorted(dictionary.items(), key=lambda x: x[0].lower(), reverse=False))
        elif type == 'namesRev': #Sort summoners in decending alphabetical order
            return dict(sorted(dictionary.items(), key=lambda x: x[0].lower(), reverse=True))
        elif type == 'levels': #Sort summoners by levels
            return dict(sorted(dictionary.items(), key=lambda x: x[1]['Level'], reverse=True))
        elif type == 'levelsRev': #Sort summoners by levels decending
            return dict(sorted(dictionary.items(), key=lambda x: x[1]['Level'], reverse=False))
        elif type == 'rank': #Sort summoners by their rank
            return dict(sorted(dictionary.items(), key=lambda x: Summoner.rankToNumber(x[1]['Rank']), reverse=True))
        elif type == 'rankRev': #Sort summoners by their rank decending
            return dict(sorted(dictionary.items(), key=lambda x: Summoner.rankToNumber(x[1]['Rank']), reverse=False))
        elif type == 'winRate': #Sort summoners by their winrate
            return dict(sorted(dictionary.items(), key=lambda x: x[1]['WinRate'], reverse=True))
        elif type == 'winRateRev': #Sort summoners by their winrate decending
            return dict(sorted(dictionary.items(), key=lambda x: x[1]['WinRate'], reverse=False))

    def rankToNumber(rank) -> int:
        """
        This will turn a rank into a number so it can be sorted easier and works like so:

        The first number will be the tier iron-challenger which will be a 0-9
        The second number will be the division but flipped becuase a lower division is considered higher so IV = 0, III = 1, II = 2, I = 3
        Finally the last digits will be the league points the player has, and in most divisions this will be 0-99. 
        However in the upper ranks this can go over 100 but the numbers will still account for that

        Example: Gold II 26 LP -> 3226
                Emerald I 77 LP -> 5377   
        """
        rankNumber = '' #Using a string to append numbers then will turn into int when returning
        rankArray = rank.split()

        if rank[0] == 'I': #Iron
            rankNumber += ('0')
        elif rank[0] == 'B': #Bronze
            rankNumber += ('1')
        elif rank[0] == 'S': #Silver
            rankNumber += ('2')
        elif rank[0] == 'G' and rank[0:1] != 'GR': #Gold
            rankNumber += ('3')
        elif rank[0] == 'P': #Platinum
            rankNumber += ('4')
        elif rank[0] == 'E': #Emerald
            rankNumber += ('5')
        elif rank[0] == 'D': #Diamond
            rankNumber += ('6')
        elif rank[0] == 'M': #Master
            rankNumber += ('7')
        elif rank[0:1] == 'GR': #GrandMaster
            rankNumber += ('8')
        elif rank[0] == 'C': #Challenger
            rankNumber += ('9')
        else:
            return -1 #Error
        
        if rankArray[1] == 'I': #I
            rankNumber += ('3')
        elif rankArray[1] == 'II': #II
            rankNumber += ('2')
        elif rankArray[1] == 'III': #III
            rankNumber += ('1')
        elif rankArray[1] == 'IV': #IV
            rankNumber += ('0')
        else:
            return -1 #Error

        if int(rankArray[2]) < 10:
            rankNumber += ('0')
            rankNumber += str(rankArray[2])
        else:
            rankNumber += str(rankArray[2])
        
        print(int(rankNumber))
        return int(rankNumber)
    
















