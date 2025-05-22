import paho.mqtt.client as paho

class MQTTClient:
    def __init__(self, broker='broker.mqttdashboard.com', port=1883, topic='Rania/10'):
        self.client = paho.Client()
        self.client.on_publish = self.on_publish
        self.client.connect(broker, port)
        self.client.loop_start()
        self.topic = topic

    def on_publish(self, client, userdata, mid):
        print(f"MQTT message published with mid: {mid}")

    def publish_sleep_alert(self, message="sleep"):
        self.client.publish(self.topic, message, qos=1)
