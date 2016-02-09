import paho.mqtt.client
import socket
import sys

#Please ask for an application user and password for deployment
user_name = "bracken_toad_publishers"
password = "%0Mg2bYCWcn6"
server = "spacehub.somakeit.org.uk"
port = 1883


#Don't normally need to edit below here

#23-character clientid based on hostname and script name
_hostname = socket.gethostname()
_scriptname = sys.argv[0].split("/")[-1]
while (len(_hostname) + len(_scriptname) > 22):
    if (len(_hostname) > len(_scriptname)):
        _hostname = _hostname[:-1]
    else:
        _scriptname = _scriptname[:-1]
client_id = _hostname + "-" + _scriptname
