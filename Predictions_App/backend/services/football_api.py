import requests
resp = requests.get('https://worldcup26.ir/get/games', timeout=10)
data = resp.json()
for game in data['games'][:3]:
    print(game.get('id'), game.get('date'), game.get('dateTime'), game.get('time'))