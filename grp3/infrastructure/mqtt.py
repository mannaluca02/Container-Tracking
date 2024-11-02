import json
from threading import Event

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt

# Event to stop the loop
stop_event = Event()
current_temperature = None
current_humidity = None
temperatures = []
humidities = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("migros/grp3/message")  # Setze hier das passende Topic

def on_message(client, userdata, msg):
    global current_temperature, current_humidity
    payload = json.loads(msg.payload)
    current_temperature = payload.get('temp')  # 'temp' ist das Feld, das die Temperatur enthält
    current_humidity = payload.get('hum')  # 'hum' ist das Feld, das die Luftfeuchtigkeit enthält
    if current_temperature is not None:
        try:
            temperatures.append(float(current_temperature))  # Konvertiere zu float
        except ValueError:
            print(f"Ungültiger Temperaturwert: {current_temperature}")
    if current_humidity is not None:
        try:
            humidities.append(float(current_humidity))  # Konvertiere zu float
        except ValueError:
            print(f"Ungültiger Luftfeuchtigkeitswert: {current_humidity}")

def mqtt_func():
    global current_temperature, current_humidity
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.loop_start()

    fig, (ax1, ax2) = plt.subplots(2, 1)
    line1, = ax1.plot([], [], lw=2, label='Temperatur (°C)')
    line2, = ax2.plot([], [], lw=2, label='Luftfeuchtigkeit (%)')
    ax1.set_ylim(15, 35)  # Setzen Sie den y-Achsenbereich entsprechend Ihrer Temperaturwerte
    ax2.set_ylim(50, 90)  # Setzen Sie den y-Achsenbereich entsprechend Ihrer Luftfeuchtigkeitswerte
    ax1.set_xlim(0, 100)  # Setzen Sie den x-Achsenbereich entsprechend der Anzahl der Datenpunkte
    ax2.set_xlim(0, 100)  # Setzen Sie den x-Achsenbereich entsprechend der Anzahl der Datenpunkte
    ax1.set_xlabel('Zeit')
    ax1.set_ylabel('Temperatur (°C)')
    ax1.set_title('Echtzeit-Temperaturüberwachung')
    ax2.set_xlabel('Zeit')
    ax2.set_ylabel('Luftfeuchtigkeit (%)')
    ax2.set_title('Echtzeit-Luftfeuchtigkeitsüberwachung')

    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        return line1, line2

    def update(frame):
        xdata = list(range(len(temperatures)))
        ydata1 = temperatures
        ydata2 = humidities
        line1.set_data(xdata, ydata1)
        line2.set_data(xdata, ydata2)
        ax1.set_xlim(0, max(100, len(temperatures)))  # Dynamische Anpassung der x-Achse
        ax2.set_xlim(0, max(100, len(humidities)))  # Dynamische Anpassung der x-Achse
        return line1, line2

    ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=1000)

    # Event-Handler für das Schließen des Fensters hinzufügen
    def on_close(event):
        stop_event.set()
        plt.close(fig)

    fig.canvas.mpl_connect('close_event', on_close)

    plt.show()

    try:
        while not stop_event.is_set():
            pass
    finally:
        client.loop_stop()
        client.disconnect()





# Trying to display color on the plot if temp > 24 and hum < 70
"""
import json
from threading import Event
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Event to stop the loop
stop_event = Event()
current_temperature = None
current_humidity = None
temperatures = []
humidities = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("migros/grp3/message")  # Setze hier das passende Topic

def on_message(client, userdata, msg):
    global current_temperature, current_humidity
    payload = json.loads(msg.payload)
    current_temperature = payload.get('temp')  # 'temp' ist das Feld, das die Temperatur enthält
    current_humidity = payload.get('hum')  # 'hum' ist das Feld, das die Luftfeuchtigkeit enthält
    if current_temperature is not None:
        try:
            temperatures.append(float(current_temperature))  # Konvertiere zu float
        except ValueError:
            print(f"Ungültiger Temperaturwert: {current_temperature}")
    if current_humidity is not None:
        try:
            humidities.append(float(current_humidity))  # Konvertiere zu float
        except ValueError:
            print(f"Ungültiger Luftfeuchtigkeitswert: {current_humidity}")

def mqtt_func():
    global current_temperature, current_humidity
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.loop_start()

    fig, (ax1, ax2) = plt.subplots(2, 1)
    line1_blue, = ax1.plot([], [], lw=2, color='blue', label='Temperatur (°C)')
    line1_red, = ax1.plot([], [], lw=2, color='red')
    line2_blue, = ax2.plot([], [], lw=2, color='blue', label='Luftfeuchtigkeit (%)')
    line2_red, = ax2.plot([], [], lw=2, color='red')
    ax1.set_ylim(15, 35)  # Setzen Sie den y-Achsenbereich entsprechend Ihrer Temperaturwerte
    ax2.set_ylim(50, 90)  # Setzen Sie den y-Achsenbereich entsprechend Ihrer Luftfeuchtigkeitswerte
    ax1.set_xlim(0, 100)  # Setzen Sie den x-Achsenbereich entsprechend der Anzahl der Datenpunkte
    ax2.set_xlim(0, 100)  # Setzen Sie den x-Achsenbereich entsprechend der Anzahl der Datenpunkte
    ax1.set_xlabel('Zeit')
    ax1.set_ylabel('Temperatur (°C)')
    ax1.set_title('Echtzeit-Temperaturüberwachung')
    ax2.set_xlabel('Zeit')
    ax2.set_ylabel('Luftfeuchtigkeit (%)')
    ax2.set_title('Echtzeit-Luftfeuchtigkeitsüberwachung')

    def init():
        line1_blue.set_data([], [])
        line1_red.set_data([], [])
        line2_blue.set_data([], [])
        line2_red.set_data([], [])
        return line1_blue, line1_red, line2_blue, line2_red

    def update(frame):
        xdata = list(range(len(temperatures)))
        ydata1_blue = [temp if temp <= 24 else None for temp in temperatures]
        ydata1_red = [temp if temp > 24 else None for temp in temperatures]
        ydata2_blue = [hum if hum >= 70 else None for hum in humidities]
        ydata2_red = [hum if hum < 70 else None for hum in humidities]

        line1_blue.set_data(xdata, ydata1_blue)
        line1_red.set_data(xdata, ydata1_red)
        line2_blue.set_data(xdata, ydata2_blue)
        line2_red.set_data(xdata, ydata2_red)
        ax1.set_xlim(0, max(100, len(temperatures)))  # Dynamische Anpassung der x-Achse
        ax2.set_xlim(0, max(100, len(humidities)))  # Dynamische Anpassung der x-Achse
        return line1_blue, line1_red, line2_blue, line2_red

    ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=1000)

    # Event-Handler für das Schließen des Fensters hinzufügen
    def on_close(event):
        stop_event.set()
        plt.close(fig)

    fig.canvas.mpl_connect('close_event', on_close)

    plt.show()

    try:
        while not stop_event.is_set():
            pass
    finally:
        client.loop_stop()
        client.disconnect()
"""