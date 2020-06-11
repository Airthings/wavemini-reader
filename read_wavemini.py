# MIT License
#
# Copyright (c) 2018 Airthings AS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# https://airthings.com

import bluepy.btle as btle
import argparse
import signal
import struct
import sys
import time


class WaveMini():

    CURR_VAL_UUID = btle.UUID("b42e3b98-ade7-11e4-89d3-123b93f75cba")

    def __init__(self, serial_number):
        self._periph = None
        self._char = None
        self.mac_addr = None
        self.serial_number = serial_number

    def is_connected(self):
        try:
            return self._periph.getState() == "conn"
        except Exception:
            return False

    def discover(self):
        scan_interval = 0.1
        timeout = 3
        scanner = btle.Scanner()
        for _count in range(int(timeout / scan_interval)):
            advertisements = scanner.scan(scan_interval)
            for adv in advertisements:
                if self.serial_number == _parse_serial_number(adv.getValue(btle.ScanEntry.MANUFACTURER)):
                    return adv.addr
        return None

    def connect(self, retries=1):
        tries = 0
        while (tries < retries and self.is_connected() is False):
            tries += 1
            if self.mac_addr is None:
                self.mac_addr = self.discover()
            try:
                self._periph = btle.Peripheral(self.mac_addr)
                self._char = self._periph.getCharacteristics(uuid=self.CURR_VAL_UUID)[0]
            except Exception:
                if tries == retries:
                    raise
                else:
                    pass

    def read(self):
        rawdata = self._char.read()
        return CurrentValues.from_bytes(rawdata)

    def disconnect(self):
        if self._periph is not None:
            self._periph.disconnect()
            self._periph = None
            self._char = None


class CurrentValues():

    def __init__(self, temperature, humidity, voc):
        self.temperature = temperature  #: Temperature in degree Celsius
        self.humidity = humidity  #: Humidity in %rH
        self.voc = voc  #: Volatile Organic Compounds in ppm

    @classmethod
    def from_bytes(cls, rawdata):
        data = struct.unpack("<HHHHHHLL", rawdata)
        return cls(round(data[1]/100.0 - 273.15, 2), data[3]/100.0, data[4])

    def __str__(self):
        msg = "Temperature: {} *C, ".format(self.temperature)
        msg += "Humidity: {} %rH, ".format(self.humidity)
        msg += "VOC: {} ppm".format(self.voc)
        return msg


def _parse_serial_number(manufacturer_data):
    try:
        (ID, SN, _) = struct.unpack("<HLH", manufacturer_data)
    except Exception:  # Return None for non-Airthings devices
        return None
    else:  # Executes only if try-block succeeds
        if ID == 0x0334:
            return SN


def _argparser():
    parser = argparse.ArgumentParser(prog="read_wavemini", description="Script for reading current values from a Wave Mini product")
    parser.add_argument("SERIAL_NUMBER", type=int, help="Airthings device serial number found under the magnetic backplate.")
    parser.add_argument("SAMPLE_PERIOD", type=int, default=60, help="Time in seconds between reading the current values")
    args = parser.parse_args()
    return args


def _main():
    args = _argparser()
    wavemini = WaveMini(args.SERIAL_NUMBER)

    def _signal_handler(sig, frame):
        wavemini.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, _signal_handler)

    while True:
        wavemini.connect(retries=3)
        current_values = wavemini.read()
        print(current_values)
        wavemini.disconnect()
        time.sleep(args.SAMPLE_PERIOD)


if __name__ == "__main__":
    _main()
