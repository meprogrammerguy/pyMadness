echo off
rem Test #3 Villanova (visitor) Gonzaga (home)
rem 
rem Data scraped From here
rem   https://gamepredict.us/kenpom?team_a=villanova&team_b=gonzagaa
rem
pipenv run python .\scrape_matchup.py --first="villanova" --second="gonzaga" --verbose
