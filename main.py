import serial
import pynmea2
from gnss_data import GNSSData
import socketio
import time

SERIAL_PORT = '/dev/serial0'
BAUD_RATE = 115200
SERIAL_TIMEOUT = 1
SOCKETIO_SERVER = 'http://192.168.1.109:8080'
SOCKETIO_RECCONECT_DELAY = 1
SOCKETIO_INITIAL_CONNECT_DELAY = 10

# Define the serial port and settings
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=SERIAL_TIMEOUT)

# Connect to Socket.IO server
sio = socketio.Client(reconnection=True, reconnection_delay=SOCKETIO_RECCONECT_DELAY)

# Define event handlers
@sio.on('connect')
def on_connect():
    print('Connected to the server.')

@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from the server.')

canConnect = False
while canConnect == False:

    try:
        sio.connect(SOCKETIO_SERVER)
        canConnect = True
    except Exception as e:
        print(e)
        time.sleep(SOCKETIO_INITIAL_CONNECT_DELAY)

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
                    data = GNSSData(latitude, longitude, speed_kmph, timestamp)
                    # Send data to Socket.IO server
                    # print(data.__dict__)
                    sio.emit('sendCurrent', data.__dict__)
                
            except Exception as e:
                print('Error:', e)
        
except KeyboardInterrupt:
    # Handle Ctrl+C to exit the loop gracefully
    ser.close()
    print('\nSerial port closed.')