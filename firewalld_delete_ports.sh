[root@redhat1 git]# cat delete_ports.sh 
#Script to nuke all the ports in firewalld

#First get a list of zones
for ZONE in $(firewall-cmd --get-zones); do

        echo "*********************"
        echo "***rules for $ZONE***"
        echo "*********************"
        firewall-cmd --list-ports --zone=$ZONE
        echo "*********************"
        PORTTEST=$(firewall-cmd --list-ports --zone=$ZONE | wc -c)

        if [  "$PORTTEST" -ge 2 ]; then
                read -p "Do you want to delete these ports? (y/n)?" DECISION
                case ${DECISION:0:1} in 
                        y|Y)
                                for PORT in $(firewall-cmd --list-ports --zone=$ZONE); do
                                        firewall-cmd --remove-port="$PORT" --zone=$ZONE
                                done
                        ;;
                        *)
                                echo "No ports deleted - continuing..."
                        ;;
                esac
        else
                echo "No ports - skipping"
        fi
done
echo
echo "All done - have a nice day :)"
echo
