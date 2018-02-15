echo off
rem Test #1 Villanova (visitor) Gonzaga (home)
rem 
rem Data scraped From here
rem   https://gamepredict.us/kenpom?team_a=villanova&team_b=gonzagaa
rem
pipenv run python .\score_matchup.py --first="villanova" --second="gonzaga" --verbose
