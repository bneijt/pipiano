PiPiano
=======

_Simple boot script start and connect fluidsynth on Raspbian_

This project is a simple start-up script to have a Raspberry pi work as a simple software synth
for a USB Midi keyboard.


Installation
------------

The following commands will install `git`, clone this repository onto your Raspbian and install all required dependencies

    sudo apt-get install git
    sudo git clone https://github.com/bneijt/pipiano.git /opt/pipiano
    sudo /opt/pipiano/install.sh


Usage
-----

After installation, the `/opt/pipiano/start.py` script will be started as a `systemctl` service at boot.

It should just get you a working installation if you have the keyboard connected when you boot the pi.

Debugging can be done using:

    sudo systemctl status pipiano
    sudo systemctl restart pipiano

If you want to configure `fluidsynth`, you can edit the commands in `/opt/pipiano/fluid_config.txt`.


Uninstall
---------
To uninstall this, do the reverse of everything in the `install.sh` script:

    systemctl stop pipiano
    systemctl disable pipiano
    rm /etc/systemd/system/pipiano.service
    rm -rf /opt/pipiano



