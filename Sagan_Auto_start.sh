#!/bin/sh
if [  ! -f "/var/run/sagan/" ]; then
        mkdir /var/run/sagan
        chmod +777 /var/run/sagan
	continue;
fi
if ! pgrep -x "SaganMain"
then
    /usr/local/bin/sagan -D
fi
