from fastapi import FastAPI
import uvicorn

import pydantic
import pymongo

import pdb

import paho.mqtt.client as mqttclient

broker_address = "localhost"
mqtt_port = 1883
# ------------------
user = "sng"
password = "sng123"
# ------------------
connected = False


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

client.connect(broker_address, port=mqtt_port)
client.subscribe("mqtt/msg1")
# ----------------------------------------------------------

app = FastAPI()
fapi_port = 5001


@app.get("/")
async def index():
    return {'hello': "World!"}


@app.get("/testget/{param}")
async def get_id(param):
    return {"result": param}


@app.post("/mdb/{jbj}")
async def receive_data(jbj):
    pass

if __name__ == '__main__':

    client.loop_start()

    print(f"FastAPI server running on prt {fapi_port}")
    uvicorn.run(app, host='0.0.0.0', port=fapi_port)

    client.loop_stop()
