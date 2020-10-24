import unittest
import requests
import os
def test_test():
    api_key = aKey = os.environ.get('api_key')
    response_1 = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/y%20chai?api_key="+api_key)
    response_2 = requests.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/-sy3NdvacyFk4H6REDSyjz5yn-R9uiefGEEio1eAue98Hpxvz3VbVaZz?api_key="+api_key)
    response_3 = requests.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/5gb6ElhJ1gq5T_wZvbquIuedIaVeK190hOpR_PfNbp6Z7KOo?api_key="+api_key)
    assert response_1.status_code == response_2.status_code == response_3.status_code == 200
