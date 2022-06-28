import requests
#import statsapi


url = "http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part='Marte%25'"
response = requests.get(url)
print(response)
data = response.json()

print(data)