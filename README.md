# Sensor-grid Project

## Design

## Getting Started

### Prepare Pi

#### Set Locale and Keyboard Layout

```
$ sudo raspi-config
```

* Add en-US locale
* Change keyboard layout

#### Configure Ethernet

In `/etc/network/interfaces` add the following lines:

```
auto eth0
allow-hotplug eth0
iface eth0 inet dhcp
```

#### Disable conflicting services

```
$ sudo service dhcpcd stop
$ sudo update-rc.d dhcpcd disable
```

### Install Software

#### Install dependencies

To build batman-adv and alfred, you will need the following packages:

* git
* libnl-3-dev
* libnl-genl-3-dev
* libcap-dev
* libgps-dev
* gpsd (optional, assuming we add gps modules later)

#### Build batctl

Pull and build batctl from the OpenMesh source repository

```
$ git clone https://git.open-mesh.org/batctl.git
$ cd batctl
$ sudo make install
```

#### Build alfred

Pull and build alfred from the OpenMesh source repository

```
$ git clone https://git.open-mesh.org/alfred.git
$ cd alfred 
$ sudo make install
```

Copy the alfred.service from config to /etc/systemd/system/alfred.service.

```
$ sudo cp config/alfred.service /etc/systemd/system/alfred.service
$ sudo systemctl daemon-reload
$ sudo systemctl start alfred.service
```

To check status of the running service:

```
$ sudo systemctl status alfred.service
```

And to have alfred come up at boot:

```
$ sudo systemctl enable alfred.service
```

### Configure Pi

#### Install batman-adv module

```
$ sudo echo "batman-adv" >> /etc/modules
```

#### Configure network interfaces

```
auto wlan0
iface wlan0 inet6 manual
  wireless-channel 1
  wireless-essid killer-mesh
  wireless-mode ad-hoc
  wireless-ap 02:12:34:56:78:9A
  pre-up /sbin/ifconfig wlan0 mtu 1532

auto bat0
iface bat0 inet6 auto
  pre-up /usr/local/sbin/batctl if add wlan0
```

#### Check interfaces

#### Check batctl



TODOs, Short-term
-----------------

* decide how to install batctl
  * Debian package is too old
  * create a new package? not a bad idea, can keep a local .deb
* Establish serial communication, maybe avoid needing to start on wifi?


Electron App
------------

The desktop app will likely function on a layer much higher than batman-adv. As
batman-adv networking will be largely transparent to us, we should expect to
write layer 7 software as we are accustomed. This may mean that a basic
client/server protocol could work for many functions, with gossip protocols to
distribute data along the network where nodes can no longer see all other nodes
in the network.


Points of Interest
------------------

* IP addresses aren't strictly necessary, routing can be done by hwaddr
* A super-peer may be necessary to offer IPs if we decide we need them


[Connect to a Raspberry Pi via SSH over USB](https://www.thepolyglotdeveloper.com/2016/06/connect-raspberry-pi-zero-usb-cable-ssh/)

[Read and write from serial port with Raspberry Pi](http://www.instructables.com/id/Read-and-write-from-serial-port-with-Raspberry-Pi/)

[Ad-hoc Wifi Networks - might be worth dropping in on the net sometimes](https://help.ubuntu.com/community/WifiDocs/Adhoc)

[Notes on how to configure batman-adv on Raspberry Pi 3](https://www.reddit.com/r/darknetplan/comments/68s6jp/how_to_configure_batmanadv_on_the_raspberry_pi_3/)

[Looks like batman-adv is already a part of the Debian kernel distro!](https://www.open-mesh.org/projects/open-mesh/wiki/Download)

Gossip Protocols:

* https://en.wikipedia.org/wiki/Gossip_protocol
* https://pythonhosted.org/gossip-python/
* https://github.com/clockworksoul/smudge
