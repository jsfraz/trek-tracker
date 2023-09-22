import serial
import pynmea2
from gnss_data import GNSSData
import socketio
import time

SOCKETIO_URL = 'http://192.168.1.107:8080?apiKey=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2OTUzOTUwOTcsIm5iZiI6MTY5NTM5NTA5Nywic3ViIjo0fQ.NCCdXFoQiiUpf614y5G80Zy3YEMp_fnqbKet9vivXyQ'
SOCKETIO_RECCONECT_DELAY = 1
SOCKETIO_INITIAL_CONNECT_DELAY = 10
SERIAL_PORT = '/dev/serial0'
BAUD_RATE = 115200
SERIAL_TIMEOUT = 1

# Connect to Socket.IO server
sio = socketio.Client(reconnection=True, reconnection_delay=SOCKETIO_RECCONECT_DELAY)

# Define event handlers
@sio.event
def connect():
    print('Connected to the server.')

@sio.event
def connect_error(data):
    print('The connection failed: ' + data)

@sio.event
def disconnect():
    print('Disconnected from the server.')

canConnect = False
while canConnect == False:

    try:
        # TODO pass the API key as parameter
        sio.connect(SOCKETIO_URL)
        canConnect = True
    except Exception as e:
        print(e)
        time.sleep(SOCKETIO_INITIAL_CONNECT_DELAY)

# Define the serial port and settings
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=SERIAL_TIMEOUT)

try:

    while True:
        # Read data from the serial port
        data = ser.readline().decode('utf-8').strip()
        
        # Check if data is not empty
        if data:
            try:
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
                    # print(gnss_data.__.dict__)
                    sio.emit('sendCurrent', gnss_data.__dict__)
                
            except Exception as e:
                print('Error:', e)
        
except KeyboardInterrupt:
    # Handle Ctrl+C to exit the loop gracefully
    ser.close()
    print('\nSerial port closed.')