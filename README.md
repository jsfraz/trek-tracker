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


## Shield

### Sketch

![Sketch](shield.png "Sketch")

### PCB

![PCB](shield_pcb.png "PCB")
