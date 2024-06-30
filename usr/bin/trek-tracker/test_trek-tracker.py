
from datetime import datetime, timezone
import time
import os
from dotenv import load_dotenv
import socketio
from gnss_data import GNSSData

def test_test():
    result = 1 + 1
    assert result == 2

def test_send_data():
    # Získání cesty k kořenovému adresáři projektu
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    # Načtení .env.test souboru
    env_file = '.env.test'
    # env_file = '.env.developement'
    dotenv_path = os.path.join(project_root, env_file)
    load_dotenv(dotenv_path)

    # get envs
    # https
    securityScheme = 'http'
    if os.getenv('HTTPS').lower() == 'true':
        securityScheme = 'https'
    # server
    server = os.getenv('SERVER_ADDRESS')
    # port
    port = int(os.getenv("SERVER_PORT"))
    # API key
    apiKey = os.getenv('API_KEY')
    # constants
    SOCKETIO_URL = securityScheme + '://' + server + ':' + str(port) + '?apiKey=' + apiKey
    SOCKETIO_RECCONECT_DELAY = int(os.getenv('RECONNECT_DELAY'))

    # create client
    sio = socketio.Client(reconnection=True, reconnection_delay=SOCKETIO_RECCONECT_DELAY)
    # define event handlers
    @sio.event
    def connect():
        print('Connected to the server.')

    @sio.event
    def connect_error(data):
        print(data)

    @sio.event
    def disconnect():
        print('Disconnected from the server.')

    # connect
    sio.connect(SOCKETIO_URL)

    # create GNSSData instance
    gnss_data = GNSSData(0, 0, 0, datetime.now(timezone.utc).isoformat())
    # Send data to Socket.IO server
    print(gnss_data.__dict__)
    time.sleep(1)
    sio.emit('sendCurrent', gnss_data.__dict__)
    time.sleep(1)
    sio.disconnect()