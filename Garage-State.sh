#!/bin/bash
#The purpose of this script is to check the state of the garagae door sensor
ZenIP="192.168.99.99"
HAIP="127.0.0.1"
HAPwd="PASSWORD"
state=$(ssh root@$ZenIP 'cat /sys/class/gpio/gpio117/value' 2>&1)
#echo $state
Update () {
	ha_server=$1
	ha_api_password=$2
	ha_state=$3
	cmd_curl="curl -X POST -d '{\"state\":\"$ha_state\"}' $ha_server/api/states/switch.garage_door -H \"x-ha-access: $ha_api_password\" --insecure"
	cmd_curl_output=`eval $cmd_curl`
	echo $cmd_curl_output
}
if [[ $state == 1 ]]; then
	SENSOR="closed"
	#echo "off"
	#Update https://$HAIP $HAPwd off
else
	SENSOR="open"
	#echo "on"
	#Update https://$HAIP $HAPwd on
fi
echo $SENSOR
