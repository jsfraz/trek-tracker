
from datetime import datetime, timezone
import random
import time
import os
from dotenv import load_dotenv
import socketio
from gnss_data import GNSSData
import serial

def test_load_config():
    """Loads confing needed for connecting to server from .env file."""

    # Get project root path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    # Load envs
    env_file = '.env.development'
    dotenv_path = os.path.join(project_root, env_file)
    load_dotenv(dotenv_path)

    # Get envs

    # HTTPS
    securityScheme = 'http'
    if os.getenv('HTTPS').lower() == 'true':
        securityScheme = 'https'
    # Server
    server = os.getenv('SERVER_ADDRESS')
    # Port
    port = int(os.getenv("SERVER_PORT"))
    # API key
    apiKey = os.getenv('API_KEY')
    # Constants
    global SOCKETIO_URL
    SOCKETIO_URL = securityScheme + '://' + server + ':' + str(port) + '?apiKey=' + apiKey
    global SOCKETIO_RECCONECT_DELAY
    SOCKETIO_RECCONECT_DELAY = int(os.getenv('RECONNECT_DELAY'))

def test_send_single_location():
    """Connects to server and pushes one location pseudo data."""

    # Load config
    test_load_config()

    # create client
    sio = socketio.Client(reconnection=True, reconnection_delay=SOCKETIO_RECCONECT_DELAY)

    # Connect
    sio.connect(SOCKETIO_URL)

    # Create GNSSData instance
    gnss_data = GNSSData(0, 0, 0, datetime.now(timezone.utc).isoformat())
    # Send data to Socket.IO server
    print(gnss_data.__dict__)
    time.sleep(1)
    sio.emit('sendCurrent', gnss_data.__dict__)
    time.sleep(1)

    # Disconnect
    sio.disconnect()

def test_send_short_trip():
    """Connects to server and sends 60 location pseudo data."""

    # Load config
    test_load_config()

    # Create client
    sio = socketio.Client(reconnection=True, reconnection_delay=SOCKETIO_RECCONECT_DELAY)

    # Connect
    sio.connect(SOCKETIO_URL)

    # Send data
    start_lat, start_lon = 50.0755, 14.4378  # Prague
    
    for _ in range(60):
        timestamp = datetime.now(timezone.utc).isoformat()
        lat = start_lat + random.uniform(-0.01, 0.01)
        lon = start_lon + random.uniform(-0.01, 0.01)
        speed = random.uniform(0, 100)  # Km/h
        
        gnss_data = GNSSData(lat, lon, speed, timestamp)
        sio.emit('sendCurrent', gnss_data.__dict__)
        time.sleep(1)

    # Disconnect
    sio.disconnect()
