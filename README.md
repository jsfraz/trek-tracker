# trek-tracker

Trek tracker for tracking your motorcycles or whatever.

## Building

```bash
dpkg-deb -b . trek-tracker-1.0.0.deb
```

## Install requirements

```bash
pip3 install -r requirements.txt
```

## Serial console settings

```bash
sudo raspi-config
```

```bash
Interfacing Options
Serial Port
Would you like a login shell to be accessible over serial?
No
Would you like the serial port hardware to be enabled?
Yes
Ok
```
