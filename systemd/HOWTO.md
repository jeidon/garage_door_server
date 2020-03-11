Clone this repo:
git@github.com:CarlEdman/godaddy-ddns.git
cd godaddy-ddns

Go here:

https://developer.godaddy.com/keys/#

Create production

Run this
ExecStart=/usr/bin/python3 /home/pi/godaddy-ddns/godaddy_ddns.py --key KEY --secret SECRET  DOMAIN

Install the systemd godaddy_ddns script.

Install the systemd garage_door_status script.
