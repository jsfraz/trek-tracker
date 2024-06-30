# trek-tracker

Trek tracker for tracking your motorcycles or whatever.

## Installing

Packages `python3` and `python3-pip` are required:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

Install requirements, build and install the package.

```bash
pip3 install -r requirements.txt
dpkg-deb -b . trek-tracker-1.0.0.deb
sudo dpkg -i trek-tracker-1.0.0.deb
```

Serial console will be configured during installation.

<!--
## Manual serial console settings

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
-->