# -*-: coding utf-8 -*-
""" USB utilities. """

from __future__ import absolute_import
import os
import re
import subprocess
import logging

import usb.core
import usb.util


class USB:

    class Device:
        unknown, respeaker, conexant = range(3)

    # this method should work in all platorms
    @staticmethod
    def get_boards():
        print("+++++++++++++++ 1")
        all_devices = usb.core.find(find_all=True)

        print("+++++++++++++++ 2")
        if not all_devices:
            return USB.Device.unknown

        for board in all_devices:
            print(str(board))
            try:
                devices = board.product.lower()
                if devices.find("respeaker") >= 0:
                    return USB.Device.respeaker
                elif devices.find("conexant") >= 0:
                    return USB.Device.conexant
                else:
                    return USB.Device.unknown
            except Exception as e:
                logging.warning("Exception getting product string: %s", e)
                continue

        return USB.Device.unknown

    @staticmethod
    def get_usb_led_device():
        devices = USB.lsusb()
        if not devices:
            return None

        devices = devices.lower()

        if devices.find("respeaker") >= 0:
            return USB.Device.respeaker
        elif devices.find("conexant") >= 0:
            # TODO: check if this is the string to look for
            return USB.Device.conexant

        return USB.Device.unknown

    @staticmethod
    def lsusb():
        FNULL = open(os.devnull, 'w')
        try:
            # Raspberry
            return subprocess.check_output(["lsusb"])
        except:
            try:
                # OSX
                return subprocess.check_output(["system_profiler", "SPUSBDataType"])
            except:
                return None
