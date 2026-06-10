import http.client
from wsgiref import headers
API_KEY = "ohd8GTNAC99EgFXpGRRmejyq8ji4vBPw5EOcLdwfOLM1sUhgoqKw5uDM1Rxe"
season_id = 26618
conn = http.client.HTTPSConnection("api.sportmonks.com/v3/football/fixtures")
conn.request("GET", f"/{season_id}?api_token={API_KEY}", headers=headers)

res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))