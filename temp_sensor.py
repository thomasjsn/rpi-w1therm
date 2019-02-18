import time
import paho.mqtt.publish as publish
from w1thermsensor import W1ThermSensor

sensors = {
    '0517021db9ff': 'rack_ceiling',
    '0517022f8eff': 'rack_back',
    '0416a02b0eff': 'rack_front',
    '051702869eff': 'rack_floor'
}

msgs = []
temps = []
available = []


def add_msg_to_queue(topic, payload):
  msg = {
    'topic': 'sensor/office/temp/{}'.format(topic),
    'payload': "{:.2f}".format(payload),
    'qos': 0,
    'retain': False
  }

  msgs.append(msg)
  print(msg)


def set_sensor_status():
  for uuid, sensor in sensors.items():
    msg = {
      'topic': 'sensor/office/temp/{}/status'.format(sensor),
      'payload': 'online' if sensor in available else 'offline',
      'qos': 0,
      'retain': False
    }

    msgs.append(msg)
    print(msg)


while True:
  for sensor in W1ThermSensor.get_available_sensors():
    temp = sensor.get_temperature()

    add_msg_to_queue(sensors[sensor.id], temp)

    temps.append(temp)
    available.append(sensors[sensor.id])

  average = sum(temps)/len(temps)

  set_sensor_status()
  add_msg_to_queue('average', average)
  publish.multiple(msgs, hostname="192.168.1.119", client_id="rack_temp")

  temps.clear()
  available.clear()
  time.sleep(15)
