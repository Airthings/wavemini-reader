# Airthings Wave Mini Sensor Reader

Airthings Wave Mini includes sensors for temperature, pressure, humidity and volatile organic compounds (VOC) measurements. Additionally, you can simply wave in front of the device to get a visual indication of your indoor air quality.

This is a project to provide users a starting point (```read_wavemini.py``` to read current sensor values from a [Airthings Wave Mini](https://www.airthings.com/no/wave-mini) devices using a Raspberry Pi 3 Model B over Bluetooth Low Energy (BLE).

**Table of contents**

- [Airthings Wave Mini Sensor Reader](#airthings-wave-mini-sensor-reader)
- [Requirements](#requirements)
  - [Setup Raspberry Pi](#setup-raspberry-pi)
  - [Turn on the BLE interface](#turn-on-the-ble-interface)
  - [Installing linux and python packages](#installing-linux-and-python-packages)
  - [Downloading script](#downloading-script)
- [Usage](#usage)
- [Sensor data description](#sensor-data-description)
- [Contribution](#contribution)
- [Release notes](#release-notes)

# Requirements

The following tables shows a compact overview of dependencies for this project.

**List of OS dependencies**

| OS          | model/version          | Comments              |
|-------------|------------------------|-----------------------|
| Raspbian    | Raspberry Pi 3 Model B | Used in this project. |
| Linux       | x86 Debian             | Should work according to [bluepy](https://github.com/IanHarvey/bluepy) |


**List of linux/raspberry dependencies**

| package        | version     | Comments                            |
|----------------|-------------|-------------------------------------|
| python         | 2.7 or 3    | Tested with python 2.7.13 and 3.7.3 |
| python-pip     |             | pip for python2.7                   |
| python3-pip    |             | pip3 for python3                    |
| git            |             | To download this project            |
| libglib2.0-dev |             | For bluepy module                   |

**List of third-party Python dependencies**

| module      | version     |
|-------------|-------------|
| bluepy      | 1.3.0       |


## Setup Raspberry Pi

The first step is to setup the Raspberry Pi with Raspbian. An installation guide for 
Raspbian can be found on the [Raspberry Pi website](https://www.raspberrypi.org/downloads/raspbian/).
In short: download the Raspbian image and write it to a micro SD card.

To continue, you need access to the Raspberry Pi using either a monitor and keyboard, or 
by connecting through WiFi or ethernet from another computer. The latter option does not 
require an external screen or keyboard and is called “headless” setup. To access a headless 
setup, you must first activate SSH on the Pi. This can be done by creating a file named ssh 
in the boot partition of the SD card. Connect to the Pi using SSH from a command line 
interface (terminal):

```
$ ssh pi@raspberrypi.local
```

The default password for the ```pi``` user is ```raspberry```.

## Turn on the BLE interface

In the terminal window on your Raspberry Pi:

```
pi@raspberrypi:~$ bluetoothctl
[bluetooth]# power on
[bluetooth]# show
[bluetooth]# exit
```

After issuing the command ```show```, a list of bluetooth settings will be printed
to the Raspberry Pi terminal window. Look for ```Powered: yes```.

## Installing linux and python packages

Raspbian images usually comes with Python (2 and/or 3) pre-installed.

```
pi@raspberrypi:~$ python2 --version
pi@raspberrypi:~$ python3 --version
```

Install dependencies:

```bash
pi@raspberrypi:~$ sudo apt-get update && sudo apt-get install libglib2.0-dev git
# For Python 2
pi@raspberrypi:~$ sudo apt-get install python-pip 
pi@raspberrypi:~$ sudo pip2 install bluepy==1.3.0
# For python 3
pi@raspberrypi:~$ sudo apt-get install python3-pip
pi@raspberrypi:~$ sudo pip3 install bluepy==1.3.0
```

## Downloading script

Downloading using git:

```
pi@raspberrypi:~$ sudo git clone https://github.com/Airthings/wavemini-reader.git
```

Downloading using wget:

```
pi@raspberrypi:~$ wget https://raw.githubusercontent.com/Airthings/wavemini-reader/master/read_wavemini.py
```

# Usage

The general format for calling the script is as follows:

```bash
sudo python read_wavemini.py SERIAL_NUMBER SAMPLE_PERIOD [> somefile.txt]
```

After a short delay, the script will print the current sensor values to the 
Raspberry Pi terminal window. Optionally, you may pipe the readings to a
text-file using ```> somefile.txt```. Exit the script using ```Ctrl+C```.


| Positional input arguments | Type | Description  |
|----------------------------|------|--------------|
| SERIAL_NUMBER | Integer | 10-digit number found under the magnetic backplate of your Airthings product.
| SAMPLE_PERIOD | Integer | Time in seconds between reading the current sensor values (excluding the overhead of connecting to target).


Example output:
```
Temperature: 27.33 *C, Pressure: 998.56 hPa, Humidity: 25.51 %rH, VOC: 48 ppm
Temperature: 27.33 *C, Pressure: 998.56 hPa, Humidity: 25.51 %rH, VOC: 48 ppm
Temperature: 27.33 *C, Pressure: 998.56 hPa, Humidity: 25.51 %rH, VOC: 48 ppm
Temperature: 27.33 *C, Pressure: 998.56 hPa, Humidity: 25.51 %rH, VOC: 48 ppm
```

> **Note**: The scripts require that your device is advertising. If your device is paired/connected to e.g. a phone, you need to turn off bluetooth on your phone while using the scripts.

> **Note on choosing a sample period:** 
Sensor values are updated every 5 minutes.


# Sensor data description

| sensor                        | units               |
|-------------------------------|---------------------|
| Temperature                   | &deg;C              |
| Pressure                      | hPa                 |
| Humidity                      | %rH                 |
| VOC                           | ppm                 |

# Contribution

Let us know how it went! If you want contribute, you can do so by posting issues or suggest enhancement
[here](https://github.com/Airthings/wavemini-reader/issues).


# Release notes

Initial release 2-June-2020
