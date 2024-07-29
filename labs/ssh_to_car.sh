#!/bin/bash
echo "Which RACECAR Team are you trying on?"

read team_number


end=$(( 100 + $team_number ))

ssh racecar@192.168.1.$end
