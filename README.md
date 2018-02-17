Setup Instructions for batman-adv on Raspbian
---------------------------------------------

* Set Locale
  * Run `raspi-config`
  * Add en-US locale
  * Set locale to en-US
  * Change keyboard layout
* Configure wifi
  * still `raspi-config`, it's easier
* Install git from packages
  * `sudo apt install git`
* Install deps (see notes below)
  - libnl-3-dev libnl-genl-3-dev libcap-dev libgps-dev gpsd
* Clone batctl from source git
* `make install` batctl
* Install script (tbd, had to manually write it)
* Take down dhcpcd service
  * `sudo service dhcpcd stop`
* Run setup script
* `sudo batctl o`


TODOs, Short-term
-----------------

* Disable interfering and unneccesary init scripts (dhcpcd)
  - DONE
* write new init scripts to bring up bat0 and wlan0 under batman-adv
  - DONE
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
