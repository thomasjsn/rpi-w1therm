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


def add_msg_to_queue(topic, payload):
  msg = {
    'topic': 'sensor/office/temp/{}'.format(topic),
    'payload': "{:.2f}".format(payload),
    'qos': 0,
    'retain': False
  }

  msgs.append(msg)


while True:
  for sensor in W1ThermSensor.get_available_sensors():
    temp = sensor.get_temperature()

    add_msg_to_queue(sensors[sensor.id], temp)
    print("Sensor {} has temperature {:.2f}".format(sensors[sensor.id], temp))

    temps.append(temp)

  average = sum(temps)/len(temps)
  print("Average temperature is {:.2f}".format(average))
  add_msg_to_queue('average', average)
  
  publish.multiple(msgs, hostname="192.168.1.119", client_id="rack_temp")

  temps.clear()
  time.sleep(15)
