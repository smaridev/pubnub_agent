import io
import json
import time

import paho.mqtt.client as mqtt
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNReconnectionPolicy, PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

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

client = mqtt.Client()
deviceserialno = getserial()

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-a57ab586-2e94-11e9-8208-aaa77ad184aa'
pnconfig.publish_key = 'pub-c-395634b8-6b43-407a-bd80-e656f030d997'
pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR
pnconfig.uuid = 'thingpointReceiver_' + deviceserialno
 
pubnub = PubNub(pnconfig)

 
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    print ("inside the function my_publish_callback")
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
 
class MySubscribeCallback(SubscribeCallback):
    def __init__(self):
      #self.f = open("/sys/class/thermal/thermal_zone0/temp", "r")
      #self.t = self.f.read().strip()
      #self.cputemp = "CPU temp "+ str(self.t)
      pass

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
 
        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc self.cputemp = "CPU temp: "+t
            pass

        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
            
    def message(self, pubnub, message):
        global client
        global deviceserialno
        print("message topic: {}".format(message.channel))
        app_topic = message.channel.replace("cloud_to_edge." + deviceserialno + ".", '')
        print("app_topic:{}".format(app_topic))
        client.publish(app_topic, message.payload)
      
def main():
    """run the application"""
    global client
    global deviceserialno
    client.connect("localhost", 1883, 60)
    client.loop_start()
    pubnub.add_listener(MySubscribeCallback())
    downstream_channel = "cloud_to_edge." + deviceserialno + ".*"
    print("subscribing to downstream channel :{}".format(downstream_channel))
    pubnub.subscribe().channels(downstream_channel).execute()
    
if __name__ == '__main__':
    main()
