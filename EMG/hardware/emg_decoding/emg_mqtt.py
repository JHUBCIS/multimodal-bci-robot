from paho.mqtt import client as mqtt_client

broker = '3.128.94.230'
port = 1883
topic = "test"
client_id = 'ba65a9d7-0107-465b-8909-23819238909000'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, char):
    msg = f"messages: {char}"
    result = client.publish(topic, char)
    status = result[0]
    if status == 0:
        print(f"Sent {char} to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")