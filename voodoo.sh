#!/bin/sh
#
# http://www.sarfata.org/posts/setting-up-an-amazon-vpn-server.html
#
# Copyright Thomas Sarlandie 2012
#
# This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 
# Unported License: http://creativecommons.org/licenses/by-sa/3.0/
#
# Attribution required: please include my name in any published derivative and
# let me know how you have improved it! 

COMMAND="$1"
shift

case $COMMAND in
hostile)
  echo "Going into hostile mode. You will be protected."
  # Load pf rules from custom file - Skip Apple default stuff
  pfctl -f voodoo-pf.conf
  # Enable packet filtering
  pfctl -e
  ;;
safe)
  echo "Going back to Apple default mode"
  pfctl -f /etc/pf.conf
  pfctl -d
  # note: it would be better to use pfctl -X <token> but getting the token 
  # requires parsing the output of 'pfctl -s References'
  ;;
log)
  ifconfig pflog0 create
  tcpdump -v -n -e -ttt -i pflog0
  ;;
*)
  echo "$0: <hostile|safe|log>"
  echo " Use hostile when you are on an unsecured network."
  echo " Use safe when you are back on a safe network. This will reset everything back to Apple's default"
  ;;
esac
