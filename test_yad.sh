#!/bin/bash

IFS=$(echo -en "\n\b")
yad --completion --entry="" $(cat ~/.tmp/teams.txt) | while IFS= read -r cmd;
    do
        echo "$cmd" >> ~/.tmp/teams.txt
        echo ${cmd}
    done
