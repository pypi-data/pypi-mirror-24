**Cloud4RPi** is a cloud control panel for your [IoT](https://en.wikipedia.org/wiki/Internet_of_things) device.
-----
[![Build Status](https://travis-ci.org/cloud4rpi/cloud4rpi.svg?branch=master)](https://travis-ci.org/cloud4rpi/cloud4rpi)

This package provides a client library that simplifies the connection to the [Cloud4RPi](https://cloud4rpi.io/) service.


## Cloud4RPi Features

- You can use widgets to display device data and send commands in real time.
- You can control your IoT devices remotely.
- You can connect any device to **Cloud4RPi**.
- You can use [MQTT](https://pypi.python.org/pypi/paho-mqtt) or HTTP to send data and receive control commands.

## Start Using

1. Install this package:
    ```bash
    sudo pip install cloud4rpi
    ```
1. Get examples for your platform:
    - Raspberry Pi: `wget https://github.com/cloud4rpi/raspberrypi-examples/archive/master.zip && unzip master.zip && rm master.zip && cd raspberrypi-examples-master`
    - C.H.I.P.: `wget https://github.com/cloud4rpi/chip-examples/archive/master.zip && unzip master.zip && rm master.zip && cd chip-examples-master`
    - Omega2: `wget https://github.com/cloud4rpi/omega2-examples/archive/master.zip && unzip master.zip && rm master.zip && cd omega2-examples-master`
1. Create a free account on [Cloud4RPi](https://cloud4rpi.io).
2. Create a device on the [Devices](https://cloud4rpi.io/devices) page.
3. Copy the **Device Token** from the device page.
4. Replace the `__YOUR_DEVICE_TOKEN__` string in one of the examples with your real device token.
5. Run the example with `python`.
6. Read the sample code and write your own code!

For detailed instructions, refer to the [documentation](https://cloud4rpi.github.io/docs/).

## See Also

* [PyPI Package](https://pypi.python.org/pypi/cloud4rpi)
* [Documentation Repository](https://github.com/cloud4rpi/docs)
* [Usage Examples for Raspberry Pi](https://github.com/cloud4rpi/raspberrypi-examples)
