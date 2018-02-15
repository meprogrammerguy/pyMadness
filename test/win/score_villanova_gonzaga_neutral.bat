echo off
rem Test #2  Villanova vs. Gonzaga at a neutral venue
rem
rem Data scraped From here
rem  https://gamepredict.us/kenpom?team_a=villanova&team_b=gonzaga&neutral=true
rem
pipenv run python .\score_matchup.py --first="villanova" --second="gonzaga" --neutral --verbose
