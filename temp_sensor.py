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

while True:
  for sensor in W1ThermSensor.get_available_sensors():
    msg = {
      'topic': 'sensor/office/temp/{}'.format(sensors[sensor.id]),
      'payload': "{:.2f}".format(sensor.get_temperature()),
      'qos': 0,
      'retain': False
    }

    msgs.append(msg)
    print("Sensor {} has temperature {:.2f}".format(sensors[sensor.id], sensor.get_temperature()))

  publish.multiple(msgs, hostname="192.168.1.119", client_id="rack_temp")
  time.sleep(15)
