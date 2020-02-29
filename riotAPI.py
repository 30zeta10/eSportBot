import os
import requests

# --- Constants ---

__TOKEN = os.environ['RIOT_TOKEN']
__CHAMPION_VERSION = '10.4.1'

# --- Functions ---


# Game-Spectater Function
def game_info(summoner_name):
    teams = {}
    blue_team = []
    red_team = []
    try:
        match = __v4_active_games(summoner_name)
        # check if we are able to spectate a game by player name
        if match['success'] != 1 or match['status_code'] != 200:
            output = {
                'success': 0,
                'status_code': match['status_code'],
                'message': 'Bot cant spectate ' + summoner_name + '.'
            }
            return output

        for summoner in match['data']['participants']:
            player = {}
            # TODO die get_solo_q Rückgabewert ist bullshit
            if summoner['teamId'] == 100:
                player['summonerName'] = summoner['summonerName']
                player['rank'] = __get_solo_q_rank(summoner['summonerId'])
                # TODO champion name
                blue_team.append(player)
            else:
                player['summonerName'] = summoner['summonerName']
                player['rank'] = __get_solo_q_rank(summoner['summonerId'])
                # TODO champion name
                red_team.append(player)
        teams['blue'] = blue_team
        teams['red'] = red_team
        return teams

    except Exception as err:
        error_out = {
            'success': -1,
            'func': 'get_v4_summ in game_info',
            'error': err
        }
        return error_out


# --- Private functions ----

# spectate for an active game
def __v4_active_games(summoner_name):
    try:
        summoner_id = requests.get(
            'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summoner_name + '?api_key=' + __TOKEN).json()[
            'id']
        data = requests.get(
            'https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/' + summoner_id + '?api_key=' + __TOKEN)
        output = {
            'success': 1,
            'status_code': data.status_code,
            'data': data.json()
        }
        return output

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


# get solo rank list from api for one summoner
def __get_solo_q_rank(summoner_id):
    try:
        solo_rank_list = requests.get(
            'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_id + '?api_key=' + __TOKEN)

        output = {
            'success': 1,
            'status_code': solo_rank_list.json()['status_code'],
            'data': solo_rank_list.json()['data']
        }
        return output

    except Exception as err:
        error_out = {
            'success': -1,
            'func': 'getsoloqrank',
            'error': err
        }
        return error_out
