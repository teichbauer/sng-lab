import paho.mqtt.client as mqttclient
import time

from pahoclient1 import on_connect

broker_address = "localhost"
port = 1883
# ------------------
user = "sng"
password = "sng123"
# ------------------

connected = False
msg_received = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:  # okay
        print("client is connected")
        global connected
        connected = True
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    print("Message received: " + str(message.payload.decode("utf-8")))
    print("Topic: " + str(message.topic))


client = mqttclient.Client("MQTT")
client.username_pw_set(user, password=password)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port)
client.loop_start()

client.subscribe("mqtt/msg1")

while not msg_received:
    time.sleep(0.2)

client.loop_stop()
