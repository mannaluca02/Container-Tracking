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


def on_connect(client, userdata, flags, rc, properties):
    """
    Callback function for when the client receives a CONNACK response from the server.

    Parameters:
    client (paho.mqtt.client.Client): The client instance for this callback.
    userdata (any): The private user data as set in Client() or userdata_set().
    flags (dict): Response flags sent by the broker.
    rc (int): The connection result.
    properties (paho.mqtt.properties.Properties): The properties associated with the connection.

    Returns:
    None
    """
    print("Connected with result code " + str(rc))
    client.subscribe("migros/grp3/message")  # Setze hier das passende Topic


def on_message(client, userdata, msg):
    """
    Callback function that is triggered when a message is received on a subscribed topic.

    This function processes the incoming MQTT message, extracts temperature and humidity
    data from the payload, and appends the values to the respective lists if they are valid.

    Args:
        client (paho.mqtt.client.Client): The MQTT client instance.
        userdata (any): User-defined data of any type that is passed to the callback.
        msg (paho.mqtt.client.MQTTMessage): The MQTT message instance containing topic and payload.

    Raises:
        ValueError: If the temperature or humidity values cannot be converted to float.

    Notes:
        - The payload is expected to be a JSON object with 'temp' and 'hum' fields.
        - Invalid temperature or humidity values will be reported via print statements.
    """
    global current_temperature, current_humidity
    payload = json.loads(msg.payload)
    current_temperature = payload.get(
        "temp"
    )  # 'temp' ist das Feld, das die Temperatur enthält
    current_humidity = payload.get(
        "hum"
    )  # 'hum' ist das Feld, das die Luftfeuchtigkeit enthält
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
    """
    Initializes and runs an MQTT client that connects to a specified broker using websockets,
    subscribes to messages, and updates real-time plots for temperature and humidity data.
    The function performs the following tasks:
    - Creates an MQTT client with a specified callback API version and transport method.
    - Sets up the on_connect and on_message callback functions.
    - Connects to the MQTT broker at the specified address and port.
    - Starts the MQTT client loop.
    - Initializes a matplotlib figure with two subplots for temperature and humidity.
    - Defines the initialization and update functions for the animation.
    - Creates a real-time animation for the temperature and humidity plots.
    - Adds an event handler to stop the MQTT client loop and close the plot when the window is closed.
    - Runs an infinite loop to keep the script running until a stop event is set.
    Note:
    - The function assumes the existence of global variables: `current_temperature`, `current_humidity`,
      `temperatures`, `humidities`, and `stop_event`.
    - The x-axis and y-axis limits for the plots are set based on assumed ranges for temperature and humidity values.
    - The function uses the `matplotlib.animation.FuncAnimation` class to update the plots in real-time.
    Raises:
    - Any exceptions raised by the MQTT client or matplotlib functions are not explicitly handled within this function.
    """
    global current_temperature, current_humidity
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2, transport="websockets"
    )
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("fl-17-240.zhdk.cloud.switch.ch", 9001, 60)
    client.loop_start()

    fig, (ax1, ax2) = plt.subplots(2, 1)
    (line1,) = ax1.plot([], [], lw=2, label="Temperatur (°C)")
    (line2,) = ax2.plot([], [], lw=2, label="Luftfeuchtigkeit (%)")
    ax1.set_ylim(
        15, 35
    )  # Setzen Sie den y-Achsenbereich entsprechend Ihrer Temperaturwerte
    ax2.set_ylim(
        50, 90
    )  # Setzen Sie den y-Achsenbereich entsprechend Ihrer Luftfeuchtigkeitswerte
    ax1.set_xlim(
        0, 100
    )  # Setzen Sie den x-Achsenbereich entsprechend der Anzahl der Datenpunkte
    ax2.set_xlim(
        0, 100
    )  # Setzen Sie den x-Achsenbereich entsprechend der Anzahl der Datenpunkte
    ax1.set_xlabel("Zeit")
    ax1.set_ylabel("Temperatur (°C)")
    ax1.set_title("Echtzeit-Temperaturüberwachung")
    ax2.set_xlabel("Zeit")
    ax2.set_ylabel("Luftfeuchtigkeit (%)")
    ax2.set_title("Echtzeit-Luftfeuchtigkeitsüberwachung")

    def init():
        """
        Initializes the data for line1 and line2.

        This function sets the data for line1 and line2 to empty lists and returns
        the updated line1 and line2 objects.

        Returns:
            tuple: A tuple containing the updated line1 and line2 objects.
        """
        line1.set_data([], [])
        line2.set_data([], [])
        return line1, line2

    def update(frame):
        """
        Update the data for the plot animation.

        Parameters:
        frame (int): The current frame number of the animation.

        Returns:
        tuple: A tuple containing the updated line objects (line1, line2).

        This function updates the x and y data for two lines (temperatures and humidities)
        and adjusts the x-axis limits dynamically based on the length of the data.
        """
        xdata = list(range(len(temperatures)))
        ydata1 = temperatures
        ydata2 = humidities
        line1.set_data(xdata, ydata1)
        line2.set_data(xdata, ydata2)
        ax1.set_xlim(0, max(100, len(temperatures)))  # Dynamische Anpassung der x-Achse
        ax2.set_xlim(0, max(100, len(humidities)))  # Dynamische Anpassung der x-Achse
        return line1, line2

    # Erstellen einer Animation für das Diagramm
    # fig: Die Figur, die animiert werden soll
    # update: Die Funktion, die bei jedem Frame der Animation aufgerufen wird, um die Daten zu aktualisieren
    # init_func: Die Initialisierungsfunktion, die einmal zu Beginn der Animation aufgerufen wird
    # blit=True: Optimiert die Animation, indem nur die Teile des Plots neu gezeichnet werden, die sich ändern
    # interval=1000: Das Intervall in Millisekunden zwischen den Frames der Animation (hier 1 Sekunde)
    ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=1000)

    def on_close(event):
        stop_event.set()
        plt.close(fig)

    fig.canvas.mpl_connect("close_event", on_close)

    plt.show()

    try:
        while not stop_event.is_set():
            pass
    finally:
        client.loop_stop()
        client.disconnect()


# This code displays the temp in blue and red based on the value. But it does not show the line plot as one merged plot
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
