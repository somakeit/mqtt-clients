#!/usr/bin/env python

import paho.mqtt.client
import mqtt_config
import time

TOPIC = 'somakeit/space/open'
FILE = '/home/wordpress/wordpress/open.htm'

space = None

mqtt = paho.mqtt.client.Client(client_id=mqtt_config.client_id, clean_session=True)
mqtt.tls_set(('/etc/ssl/certs/ca-certificates.crt'))
mqtt.username_pw_set(mqtt_config.user_name, mqtt_config.password)
mqtt.connect(mqtt_config.server, port=mqtt_config.port)

def on_disconnect(client, userdata, rc):
    print 'reconnecting..'
    mqtt.reconnect()

def on_connect(client, userdata, flags, rc):
    mqtt.subscribe(TOPIC, qos=1)

def on_message(client, userdata, msg):
    global space
    content = None

    if msg.payload == '1':
        if space == 'open':
            return

        content = '''
            <h1>So Make It is Open</h1>
            <p>This means that the switch in the space is on.<p>
            <p>Space has been open since ''' + time.strftime('%H:%M', time.localtime()) + ''' on ''' +  time.strftime('%A %b %d', time.localtime()) + '''.</p>
            <p>This should mean that a keyholder is in the space now and intends to stay for at least the next half hour. If you want to be sure of their plans, try raising them on <a href="/chat">chat</a> by typing "?say what you want to say to them" or looking at them by typing "?webcam".</p>
        '''

        space = 'open'

    elif msg.payload == "0":
        if space == 'closed':
            return

        content = '''
            <h1>So Make It is Closed</h1>
            <p>This means that the switch in the space is off.<p>
            <p>Space has been closed since ''' + time.strftime('%H:%M', time.localtime()) + ''' on ''' +  time.strftime('%A %b %d', time.localtime()) + '''.</p>
            <p>This should mean that no keyholder is in the space and willing to remain for the next half an hour. You could confirm this is the case by going to <a href="/chat">chat</a> and typing "?webcam" to look at the space or maybe "?say what you want to say" to try to speak to the people in space.</p>
            <p>If space really is closed and this saddens you, maybe you can apply to be a <a href="https://members.somakeit.org.uk/roles">keyholder</a>?
        '''

        space = 'closed'

    else:
        if space == 'broken':
            return

        content = '''
            <h1>Uh-oh, It's Broken</h1>
            <p>This button is broken, the space is both open and closed until you observe it.<p>
            <p>Observe the space by going to <a href="/chat">chat</a> and typing "?webcam" to look at the space, or maybe "?say what you want to say" to try to speak to the people in space.</p>
            <p>People are probably working hard to re-instate the button and this page will tell you if the space is open or closed in the near future.</p>
        '''

        space = 'broken'

    if content != None:
        f = open(FILE, 'w')
        f.write(content)
        f.close()

mqtt.on_connect = on_connect
mqtt.on_disconnect = on_disconnect
mqtt.on_message = on_message

mqtt.connect(mqtt_config.server, port=mqtt_config.port)
mqtt.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=True)
