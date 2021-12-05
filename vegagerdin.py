# need to install
# pip install paho-mqtt requests lxml html5lib bs4
import sys
import json
import requests
import time
import paho.mqtt.client as paho
import logging
# initialize the log settings
logging.basicConfig(filename = '/usr/share/hassio/homeassistant/snjallingur_scripts/pythonscripts.log',format='%(asctime)s %(message)s', level = logging.DEBUG)
logging.info('logger for vegagerdin started')

# MQTT Broker
# IP address or host name
broker="localhost"
# create client and connect to broker
try:
    client= paho.Client("client-vegagerdin")
    client.username_pw_set(username="homeassistant",password="La0voozeihohfae8Soh0Thizeeyah8ahg5bias5kahqu3uyoo0Fie9shee9rie6i")
    client.connect(broker)
    client.loop_start()  #Start loop 
    time.sleep(4) # Wait for connection setup to complete
except Exception as e:
    print(e)
    logging.exception(str(e)) 
    logging.error('Couldn´t connect to MQTT broker ' + str(e)) 


urlfile = "http://gagnaveita.vegagerdin.is/api/faerd2017_1"

#print(requests.get(urlfile).json())
kjalarnes = {}
hellisheidi = {}
holtavorduheidi = {}
response = requests.get(urlfile).json()
for IdButur in response:
    # Deprecated: <IdButur>904210018</IdButur> -> Hvalfjarðarvegur. Botnsá - Hringvegur
    #<IdButur>904210019</IdButur> -> Hvalfjarðarvegur. Botnsá - Hringvegur -> 904210022
    #<IdButur>904210019</IdButur> -> Hvalfjarðargöng
    #<IdButur>903030019</IdButur>  -> Þingv.v-Hvalfjg.
    #<IdButur>904690018</IdButur> -> Hvalfjarðagöng
    #<IdButur>904060022</IdButur> -> Holtavörðuheiði
    # Deprecated: <IdButur>902020018</IdButur> -> Hellisheiði
    # <IdButur>902020019</IdButur> -> Hellisheiði
    # Kjalarnes
    #print(int(IdButur['IdButur']))
    #
    #Holtavörðuheiði
    #904060022
    if IdButur['FulltNafnButs'] == "Holtavörðuheiði":
        holtavorduheidi['condition'] = IdButur['AstandYfirbord']
        holtavorduheidi['condition_description'] = IdButur['AstandLysing']
        holtavorduheidi['condition_detail'] = IdButur['AstandVidbotaruppl']
        holtavorduheidi['name_short'] = IdButur['StuttNafnButs']
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
            logging.error('Couldn´t publish to MQTT broker: ' + str(broker))
    #
    # Hellisheiði
    if IdButur['FulltNafnButs'] == "Hringv. um Hellisheiði: Þorlákshafnarv. - Þrengslav.":
        hellisheidi['condition'] = IdButur['AstandYfirbord']
        hellisheidi['condition_description'] = IdButur['AstandLysing']
        hellisheidi['condition_detail'] = IdButur['AstandVidbotaruppl']
        hellisheidi['name_short'] = IdButur['StuttNafnButs']
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
            #logging.exception(str(e)) 
            logging.error('Couldn´t publish to MQTT broker: ' + str(broker))
    #
    # Kjalarnes
    if IdButur['FulltNafnButs'] == "Hvalfjarðarvegur. Botnsá - Hringvegur":
        #print(IdButur['FulltNafnButs'])
        kjalarnes['condition'] = IdButur['AstandYfirbord']
        kjalarnes['condition_description'] = IdButur['AstandLysing']
        kjalarnes['condition_detail'] = IdButur['AstandVidbotaruppl']
        kjalarnes['name_short'] = IdButur['StuttNafnButs']
        kjalarnes['updated'] = IdButur['DagsKeyrtUt']
        kjalarnes['snow_maintenance'] = IdButur['Snjomokstursregla']
        kjalarnes['name_full'] = IdButur['FulltNafnButs'] 
        if IdButur['AstandYfirbord'] in ['LOKAD','OFAERT_ANNAD','OFAERT_VEDUR']:
            kjalarnes['passable'] = "false"
        else:
            kjalarnes['passable'] = "true"              
        #publish to MQTT
        compact_obj = json.dumps(kjalarnes, separators=(',', ':'))
        #print(compact_obj)
        #client.publish("homeassistant/vegagerdin/kjalarnes",compact_obj)
        #client.publish("homeassistant/vegagerdin/kjalarnes",compact_obj)
        try:
            client.publish("homeassistant/vegagerdin/kjalarnes",compact_obj)
        except:
            logging.error('Couldn´t publish to MQTT broker: ' + str(broker))

client.loop_stop()    #Stop loop 
client.disconnect()
