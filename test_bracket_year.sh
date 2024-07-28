#!/bin/bash
#
# script to scrape ncaa march madness bracket page
#   if page is there the scraper will use test data instead of "live"
# 
green='\033[0;32m'
red='\033[0;31m'
NC='\033[0m'
the_count=( "$#" )
the_args=( "$@" )
if [ $the_count -gt 1 ]
then
    echo -e "      ${red}test_bracket_year.sh${NC}"
    echo " "
    echo -e "${red}no arguments: current year, one argument: year in yyyy${NC}"
    echo " "
    echo -e "${red}... exiting${NC}"
    exit 1
fi
cur_year=true
if [ $the_count -eq 0 ]
then
    year=$(date +%Y)
fi
if [ $the_count -eq 1 ]
then
	cur_year=false
    year=$the_args
fi

cd $HOME
test_location="$HOME/git/pyMadness/test"
bracket="$test_location/bracket/$year"
cd $test_location
mkdir -p $bracket
cd $bracket
#
# ncaa madness tournament bracket page
#
echo -e "           ${green}ncaa march madness tournament bracket scrape${NC}"
	curl -L "http://www.ncaa.com/march-madness-live/bracket" -o "bracket.html"

echo " "
echo -e "${green}done.${NC}"
