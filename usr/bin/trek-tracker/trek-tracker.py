import serial
import pynmea2
from gnss_data import GNSSData
import socketio
import time
import RPi.GPIO as GPIO
import subprocess
from threading import Thread
import configparser

# server
SOCKETIO_URL = ''
SOCKETIO_RECCONECT_DELAY = 1
SOCKETIO_INITIAL_RECONNECT_DELAY = 10
# pins
PIN_SHUTDOWN_BUTTON = 5     # on/off pin
PIN_PIEZO = 40      # piezo pin
# other
SERIAL_PORT = '/dev/serial0'
BAUD_RATE = 115200
SERIAL_TIMEOUT = 1

# beep using piezo
def beep(count, duration):
    try:
        pin = GPIO.PWM(PIN_PIEZO, 520)      # pwm instance
        for x in range(count):
            pin.start(50)       # start with duty cycle 50
            pin.ChangeFrequency(520)
            GPIO.output(PIN_PIEZO, GPIO.HIGH)
            time.sleep(duration)
            pin.stop()
            GPIO.output(PIN_PIEZO, GPIO.LOW)
            if x != count - 1:
                time.sleep(0.3)
    except Exception as e:
        print(e)

# config
configName = 'trek-tracker'
config = configparser.ConfigParser()
try:
    config.read('/etc/trek-tracker/trek-tracker.conf')
    # https
    securityScheme = 'http'
    if config[configName]['https'] == 'True' or config[configName]['https'] == 'true':
        securityScheme = 'https'
    # server
    server = config[configName]['ServerAddress']
    # port
    port = int(config[configName]['ServerPort'])
    # API key
    apiKey = config[configName]['ApiKey']
    # constants
    SOCKETIO_URL = securityScheme + '://' + server + ':' + str(port) + '?apiKey=' + apiKey
    SOCKETIO_RECCONECT_DELAY = int(config[configName]['ReconnectDelay'])
    SOCKETIO_INITIAL_RECONNECT_DELAY = int(config[configName]['InitialReconnectDelay'])
    BAUD_RATE = int(config[configName]['BaudRate'])
except Exception as e:
    print(e)
    beep(3, 1)
    exit(1)

# pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_SHUTDOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_PIEZO, GPIO.OUT)

# Socket.IO server
sio = socketio.Client(reconnection=True, reconnection_delay=SOCKETIO_RECCONECT_DELAY)

# Define event handlers
@sio.event
def connect():
    print('Connected to the server.')
    beep(2, 0.25)

@sio.event
def connect_error(data):
    print(data)
    beep(2, 1)

@sio.event
def disconnect():
    print('Disconnected from the server.')

# listener for shutdown button
def shutdown_button_listener():
    pressed = False
    while True:
        # button is pressed when pin is LOW
        if not GPIO.input(PIN_SHUTDOWN_BUTTON):
            if not pressed:
                print('Shutting down...')
                sio.disconnect()
                beep(1, 1)
                # must be run as superuser!!!
                subprocess.call(['shutdown', '-h', 'now'], shell=False)
        # button not pressed (or released)
        else:
            pressed = False
        time.sleep(0.1)

# start listening for shutdown button press in separated thread
shutdown_button_thread = Thread(target=shutdown_button_listener, name='shutdownButton')
shutdown_button_thread.start()

beep(1, 0.25)
time.sleep(1)
canConnect = False
while canConnect == False:

    try:
        sio.connect(SOCKETIO_URL)
        canConnect = True
    except Exception as e:
        print(e)
        time.sleep(SOCKETIO_INITIAL_RECONNECT_DELAY)

# Define the serial port and settings
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=SERIAL_TIMEOUT)

while True:
    try:
        # Read data from the serial port
        data = ser.readline().decode('utf-8').strip()
        
        # Check if data is not empty
        if data:
            # Parse the NMEA sentence
            msg = pynmea2.parse(data)
                
            if isinstance(msg, pynmea2.RMC):
                # Extract latitude, longitude, speed, and timestamp
                latitude = msg.latitude
                longitude = msg.longitude
                speed_knots = msg.spd_over_grnd
                timestamp = msg.datetime.utcnow().isoformat()
                
                # Convert speed from knots to km/h
                speed_kmph = float(speed_knots) * 1.852  # 1 knot = 1.852 km/h
                
                # Create GNSSData instance
                gnss_data = GNSSData(latitude, longitude, speed_kmph, timestamp)
                # Send data to Socket.IO server
                print(gnss_data.__dict__)
                sio.emit('sendCurrent', gnss_data.__dict__)
            
        else:
            print('No data!')

    except Exception as e:
        print('Error:', e)