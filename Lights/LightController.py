#!/usr/bin/env python3

from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json

import asyncio
import uuid
import argparse

CONFIG_FILE = 'tradfri_standalone_psk.conf'
IPAdress = "192.168.2.102"
SafetyKey = "hP5WF0MhBLugeUTf"

async def run(Brightness, Color):
    # Assign configuration variables.
    # The configuration check takes care they are present.
    conf = load_json(CONFIG_FILE)

    try:
        identity = conf[IPAdress].get('identity')
        psk = conf[IPAdress].get('key')
        api_factory = APIFactory(host=IPAdress, psk_id=identity, psk=psk)
    except KeyError:
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host=IPAdress, psk_id=identity)

        try:
            psk = await api_factory.generate_psk(SafetyKey)
            print('Generated PSK: ', psk)

            conf[IPAdress] = {'identity': identity,
                               'key': psk}
            save_json(CONFIG_FILE, conf)
        except AttributeError:
            raise PytradfriError("Please provide the 'Security Code' on the "
                                 "back of your Tradfri gateway using the "
                                 "-K flag.")

    api = api_factory.request

    gateway = Gateway()

    devices_command = gateway.get_devices()
    devices_commands = await api(devices_command)
    devices = await api(devices_commands)

    lights = [dev for dev in devices if dev.has_light_control]

    # Lights can be accessed by its index, so lights[1] is the second light
    if lights:
        light = lights[0]
    else:
        print("No lights found!")
        light = None


    if light:

        # Example 4: Set the light level of the light
        dim_command = light.light_control.set_dimmer(Brightness)
        await api(dim_command)

        # Example 5: Change color of the light
        # f5faf6 = cold | f1e0b5 = normal | efd275 = warm
        color_command = light.light_control.set_hex_color(Color)
        await api(color_command)


    await api_factory.shutdown()

def setLights(Brightness, Temperature):
    ColorTemp = 'f5faf6'

    if Temperature == 0:
        ColorTemp = 'f5faf6'
    if Temperature == 1:
        ColorTemp = 'f1e0b5'
    if Temperature == 2:
        ColorTemp = 'efd275'

    loop = asyncio.new_event_loop().run_until_complete(run(Brightness, ColorTemp))
    asyncio.set_event_loop(loop)

