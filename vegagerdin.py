# need to install
# pip install paho-mqtt requests lxml html5lib bs4
import sys
import json
import requests
import time
import paho.mqtt.client as paho

# MQTT Broker
# IP address or host name
broker="yourMQTTbroker"
# create client and connect to broker
try:
    client= paho.Client("client-001")
    client.connect(broker)
except:
    print("An unexpected error occured")
    #print("Unexpected error:", sys.exc_info()[0])
    #raise

urlfile = "http://gagnaveita.vegagerdin.is/api/faerd2017_1"

#print(requests.get(urlfile).json())
kjalarnes = {}
hellisheidi = {}
holtavorduheidi = {}
response = requests.get(urlfile).json()
for IdButur in response:
    # Deprecated: <IdButur>904210018</IdButur> -> Hvalfjarðarvegur. Botnsá - Hringvegur
    #<IdButur>904210019</IdButur> -> Hvalfjarðarvegur. Botnsá - Hringvegur
    #<IdButur>904210019</IdButur> -> Hvalfjarðargöng
    #<IdButur>903030019</IdButur>  -> Þingv.v-Hvalfjg.
    #<IdButur>904690018</IdButur> -> Hvalfjarðagöng
    #<IdButur>904060022</IdButur> -> Holtavörðuheiði
    # Deprecated: <IdButur>902020018</IdButur> -> Hellisheiði
    # Deprecated: <IdButur>902020019</IdButur> -> Hellisheiði
    #<IdButur>902020022</IdButur> -> Hellisheiði
    # Kjalarnes
    #print(int(IdButur['IdButur']))
    if int(IdButur['IdButur']) == 904210019:
        print(IdButur['FulltNafnButs'])
        kjalarnes['condition'] = IdButur['AstandYfirbord']
        kjalarnes['condition_description'] = IdButur['AstandLysing']
        kjalarnes['condition_detail'] = IdButur['AstandVidbotaruppl']
        kjalarnes['name'] = IdButur['StuttNafnButs']
        kjalarnes['updated'] = IdButur['DagsKeyrtUt']
        kjalarnes['snow_maintenance'] = IdButur['Snjomokstursregla']
        kjalarnes['name_full'] = IdButur['FulltNafnButs'] 
        if IdButur['AstandYfirbord'] in ['LOKAD','OFAERT_ANNAD','OFAERT_VEDUR']:
            kjalarnes['passable'] = "false"
        else:
            kjalarnes['passable'] = "true"              
        #publish to MQTT
        compact_obj = json.dumps(kjalarnes, separators=(',', ':'))
        client.publish("homeassistant/vegagerdin/kjalarnes",compact_obj)
    #
    #Holtavörðuheiði
    #904060022
    if int(IdButur['IdButur']) == 904060022:
        holtavorduheidi['condition'] = IdButur['AstandYfirbord']
        holtavorduheidi['condition_description'] = IdButur['AstandLysing']
        holtavorduheidi['condition_detail'] = IdButur['AstandVidbotaruppl']
        holtavorduheidi['name'] = IdButur['StuttNafnButs']
        holtavorduheidi['updated'] = IdButur['DagsKeyrtUt']
        holtavorduheidi['snow_maintenance'] = IdButur['Snjomokstursregla']
        holtavorduheidi['name_full'] = IdButur['FulltNafnButs'] 
        if IdButur['AstandYfirbord'] in ['LOKAD','OFAERT_ANNAD','OFAERT_VEDUR']:
            holtavorduheidi['passable'] = "false"
        else:
            holtavorduheidi['passable'] = "true"           
        #publish to MQTT
        compact_obj = json.dumps(holtavorduheidi, separators=(',', ':'))
        try:
            client.publish("homeassistant/vegagerdin/holtavorduheidi",compact_obj)
        except:
            print("An unexpected error occured")  
    #
    # Hellisheiði
    if int(IdButur['IdButur']) == 902020019:
        hellisheidi['condition'] = IdButur['AstandYfirbord']
        hellisheidi['condition_description'] = IdButur['AstandLysing']
        hellisheidi['condition_detail'] = IdButur['AstandVidbotaruppl']
        hellisheidi['name'] = IdButur['StuttNafnButs']
        hellisheidi['updated'] = IdButur['DagsKeyrtUt']
        hellisheidi['snow_maintenance'] = IdButur['Snjomokstursregla']
        hellisheidi['name_full'] = IdButur['FulltNafnButs'] 
        if IdButur['AstandYfirbord'] in ['LOKAD','OFAERT_ANNAD','OFAERT_VEDUR']:
            hellisheidi['passable'] = "false"
        else:
            hellisheidi['passable'] = "true"    
            
        #publish to MQTT
        compact_obj = json.dumps(hellisheidi, separators=(',', ':'))
        try:
            client.publish("homeassistant/vegagerdin/hellisheidi",compact_obj)
        except:
            print("An unexpected error occured")
