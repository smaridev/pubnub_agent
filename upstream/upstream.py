import io
import json
import time

import paho.mqtt.client as mqtt
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNReconnectionPolicy, PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
 
pnconfig.subscribe_key = 'sub-c-a57ab586-2e94-11e9-8208-aaa77ad184aa'
pnconfig.publish_key = 'pub-c-395634b8-6b43-407a-bd80-e656f030d997'
pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR
pnconfig.uuid = 'thing_point_1_uuid'
 
pubnub = PubNub(pnconfig)
client = mqtt.Client()
pubnub.publish().channel("aruba_to_cloud.tp1.healthmon/stats").message("test publish").sync()

deviceserialno = None

def getserial():
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
   
    return cpuserial 


def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        # Message successfully published to specified channel.
        print("success status:{}".format(status))
    else:
        # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
        print("error status:{}".format(status.error))



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global pnconfig
    global deviceserialno
    global pubnub
    print("message topic:" + str(msg.topic)+" "+str(msg.payload))
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    payload_dict = json.loads(m_decode)
    #converted_topic = msg.topic.replace("/",".") 
    forward_chanel = "edge_to_cloud." + str(deviceserialno) + "." + str(converted_topic)
    print("forward to pubnub channel: {}".format(forward_chanel))
    print("pubnub client:{}".format(dir(pubnub)))
    pubnub.publish().channel(forward_chanel).message(payload_dict).pn_async(my_publish_callback)
    print("after publish")


      
def main():
    """run the application"""
    global client
    global deviceserialno
    deviceserialno = getserial()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()


if __name__ == '__main__':
    main()
