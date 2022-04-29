from fastapi import FastAPI
import uvicorn
import paho.mqtt.client as mqtt
import pdb

app = FastAPI()

# ------------- mqtt stuff ----------------------------------------------------

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


@app.get("/test-mqtt")
async def func():
    # pdb.set_trace()
    # fast_mqtt.publish("/mqtt", "Hello from Fastapi")  # publishing mqtt topic
    return {"result": True, "message": "Published"}

# ------------- FastAPI stuff


@app.get("/")
async def index():
    return {'hello': "World!"}


@app.get("/test/{param}")
async def get_id(param):
    return {"result": param}

_port = 6001
if __name__ == '__main__':
    print(f"FastAPI is running on port: {_port}")
    # pdb.set_trace()
    uvicorn.run(app, host='0.0.0.0', port=_port)
