echo off
rem Test #2 Gonzaga vs. Villanova at a neutral venue
rem
rem Data scraped From here
rem  https://gamepredict.us/kenpom?team_a=Gonzaga&team_b=Villanova&neutral=true
rem
.\scrape_match.py --first="Gonzaga" --second="Villanova" --neutral --verbose
