import serial
import pynmea2
import json

# Define the serial port and settings with a baud rate of 115200
ser = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

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
                    timestamp = msg.datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
                    
                    # Convert speed from knots to km/h
                    speed_kmph = float(speed_knots) * 1.852  # 1 knot = 1.852 km/h
                    
                    # Create a dictionary with the extracted information
                    data_dict = {
                        "latitude": latitude,
                        "longitude": longitude,
                        "speed": speed_kmph,
                        "timestamp": timestamp,
                    }
                    
                    # Print the JSON data
                    print(json.dumps(data_dict, indent=4))
                
            except pynmea2.ParseError as e:
                print(f"Failed to parse NMEA sentence: {data}")
        
except KeyboardInterrupt:
    # Handle Ctrl+C to exit the loop gracefully
    ser.close()
    print("\nSerial port closed.")
