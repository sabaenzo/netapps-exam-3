from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
import re
import requests
import socket
from authenticate import Authenticator
import canvas
import time, sys
import RPi.GPIO as GPIO
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf, IPVersion, ServiceInfo
import time
import logging
import argparse
redPin = 12   		#Set to appropriate GPIO
greenPin = 16	 #Should be set in the
bluePin = 20


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

red = GPIO.PWM(redPin, 1000)
blue = GPIO.PWM(bluePin, 1000)
green = GPIO.PWM(greenPin, 1000)



app = Flask(__name__)


status=''
color=''
intensity=''

@app.route('/LED', methods=['GET','POST'])
def led():
    global status
    global color
    global intensity
    if request.method =='GET':

        retStatus={'Status':status, 'Color':color, 'Intensity':intensity}
        print("Reporting status")
        return retStatus


    elif request.method == 'POST':

        status = str(request.args.get('status'))

        color = str(request.args.get('color'))

        intensity = str(request.args.get('intensity'))
        #Turn off all LEDs
        red.start(0)
        green.start(0)
        blue.start(0)
        red.ChangeDutyCycle(0)
        green.ChangeDutyCycle(0)
        blue.ChangeDutyCycle(0)
        if status == 'off':
            red.ChangeDutyCycle(0)
            green.ChangeDutyCycle(0)
            blue.ChangeDutyCycle(0)
            color=''
            intensity='0'

            return "Turned off LED"
        if color =='red':
            print("red")
            print(int(intensity))
            red.ChangeDutyCycle(int(intensity))
        elif color=='green':
            print("green")
            green.ChangeDutyCycle(int(intensity))
        elif color=='blue':
            print("blue")
            blue.ChangeDutyCycle(int(intensity))
        elif color=='magenta':
            print("magenta")
            red.ChangeDutyCycle(int(intensity))
            blue.ChangeDutyCycle(int(intensity))
        elif color=='cyan':
            print("cyan")
            blue.ChangeDutyCycle(int(intensity))
            green.ChangeDutyCycle(int(intensity))
        elif color=='yellow':
            print("yellow")
            red.ChangeDutyCycle(int(intensity))
            green.ChangeDutyCycle(int(intensity))
        elif color=='white':
            print("white")
            red.ChangeDutyCycle(int(intensity))
            blue.ChangeDutyCycle(int(intensity))
            green.ChangeDutyCycle(int(intensity))
        return "Post Request fulfilled"

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument('--v6', action='store_true')
    version_group.add_argument('--v6-only', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)
    if args.v6:
        ip_version = IPVersion.All
    elif args.v6_only:
        ip_version = IPVersion.V6Only
    else:
        ip_version = IPVersion.V4Only

    colorz = "(red|green|blue|yellow|magenta|cyan|white)"
    desc = dict(path='/LED', colors=colorz)
    local_ip = socket.gethostbyname(socket.gethostname()+'.local')
    print(local_ip)
    local_ip = socket.inet_aton(local_ip)

    info = ServiceInfo(
        "_http._tcp.local.",
        "LEDrpi._http._tcp.local.",
        addresses=[local_ip],
        port=5000,
        properties=desc,
        server="ash-2.local.",
    )

    zeroconf = Zeroconf(ip_version=ip_version)
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    try:
        app.run(host=socket.gethostbyname(socket.gethostname()+'.local'),port=5000, debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()




