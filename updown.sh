#I like to add the line alias updown=/root/updown.sh to /etc/bashrc
#I use this really frequently on my VMs as yum has a bug where it will
#not work correctly for on reason or another when I masqurade all my private VMs 
#on one VM with a public interface. For this reason I usually create public if "eno9"

#!/bin/bash

if [ $# -ne 1 ]; then
        echo "Usage: $(basename $0) [ pub | priv ]"
        exit 1
elif [ "$1" != "priv" ] && [ "$1" != "pub" ]; then
        echo "Usage: $(basename $0) [ pub | priv ]"
        exit 1
fi 

for i in $(nmcli con show | cut -d ' ' -f 1 | grep -v '^NAME$'); do

        if [ $1 == priv ]; then
                case $i in
                        eno1)
                                nmcli con up $i
                                ;;
                        *)
                                nmcli con down $i
                                ;;
                esac

        elif [ $1 == pub ]; then
                case $i in 
                        eno9)
                                nmcli con up $i
                                ;;
                        *)
                                nmcli con down $i
                                ;;
                esac

        fi

done
