import paho.mqtt.client as mqtt
import time
import requests
import json
import socket


def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
        client.subscribe("test/esp32/hilox")
    else:
        print("could not connect, return code:", return_code)


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    # print("Received message:", payload)

    # Extraer los valores del mensaje JSON
    try:
        data = json.loads(payload)
        esp32 = data['esp32']
        mensaje = data['mensaje']
        fecha = data['fecha']
        hora = data['hora']
        latitude = data['latitude']
        longitude = data['longitude']

        # ... y así sucesivamente con las claves que necesites
        print("mensaje:", mensaje)
        print("fecha:", fecha)
        # Puedes realizar otras operaciones con los valores extraídos
        url = 'https://apirest-production-709d.up.railway.app/reportes/post/'
        reporte = {
            'esp32': esp32,
            'mensaje': mensaje,
            'fecha': fecha,
            'hora': hora,
            'latitude': latitude,
            'longitude': longitude
            }

        x = requests.post(url, json = reporte)
        # print("reporte en json: "+reporte)
        print(x.text)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

broker_hostname = "test.mosquitto.org"
local_broker_hostname = "172.17.0.3"
port = 1883 

client = mqtt.Client("Client2")

client.on_connect=on_connect
client.on_message=on_message

# client.connect(local_broker_hostname, port)

try:
    client.connect(broker_hostname, port)
    print("conectado a mosquito...")
except socket.error as e:
    print("Error de conexión al broker MQTT en Docker:", e)
    try:
        client.connect(local_broker_hostname, port)
        print("conectado a localhost...")
    except socket.error as e:
        print("Error de conexión al broker MQTT local:", e)

client.loop_start()

try:
    time.sleep(4000000)
finally:
    client.loop_stop()



# {"mensaje": "Gas a niveles peligrosos","fecha": "15/05/23","hora": "17:34","latitud": "52.32","long": "-91.02"}

#mosquitto_pub -t Test -m '{"esp32": "chunche3", "mensaje": "Gas a niveles peligrosos","fecha": "15/05/23","hora": "17:34","latitude": 52.32,"longitude": -91.02}'

#sudo docker run -it -p 1883:1883 -p 9001:9001 -v /home/diego/api-rest-djando-reportes/mqtt/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto

    # serviciomqtt:
    #     image: diego178q/serviciomqtt 
    #     networks:
    #         - reportNet
    #     depends_on:
    #         - mosquito
    #     restart: always
