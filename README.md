# General Instructions
>Run python or python3 on GetData.py.  
>You will be prompted for a range of years and a country.  
>A .png file will be created of a graph of the MLB players from that country over your span of years.  
>The file will be in the same directory.
>A .json file will also be made with that maps each year to a list of player ids for the MLB API
>This data will also be stored in a mysql database

>For each year, the script requests every team in the MLB that year.
>It then cycles through each player on those teams rosters and checks if they are from the requested country.
>If this is true, their unique player ID is added to a list, which is then exported to the json file.
>Matplot lib simply plots the length of the ID list against the range of input years.

# Libraries used
>**requests**
>**json**
>**sqlalchemy**
>**matplotlib**
>**pandas**
Make sure all these libraries are intalled using pip
# Licensing
> No licensing yet