#file containing functions that use riot api calls

import os
import requests

from dotenv import load_dotenv 

#load riot api token from .env file
load_dotenv()
token = os.getenv('RIOT_TOKEN')

def game(summoner_name):

    request_summonerID = v4_summoners(summoner_name)
    if request_summonerID.status_code == 200:

        summonerID = request_summonerID.json()['id']
        request_match_info = v4_active_games(summonerID)

        if request_match_info.status_code == 200:

            match_info = request_match_info.json()
            blue_side = 'Blue Side: \n \n'
            red_side = 'Red Side: \n \n'    

            for summoners in match_info['participants']:
                
                if summoners['teamId'] == 100:
                
                    blue_side = blue_side + '  ' + summoners['summonerName'] + '   ' + get_champion_by_ID(summoners['championId']) + '   ' + get_soloq_rank(summoners['summonerId']) + ' \n'

                else:

                    red_side = red_side + '  ' + summoners['summonerName'] + '   ' + get_champion_by_ID(summoners['championId']) + '   ' + get_soloq_rank(summoners['summonerId']) + ' \n'                    
        
            game_info = blue_side + '\n' + red_side

            return game_info
        
        else:

            return 'Your requested summoner is currently not in-game.'


    elif request_summonerID.status_code == 404:

        return 'The requested summoner does not exist.'

    else:

        print(request_summonerID.status_code)
        return 'The servers of riot are boosted just like your teammates. Try again later!'




def v4_summoners(summoner_name):

    return requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + token)


def v4_active_games(summoner_ID):

    return requests.get('https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/' + summoner_ID + '?api_key=' + token)


def get_soloq_rank(summoner_ID):


    '''

    returns a string in the format of: <Tier Division LP Wins-Loses>
    Example: GOLD II 68LP 46-43 

    '''
    r = requests.get('https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_ID + '?api_key=' + token)
    
    json_file = r.json()

    if json_file == []:

        return 'Not ranked in yet.'

    for i in range (0, len(json_file)):

        if json_file[i]['queueType'] == 'RANKED_SOLO_5x5':

            return json_file[i]['tier'] + ' ' + json_file[i]['rank'] + ' ' + str(json_file[i]['leaguePoints']) +  'LP ' + str(json_file[i]['wins']) + '-' + str(json_file[i]['losses'])

    return 'Not ranked in yet.'



def get_champion_by_ID(champion_ID):

    #get name of a champion when given its ID

    champion_ID = str(champion_ID)
    r = requests.get('http://ddragon.leagueoflegends.com/cdn/10.4.1/data/en_US/champion.json')

    for i in list(r.json()['data']):
        if r.json()['data'][i]['key'] == champion_ID:
            return(i)