from django.shortcuts import render
from ncclient import manager
from xml.etree import ElementTree as ET

ip_address = '10.21.2.53'


def buttonTalkWithServer (request):
    return render(request, 'home.html')

def get_data(request): 
    with manager.connect(host=ip_address, port=830, username='pi',password='rtrksifra', hostkey_verify=False) as m:
        data = m.get(filter = ("subtree", "<room-data></room-data>")).data_xml
        root = ET.fromstring(data)
        if (root[0][0].text == "false"):
            light_status = "Light Status: OFF"
        else:
            light_status = "Light Status: ON"
        
        temperature = "Temperature: " + root[0][1].text

        if (root[0][2].text == "false"):
            door_status = "Door Status: CLOSED"
        else:
            door_status = "Door Status: OPEN"
    return render(request, 'home.html', {'temperature':temperature, 'door_status': door_status, 'light_status': light_status})

def turn_off_ac(request): 
    with manager.connect(host=ip_address, port=830, username='pi',password='rtrksifra', hostkey_verify=False) as m:
        turn_off_config = """<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><room-data xmlns="urn:sysrepo:room1"><ac-status>false</ac-status></room-data></config>"""
        m.edit_config(target = 'running', config = turn_off_config)
    return render(request, 'home.html')

def turn_on_ac(request): 
    with manager.connect(host=ip_address, port=830, username='pi',password='rtrksifra', hostkey_verify=False) as m:
        turn_off_config = """<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><room-data xmlns="urn:sysrepo:room1"><ac-status>true</ac-status></room-data></config>"""
        m.edit_config(target = 'running', config = turn_off_config)
            
    return render(request, 'home.html')