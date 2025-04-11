# Container-Tracking

Willkommen beim Container-Tracking-Projekt!
Diese Anwendung dient dazu, Transportdaten von Containern zu visualisieren und auszuwerten.

## 🔍 Funktionen

Der Tracker bietet folgende Möglichkeiten:
- 📄 Lokale CSV-Datei einlesen und Route auf einer 2D-Straßenkarte anzeigen
- 🌐 CSV-Datei über die WebApp beziehen und Route visualisieren
- ☁️ CSV-Datei über einen Webservice abrufen und Route darstellen
- 🛰️ Simulation automatisch starten, Sensordaten (Temperatur & Luftfeuchtigkeit) live über MQTT einlesen und in einem Diagramm anzeigen



## ⚙️ Voraussetzungen

Stelle sicher, dass folgende Komponenten auf deinem System installiert sind:
- Python 3.12 oder höher
    ```bash
    python --version
    # Beispielausgabe: Python 3.12.8
    ```
- pip (Python-Paketmanager)
    ```bash
    pip --version
    # Beispielausgabe: pip 24.2
    ```
## 🧑‍💻 Installation

So richtest du das Projekt lokal ein:
1.	Repository klonen
2.	Virtuelle Umgebung im Projektordner erstellen:
    ```bash
    python -m venv ./venv
    ```
3.	Virtuelle Umgebung aktivieren:
    Unter Windows:
    ```bash
    .\venv\Scripts\activate
    ```
    Unter macOS / Linux:
    ```bash
    source ./venv/bin/activate
    ```
4.	Abhängigkeiten installieren:
    ```bash
    pip install -r requirements.txt
    ```
5.	Nach Gebrauch die virtuelle Umgebung deaktivieren:
    ```bash
    deactivate
    ```
## 🚀 Nutzung

Bevor du startest, beachte bitte die Hinweise zur Kompatibilität weiter unten.

Navigiere in das Verzeichnis grp3 und führe folgendes aus, um die Hilfefunktion anzuzeigen:
```bash
python main.py -h
```
## 📜 Argumente & Optionen
```bash
usage: main.py [-h] [-p [CSV_PATH]] [-c [CONTAINER_ID]] [-r [ROUTE_ID]] {1,2,3,4}

Dieses Skript erlaubt das Auswählen eines Backends (1–4) und bietet passende Argumente je nach Auswahl.

Positionale Argumente:
  {1,2,3,4}           Backend-Auswahl:
                      1: Lokale CSV-Datei (benötigt --csv_path)
                      2: WebApp (keine weiteren Parameter nötig)
                      3: HTTP-Service (benötigt --container_id und --route_id)
                      4: MQTT-Service (keine weiteren Parameter nötig)

Optionen:
  -h, --help          Hilfe anzeigen und beenden

Backend 1 – Lokale Datei:
  -p [CSV_PATH], --csv_path [CSV_PATH]
                      Pfad zur CSV-Datei (z.B. -p ./data/demo.csv)

Backend 3 – HTTP-Service:
  -c [CONTAINER_ID], --container_id [CONTAINER_ID]
                      Container-ID (z.B. -c 'grp3')
  -r [ROUTE_ID], --route_id [ROUTE_ID]
                      Routen-ID (z.B. -r 'demo')
```
## 🖥️ Kompatibilität

Die Anwendung wurde erfolgreich auf verschiedenen Windows- und MacOS-Systemen getestet.

## 🛑 Bekanntes Problem:
Auf einem Mac mit M4-Chip kam es zu Fehlern im Zusammenhang mit urllib und ssl.
Diese Probleme sind bisher schlecht dokumentiert, und auch der Wechsel auf OpenSSL konnte keine Abhilfe schaffen. Auf Geräten mit M3-Chip läuft die Anwendung hingegen problemlos.
