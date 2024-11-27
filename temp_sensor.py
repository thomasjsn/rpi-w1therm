import paho.mqtt.client as mqtt
import queue
import time
from w1thermsensor import W1ThermSensor

sensors = {
    #'0517021db9ff': 'above_rack',
    #'0517022f8eff': 'rack_back',
    #'0416a02b0eff': 'garage_outside',
    '051702869eff': 'garage_outside'
}

msgs = queue.Queue()
#temps = []
available = []


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    #client.subscribe(cfg.mqtt['prefix'] + "/pdu/outlet/+/+")

    if rc==0:
        client.connected_flag=True
        #client.publish("$CONNECTED/rack-temp", 1, retain=True)
    else:
        client.bad_connection_flag=True


def add_msg_to_queue(topic, payload):
  msg = {
    'topic': 'sensor/rpi-temp/{}'.format(topic),
    'payload': "{:.1f}".format(payload),
    'qos': 0,
    'retain': False
  }

  msgs.put(msg)
  #print(msg)


def set_sensor_status():
  for uuid, sensor in sensors.items():
    msg = {
      'topic': 'sensor/rpi-temp/{}/status'.format(sensor),
      'payload': 'online' if sensor in available else 'offline',
      'qos': 0,
      'retain': False
    }

    msgs.put(msg)
    #print(msg)


client = mqtt.Client("rpi-temp")
client.on_connect = on_connect
#client.on_message = on_message
#client.will_set("$CONNECTED/rack-temp", 0, qos=0, retain=True)
client.connect("mqtt.lan.uctrl.net")
client.loop_start()


while True:
  for sensor in W1ThermSensor.get_available_sensors():
    try:
      temp = sensor.get_temperature()

      add_msg_to_queue(sensors[sensor.id], temp)
      #print("sensor: %s (%s) is %.2f" % (sensor.id, sensors[sensor.id], temp))

      #temps.append(temp)
      available.append(sensors[sensor.id])
    except w1thermsensor.errors.SensorNotReadyError:
      print("Sensor was not ready")

  #average = sum(temps)/len(temps)

  #set_sensor_status()
  #add_msg_to_queue('average', average)
  #print("average from %d sensors is %.2f" % (len(temps), average))

  while not msgs.empty():
    client.publish(**msgs.get())

  #temps.clear()
  #available.clear()
  time.sleep(60)
