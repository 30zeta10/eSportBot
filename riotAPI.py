import os
import requests

# --- Constants ---

__TOKEN = os.environ['RIOT_TOKEN']
__CHAMPION_VERSION = '10.4.1'

# --- Functions ---


# Game-Spectater Function
def game_info(summoner_name):
    blue_team = dict
    red_team = dict

    try:
        match = __v4_active_games(__v4_summoners(summoner_name).json()['id'])
        # check if we are able to spectate a game by player name
        # TODO Fall abdecken mit success != 1
        if match.status_code != 200:
            output = {
                'success': 0,
                'status_code': match.status_code,
                'message': 'Bot cant spectate ' + summoner_name
            }
            return output

        # order players by red and blue team
        # for i in match.json()['participants']:
        #    player = {'summoner': i['summonerName']
        #              }

        #   print(i)
    except Exception as err:
        error_out = {
            'success': -1,
            'func': 'get_v4_summ in game_info',
            'error': err
        }
        return error_out


# --- Private functions ----

# Get information about one summoner including the encrpted playerid
# TODO man kann beide hilfsfunktionen v4 zusammenfassen und nur über ein output machen
def __v4_summoners(summoner_name):
    try:
        data = requests.get(
            'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + __TOKEN)
    except Exception as err:
        error_out = {
            'success': -1,
            'func': 'v4summoners',
            'error': err
        }
        return error_out


# spectate for an active game
def __v4_active_games(summoner_id):
    try:
        return requests.get(
            'https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/' + summoner_id + '?api_key=' + __TOKEN)
    except Exception as err:
        error_out = {
            'success': -1,
            'func': 'v4activegames',
            'error': err
        }
        return error_out


# assign id to champion
# current Version 10.4.1
def __get_champion_list(champion_id, version):
    try:
        champion_list = requests.get(
            'http://ddragon.leagueoflegends.com/cdn/' + version + '/data/en_US/champion.json').json()
        for i in list(champion_list.json()['data']):
            if champion_list.json()['data'][i]['key'] == champion_id:
                output = {
                    'success': 1,
                    'data': i
                }
                return output

        output = {
            'success': 0,
            'data': {}
        }
        return output

    except Exception as err:
        error_out = {
            'success': -1,
            'func': 'getchampionslist',
            'error': err
        }
        return error_out


