import requests
import json
import pandas
import sqlalchemy as db
from matplotlib import pyplot as plt


def is_from_country(id, country):
  url = "http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id=" + str(id) +""
  response = requests.get(url)
  if response.json()['player_info']['queryResults']['row']['birth_country'].lower() == country.lower():
    return True
  return False


def get_teams(year):
  team_ids = []
  fake_teams = [
    '', 'no team', 'office of the commissioner', 'to be determined', 'national league all-stars',
     'national league champion', 'american league champion', 'american league all-stars', 
    ]
  url = "http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&season=" + str(year) + "&team_all_season.col_in=mlb_org_id&team_all_season.col_in=name_display_full"
  response = requests.get(url)
  data = response.json()['team_all_season']['queryResults']['row']
  for i in data:
    if i['name_display_full'].lower() not in fake_teams:
      team_ids.append(i['mlb_org_id'])
  return team_ids


def get_players(country, year):
  teams = get_teams(year)
  players = []
  for i in teams:
    roster_url = "http://lookup-service-prod.mlb.com/json/named.roster_team_alltime.bam?start_season=" + str(year) + "&end_season=" + str(year) + "&team_id=" + str(i) + ""
    response = requests.get(roster_url)
    try:
      data = response.json()['roster_team_alltime']['queryResults']['row']
    except:
      continue
    for j in data:
      try:
        if is_from_country(j['player_id'], country):
          players.append(j['name_first_last'])
      except:
        continue
  return players


def sql_database(data, country):
  pandas.DataFrame.from_dict(data, orient='index')
  engine = db.create_engine('sqlite:///' + country + ''.db')
  dataframe_name.to_sql(country, con=engine, if_exists='replace', index=False)
  query_result = engine.execute("SELECT * FROM " + country + ";").fetchall()
  print(pd.DataFrame(query_result))


def main():
  print("This program will create a graph of the number of mlb players from a certain country over time")
  start_year = int(input("Please enter the starting year: "))
  end_year = int(input("Please enter the ending year: "))
  country = input("Please enter a country: ")
  print("Creating graph, this may take a while.  Press ctrl + C to quit")

  num_of_players = []
  data = {}
  for i in range(start_year, end_year):
    print("Processing " + str(i))
    try:
      data[str('i')] = get_players(country, i)
      num_of_players.append(len(data))
    except:
      continue

  with open(str(country + str(start_year) + "_" + str(end_year) + ".json"), "w") as json_file:
    json.dump(data, json_file)
   
  plt.plot(list(range(start_year, end_year)), num_of_players)
  
  plt.xlabel("Year")
  plt.ylabel("Players from " + country.capitalize())
  plt.title("MLB players from " + country.capitalize())

  plt.savefig(country.capitalize() + str(start_year) + "_" + str(end_year)  + ".png")


if __name__ == '__main__':
  main()