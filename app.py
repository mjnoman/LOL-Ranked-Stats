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
        
        #If region isn't Korea or Russia, need to add a 1 to region
        if region != 'KR' and region != 'RU':
            region += '1'
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

        #Set all champ names to lowercase to render images
        chars = fixNames(chars)

        #Grab match data
        matchIDs = []
        matchData = []

        for i in range(10):
            tempMatchResult = recentMatch['matches'][i]
            matchIDs.append(tempMatchResult['gameId'])

        for each in matchIDs:
            try:
                matchData.append(getData(region, 'fourth', each, aKey))
            except:
                return render_template('error.html')
        bansBlue = []
        bansRed = []
        
        fullBlueData = []
        fullRedData = []
        partId = []
        partName = []
        partChamp = []
        strData = []
        minion = []
        level = []
        num = 0
        #Grab all data from each side
        for each in matchData:
            gameDurationSec = each['gameDuration']

            blueId = each['teams'][0]['teamId']
            winStatBlue = each['teams'][0]['win']
            
            for all in each['teams'][0]['bans']:
                bansBlue.append(all['championId'])

            redId = each['teams'][1]['teamId']
            winStatRed = each['teams'][1]['win']
            
            for all in each['teams'][1]['bans']:
                bansRed.append(all['championId'])


            
            for i in range(10):
                partId.append(each['participants'][i]['participantId'])
                partName.append(each['participantIdentities'][partId[i] - 1]['player']['summonerName'])
                partChamp.append(each['participants'][i]['championId'])
                strData.append(str(each['participants'][i]['stats']['kills']) + '/' + str(each['participants'][i]['stats']['deaths']) + '/' + str(each['participants'][i]['stats']['assists']))
                minion.append(each['participants'][i]['stats']['totalMinionsKilled'] + each['participants'][i]['stats']['neutralMinionsKilled'] + each['participants'][i]['stats']['neutralMinionsKilledTeamJungle'] + each['participants'][i]['stats']['neutralMinionsKilledEnemyJungle'])
                level.append(each['participants'][i]['stats']['champLevel'])
            
            for i in range(5):
                if type(partName[i + num]) == 'str':
                    fullBlueData.append(partName[i + num] + "\t" + strData[i + num] + '\t' + str(minion[i + num]) + " CS\tLevel " + str(level[i + num]))
                else:
                    fullBlueData.append(partName[i + num] + "\t" + strData[i + num] + '\t' + str(minion[i + num]) + " CS\tLevel " + str(level[i + num]))
            for i in range(5, 10):
                if type(partName[i + num]) == 'str':
                    fullRedData.append(partName[i + num] + "\t" + strData[i + num] + '\t' + str(minion[i + num]) + " CS\tLevel " + str(level[i + num]))
                else:
                    fullRedData.append(partName[i + num] + "\t" + strData[i + num] + '\t' + str(minion[i + num]) + " CS\tLevel " + str(level[i + num]))
            num = num + 10
        teamChamps = []
        for champId in partChamp:
            for each in champNameList:
                if (int(champNameList[each]['key']) == champId):
                    teamChamps.append(champNameList[each]['id'])
        teamChamps = fixNames(teamChamps)
        redTeamChamps = []
        blueTeamChamps = []
        
        for i in range(0, len(teamChamps)):
            if (i%10 == 0) or (i%10 == 1) or (i%10 == 2) or (i%10 == 3) or (i%10 == 4):
                blueTeamChamps.append(teamChamps[i])
            else:
                redTeamChamps.append(teamChamps[i])
        #for i in range(5):
        #    blueTeamChamps.append(teamChamps[i])
        #for i in range(5,10):
        #    redTeamChamps.append(teamChamps[i])
        
        #Remove space ascii value and return the spaces to the name
        if(summName is not None):
            summName = summName.replace('%20', ' ')

        statsStyle = "border : 4px solid black;"
        #Render the html page, passing each of the grabbed values
        return render_template('index.html', summName=summName, blueTeam=fullBlueData, blueTeamCh=blueTeamChamps, 
                                redTeam=fullRedData, redTeamCh=redTeamChamps, champs=chars, rankTier=rankTier, 
                                divTier = divTier, leagueP = leagueP, wins = wins, losses = losses, 
                                statsStyle=statsStyle, winPct = winPct)
    else:
        return render_template('index.html')

#Sends api requests(or download from ddragon) to Riot Games for user info
def getData(region, urlCh, urlFin, aKey):
    if(urlCh == 'first'):
        url = "https://"+region+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"+urlFin+"?api_key="+aKey
    elif(urlCh == 'second'):
        url = "https://"+region+".api.riotgames.com/lol/match/v4/matchlists/by-account/"+urlFin+"?api_key="+aKey
    elif(urlCh == 'third'):
        url = "https://"+region+".api.riotgames.com/lol/league/v4/entries/by-summoner/"+urlFin+"?api_key="+aKey
    elif(urlCh == 'fourth'):
        url = "https://"+region+".api.riotgames.com/lol/match/v4/matches/"+str(urlFin)+"?api_key="+aKey
    else:
        url = "https://ddragon.leagueoflegends.com/cdn/10.23.1/data/en_US/champion.json"
    jsonData = urllib.request.urlopen(url).read()
    return json.loads(jsonData)

#Fix up user's ranked division name
def rankNameFix(capital):
    correctName = ""
    for each in capital:
        correctName += each.lower()
    return correctName.capitalize()

def fixNames(chars):
    for i in range(len(chars)):
        chars[i] = chars[i].lower()
    return chars

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
