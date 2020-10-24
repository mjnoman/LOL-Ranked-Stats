from flask import Flask, render_template, request
import urllib.request, json
import math
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        pass
    #For after user inputs name and server
    if request.method == 'POST':
        #Grabbing data and initializing variables passed to page
        region = request.form.get('region')
        summName = request.form.get('name')
        aKey = os.environ.get('api_key')

        #Replace any space with ascii value
        if(summName is not None):
            summName = summName.replace(' ', '%20')

        #Try to grab account data with name, else render error page
        try:
            data_summ = getData(region, 'first', summName, aKey)
        except:
            return render_template('error.html')

        #Grab account Id and riot ID from return data
        accountId = data_summ['accountId']
        riotId = data_summ['id']

        #Try to grab recent match data, else render error page
        try:
            recentMatch = getData(region, 'second', accountId, aKey)
        except:
            return render_template('error.html')

        #Grab each champion ID's of champions user has played in ranked
        chids = []
        for i in range(10):
            tempMatchData = recentMatch['matches'][i]
            chids.append(tempMatchData['champion'])

        #Try to get ranked stats for player, else render error page
        try:
            rankStat = getData(region, 'third', riotId, aKey)
        except:
            return render_template('error.html')

        #Grab data from the return json 
        rankedTier = rankStat[0]['tier']
        rankTier = rankNameFix(rankedTier)
        divTier = rankStat[0]['rank']
        leagueP = rankStat[0]['leaguePoints']
        wins = rankStat[0]['wins']
        losses = rankStat[0]['losses']
        winPct = math.floor((wins*100)/(wins + losses))

        #Try to grab champion data from ddragon, else render error page
        try:
            champName = getData(region, 'fifth', None, aKey)
        except:
            return render_template('error.html')

        #Grab champion names and add them to list
        chars = []
        champNameList = champName['data']
        for champId in chids:
            for each in champNameList:
                if (int(champNameList[each]['key']) == champId and champNameList[each]['id'] not in chars):
                    chars.append(champNameList[each]['id'])
        
        #If names need to be presented, this will fixed internal names
        #charsFixed = champNameFix(chars)

        #Grab match data
        matchIDs = []
        matchData = []

        for i in range(1):
            tempMatchResult = recentMatch['matches'][i]
            matchIDs.append(tempMatchResult['gameId'])
        
        for each in matchIDs:
            try:
                matchData.append(getData(region, 'fourth', each, aKey))
            except:
                return render_template('error.html')



        #Remove space ascii value and return the spaces to the name
        if(summName is not None):
            summName = summName.replace('%20', ' ')
        
        #Render the html page, passing each of the grabbed values
        return render_template('index.html', summName=summName, matchData=matchData, champs=chars, rankTier=rankTier, divTier = divTier, leagueP = leagueP, wins = wins, losses = losses, winPct = winPct)
    else:
        return render_template('index.html')

#Sends api requests(or download from ddragon) to Riot Games for user info
def getData(region, urlCh, urlFin, aKey):
    if(urlCh == 'first'):
        url = "https://"+region+"1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+urlFin+"?api_key="+aKey
    elif(urlCh == 'second'):
        url = "https://"+region+"1.api.riotgames.com/lol/match/v4/matchlists/by-account/"+urlFin+"?api_key="+aKey
    elif(urlCh == 'third'):
        url = "https://"+region+"1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+urlFin+"?api_key="+aKey
    elif(urlCh == 'fourth'):
        url = "https://"+region+"1.api.riotgames.com/lol/match/v4/matches/"+str(urlFin)+"?api_key="+aKey
    else:
        url = "https://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json"
    jsonData = urllib.request.urlopen(url).read()
    return json.loads(jsonData)

#Fix up user's ranked division name
def rankNameFix(capital):
    correctName = ""
    for each in capital:
        correctName += each.lower()
    return correctName.capitalize()

#If used it will convert internal champion name strings to match actual names
def champNameFix(chName):
    for i in range(len(chName)):
        if(chName[i] == 'AurelionSol'):
            chName[i] = 'Aurelion Sol'
        elif(chName[i] == 'Chogath'):
            chName[i] = 'Cho\'Gath'
        elif(chName[i] == 'DrMundo'):
            chName[i] = 'Dr. Mundo'
        elif(chName[i] == 'JarvanIV'):
            chName[i] = 'Jarvan IV'
        elif(chName[i] == 'Kaisa'):
            chName[i] = 'Kai\'Sa'
        elif(chName[i] == 'Khazix'):
            chName[i] = 'Kha\'Zix'
        elif(chName[i] == 'Kogmaw'):
            chName[i] = 'Kog\'Maw'
        elif(chName[i] == 'Leblanc'):
            chName[i] = 'LeBlanc'
        elif(chName[i] == 'LeeSin'):
            chName[i] = 'Lee Sin'
        elif(chName[i] == 'MasterYi'):
            chName[i] = 'Master Yi'
        elif(chName[i] == 'MissFortune'):
            chName[i] = 'Miss Fortune'
        elif(chName[i] == 'MonkeyKing'):
            chName[i] = 'Wukong'
        elif(chName[i] == 'Reksai'):
            chName[i] = 'Rek\'Sai'
        elif(chName[i] == 'TwistedFate'):
            chName[i] = 'Twisted Fate'
        elif(chName[i] == 'Velkoz'):
            chName[i] = 'Vel\'Koz'
        elif(chName[i] == 'XinZhao'):
            chName[i] = 'Xin Zhao'
    return chName

if __name__ == '__main__':
    app.run()
