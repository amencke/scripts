#Script to nuke all the rich rules in firewalld

#First get a list of zones
for ZONE in $(firewall-cmd --get-zones); do

        #Get the rules for that zone and store in a file
        touch ${ZONE}_rules
        if [ $? -ne 0 ]; then
                echo "failed creating ${ZONE}_rules file"
                exit 1
        fi
        firewall-cmd --list-rich-rules --zone=$ZONE > ${ZONE}_rules

        echo "*********************"
        echo "***rules for $ZONE***"
        echo "*********************"

        RULECOUNT=$(cat ${ZONE}_rules | wc -l)
        if [ "$RULECOUNT" -eq 0 ]; then
                echo "There are no rules in the $ZONE zone."
        else
                cat ${ZONE}_rules | while read LINE; do
                        echo "$LINE"
                done
                read -p "Do you want to delete these rules? (y/n)?" DECISION
                case ${DECISION:0:1} in 
                        y|Y)
                                cat ${ZONE}_rules | while read LINE; do
                                        firewall-cmd --remove-rich-rule="$LINE" --zone=$ZONE
                                done
                        ;;
                        *)
                                echo "No rules deleted - continuing..."
                        ;;
                esac
        fi

done
echo
echo "All done - have a nice day :)"
echo
