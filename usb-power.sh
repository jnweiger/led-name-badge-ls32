#!/bin/bash
###############################################################
# It will power on/off a usb device based on a string found in dmesg output.
# 
# Example for the led-badge:
#
# usb-power.sh off "Product: LS32 Custm HID"
# - This code does not work with a Lenovo-T440s running Mint. Not sure why.
###############################################################
if [[ $2 == "" ]]; then
	echo "Usage: $0 [on|off] DMESG_STRING"
	exit;
fi
USB_DEV=$(dmesg | grep -o "usb .*: $2" | tail -n 1 | awk '{print $2}' | sed 's/://')
if [[ $USB_DEV == "" ]]; then
	echo "Device not found";
	exit;
fi

echo using USB_DEV=$USB_DEV

if [[ $1 == "on" ]]; then
	echo "2000" > /sys/bus/usb/devices/$USB_DEV/power/autosuspend_delay_ms 
	echo "on" > /sys/bus/usb/devices/$USB_DEV/power/control 
elif [[ $1 == "off" ]]; then
	echo "0" > /sys/bus/usb/devices/$USB_DEV/power/autosuspend_delay_ms 
	echo "auto" > /sys/bus/usb/devices/$USB_DEV/power/control 
else
	echo "Unknown action: $1"
	exit;
fi
