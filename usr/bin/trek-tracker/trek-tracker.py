from datetime import timezone
import serial
import pynmea2
from gnss_data import GNSSData
import socketio
import time
import RPi.GPIO as GPIO
import configparser

# Server
SOCKETIO_URL = ''
SOCKETIO_RECCONECT_DELAY = 1
SOCKETIO_INITIAL_RECONNECT_DELAY = 10
# Pins
PIN_PIEZO = 40      # Piezo pin
# Other
SERIAL_PORT = '/dev/serial0'
BAUD_RATE = 115200
SERIAL_TIMEOUT = 1

def beep(count, duration):
    """Beep using piezo."""

    try:
        pin = GPIO.PWM(PIN_PIEZO, 520)      # PWM instance
        for x in range(count):
            pin.start(50)       # Start with duty cycle 50
            pin.ChangeFrequency(520)
            GPIO.output(PIN_PIEZO, GPIO.HIGH)
            time.sleep(duration)
            pin.stop()
            GPIO.output(PIN_PIEZO, GPIO.LOW)
            if x != count - 1:
                time.sleep(0.3)
    except Exception as e:
        print(e)

# Config
configName = 'trek-tracker'
config = configparser.ConfigParser()
try:
    config.read('/etc/trek-tracker/trek-tracker.conf')
    # HTTPS
    securityScheme = 'http'
    if config[configName]['https'].lower() == 'true':
        securityScheme = 'https'
    # Server
    server = config[configName]['ServerAddress']
    # Port
    port = int(config[configName]['ServerPort'])
    # API key
    apiKey = config[configName]['ApiKey']
    # Constants
    SOCKETIO_URL = securityScheme + '://' + server + ':' + str(port) + '?apiKey=' + apiKey
    SOCKETIO_RECCONECT_DELAY = int(config[configName]['ReconnectDelay'])
    SOCKETIO_INITIAL_RECONNECT_DELAY = int(config[configName]['InitialReconnectDelay'])
    BAUD_RATE = int(config[configName]['BaudRate'])
except Exception as e:
    print(e)
    beep(3, 1)
    exit(1)

# Pin setup
GPIO.setmode(GPIO.BOARD)
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

# Wait for 1 second
time.sleep(1)

while True:
    '''
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
                timestamp = msg.datetime.now(timezone.utc).isoformat()
                
                # Convert speed from knots to km/h
                speed_kmph = float(speed_knots) * 1.852  # 1 knot = 1.852 km/h
                
                # Create GNSSData instance
                gnss_data = GNSSData(latitude, longitude, speed_kmph, timestamp)
                # Send data to Socket.IO server
                print(gnss_data.__dict__)
                sio.emit('sendCurrent', gnss_data.__dict__)
            else:
                print('Not RMC message')
            
        else:
            print('No data!')
    except Exception as e:
        print('Error:', e)
    '''