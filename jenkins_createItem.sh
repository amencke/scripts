#!/bin/bash

CRUMB=$(curl -u jenkins:jenkins 'http://'"$JENKINS_HOME"'/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)' | cut -d: -f2)

curl -X POST \
        -H "Content-Type:application/xml" \
        -d @config.xml \
        -u $USER:$PASS\
        "http://$JENKINS_HOME/createItem?name=someJenkinsJob&.crumb=$CRUMB"
        
if [ "$?" -eq 0 ]; then
        echo "Job created successfully"
else
        echo "Something went wrong"
fi
echo
        
