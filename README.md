# trek-tracker

Tracker for the [Trek project](https://github.com/jsfraz/trek-server).

## Used GPS module

- [Waveshare LC76G](https://www.waveshare.com/wiki/LC76G_GNSS_Module)

## Building and installing

```bash
dpkg-deb -b . trek-tracker-1.0.0.deb
sudo dpkg -i trek-tracker-1.0.0.deb
```

Or you can download and install the package from [Releases](https://github.com/jsfraz/trek-tracker/releases).

### Power on/power off button

To enable powering off with the button you MUST add `dtoverlay=gpio-shutdown` in the end of `/boot/config.txt` file.

## 3D printed case

![1](cases/Yuki%20250%20CSR/case.png "1")

Model created in [Blender](https://www.blender.org/), snapshot captured using [MeshLab](https://www.meshlab.net/).

## Shield

Created in [Fritzing](https://fritzing.org/).

### Sketch

![Sketch](images/shield.png "Sketch")

### PCB

![PCB top](images/shield_pcb_top.png "PCB top")

![PCB bottom](images/shield_pcb_bottom.png "PCB bottom")

Screenshot from [PCBWay online gerber viewer](https://www.pcbway.com/project/OnlineGerberViewer.html).

<!--
### Schema

![Schema](images/shield_pcb_schema.png "Schema")
-->
