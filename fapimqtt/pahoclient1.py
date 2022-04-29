# in requirements.txt:
# paho-mqtt >= 1.6.1
# --------------------------
import paho.mqtt.client as mqttclient
import time
import json

connected = False
broker_address = "localhost"
port = 1883
# ------------------
user = "sng"
password = "sng123"
# ------------------


def on_connect(client, userdata, flags, rc):
    if rc == 0:  # okay
        print("client is connected")
        global connected
        connected = True
    else:
        print("Connection failed")


msg = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
    "key4": "value4",
}
jmsg = json.dumps(msg)

client = mqttclient.Client("MQTT")
client.username_pw_set(user, password=password)

client.on_connect = on_connect
client.connect(broker_address, port=port)

client.loop_start()

while not connected:
    time.sleep(0.2)

client.publish("mqtt/msg1", jmsg)
client.loop_stop()
