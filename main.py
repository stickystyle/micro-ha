import machine
import dht
import time
import ubinascii
import ujson

#from umqtt.simple import MQTTClient
from umqtt.robust import MQTTClient

machine_id = ubinascii.hexlify(machine.unique_id()).decode('utf-8')

BROKER = "192.168.10.200"
TOPIC = 'homeassistant'
CLIENT_ID = "esp8266_{}".format(machine_id)

TEMP_INTERVAL = 600000

PIR_CONFIG_TOPIC = '{}/binary_sensor/{}/config'.format(TOPIC, CLIENT_ID)
PIR_STATE_TOPIC = '{}/binary_sensor/{}/motion'.format(TOPIC, CLIENT_ID)

TEMP_CONFIG_TOPIC = '{}/sensor/{}/config'.format(TOPIC, CLIENT_ID)
TEMP_STATE_TOPIC = '{}/sensor/{}/temperature'.format(TOPIC, CLIENT_ID)

BIRTH_LWT_TOPIC = '{}/{}/status'.format(TOPIC, CLIENT_ID)

dht_pin = machine.Pin(4)
pir_pin = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

d = dht.DHT22(dht_pin)

client = MQTTClient(CLIENT_ID, BROKER)
client.set_last_will(topic=BIRTH_LWT_TOPIC, msg='offline', retain=True)
resp = client.connect()
print("Connected to {}, {}".format(BROKER, resp))

client.publish(topic=BIRTH_LWT_TOPIC, msg='online', retain=True)

client.publish(topic=TEMP_CONFIG_TOPIC, msg='{{"name":"{:s}_temperature", "state_topic":"{}"}}'.format(CLIENT_ID, TEMP_STATE_TOPIC))
client.publish(topic=PIR_CONFIG_TOPIC, msg='{{"name":"{:s}_motion", "device_class": "motion", "state_topic":"{}"}}'.format(CLIENT_ID, PIR_STATE_TOPIC))

last_dht_read = time.ticks_ms()
pir_vals = {0: 'OFF', 1: 'ON'}
last_pir = 0
client.publish(topic=PIR_STATE_TOPIC, msg='OFF', retain=False)
d.measure()
mesurements = {'temperature': d.temperature(), 'humidity': d.humidity()}
client.publish(topic=TEMP_STATE_TOPIC, msg=ujson.dumps(mesurements), retain=True)
while True:
    pir_status = pir_pin.value()
    if time.ticks_diff(time.ticks_ms(), last_dht_read) > TEMP_INTERVAL:
        d.measure()
        mesurements = {'temperature': d.temperature(), 'humidity': d.humidity()}
        last_dht_read = time.ticks_ms()
        client.publish(topic=TEMP_STATE_TOPIC, msg=ujson.dumps(mesurements), retain=True)
    if pir_status != last_pir:
        print(pir_status, last_pir)
        client.publish(topic=PIR_STATE_TOPIC, msg=pir_vals[pir_status], retain=False) 
        last_pir = pir_status
