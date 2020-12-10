# vegagerdin
Home Assistant MQTT sensor(s) for road condition in Iceland
based on:
http://gagnaveita.vegagerdin.is/api/faerd2017_1

more information about the returned response can be found here:
http://www.vegagerdin.is/vefur2.nsf/Files/gagnaveita_faerd_2017/$file/gagnaveita_faerd_2017.pdf

If you want to include the sensors in a picture entity card you could use still images from one of their webcams listed here:
http://www4.vegagerdin.is/xml/myndavelar.xml

The sensors are created from a python script ("vegagerdin.py"). The script pulls the information from the xml file and "watches" to certain road sections ('IdButur'). The trickiest part is to find the right road setion ID. The Python script gathers the information from a road setion and publishes the results to an MQTT broker. The script is defined as a shell command ("shell_commands.yaml") and the shell script is run from an automation every 10 minutes (or more frequently if you like).

There is also a binary_sensor ("binary_sensors.yaml") from the MQTT sensor(s) created ("sensors.yaml").


![GitHub Logo](/lovelace_hellisheidi.jpg)
Format: ![Alt Text](url)
