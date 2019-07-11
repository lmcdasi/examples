#!/bin/sh -f

# Cleans Jenkins Workspace - Requires sudo without passwd
# Add it to crontab to run every hour
#DO NOT REMOVE SCRIPT - used by crontab

JENKINS_URL="http://<REPLACE_WITH_JENKINS_URL>"
ONE_DAY_IN_SECONDS=3600 
UTILITY_USER="TO_BE_FILLED"
UTILITY_PW="TO_BE_FILLED"

dateNow=$(date +%s)

for d in $(find /home/jenkins/workspace*/ -maxdepth 1 -type d -path '*/*ws-cleanup*'); do 
    dTime=$(stat -c %Y $d) 
    elapsed=$((dateNow - dTime)) 

    if [ ${elapsed} -ge ${ONE_DAY_IN_SECONDS} ]; then 
       logger -t "JENKINS_CLEAN_DISK_LEAK" "Deleting ws_cleanup leak ${d}"
       sudo rm -rf ${d} 

       curl -s http://${JENKINS_URL}/administrativeMonitor/AsyncResourceDisposer/ -u${UTILITY_USER}:${UTILITY_PW} | tr '"' '\n' | grep 'stop-tracking' | cut -d '-' -f 3 | sort -n | while read ASYNC_THREAD; do curl http://${JENKINS_URL}/administrativeMonitor/AsyncResourceDisposer/stopTracking -u${UTILITY_USER}:${UTILITY_PW} -X POST --data "id=${ASYNC_THREAD}"; done
 
       if [ $? -ne 0 ]; then 
          logger -t "JENKINS_CLEAN_DISK_LEAK" "Unable to clean Jenkins WS. Manual check required." 
	  # Disable it in crontab
       fi 
    fi 
done 
