# This file contains Secrets relevant to your installtion.
# DO NOT SHARE THIS FILE!

#CloudFlare Token
TOKEN = "000"

#Zone
ZONE = "yourdomain.example"

#Record
RECORD = "yoursubdomain"

IFNAME = "eth0"


# You shouldn't have to change this.
ipcmd = "ip -6 addr show " + IFNAME + " | grep global"

