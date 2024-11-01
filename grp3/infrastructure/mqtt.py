import paho.mqtt.client as mqtt
import json
from threading import Event

# Event to stop the loop
stop_event = Event()
current_temperature = None

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("migros/grp3/message")  # Setze hier das passende Topic

def on_message(client, userdata, msg):
    global current_temperature
    payload = json.loads(msg.payload)
    current_temperature = payload.get('temp')  # 'temp' ist das Feld, das die Temperatur enthält

def mqtt_func():
    global current_temperature
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.loop_start()

    try:
        while not stop_event.is_set():
            if current_temperature is not None:
                print(f"Aktuelle Temperatur: {current_temperature}")
    finally:
        client.loop_stop()
        client.disconnect()