# -*-: coding utf-8 -*-
""" Bluetooth setup utilities. """

import getpass
import os
import subprocess
import time

from snipsskillscore.logging import log, log_warning

from .os_helpers import cmd_exists, download_file, execute_command, remove_file


class Bluetooth:
    """ Bluetooth setup utilities. """

    @staticmethod
    def setup():
        run_on_boot = raw_input(
            "Would you like to enable Bluetooth for this device? [Y/n] ")
        if run_on_boot is not None and run_on_boot.strip() != "" and run_on_boot.lower() != "y":
            return

        try:
            Bluetooth.install_node()
        except Exception:
            log_warning("Could not download Node, which is required for Bluetooth. " + \
                "Please install Node manually, and restart the snipsskills installation script.")
        

    @staticmethod
    def install_node():
        if cmd_exists('node'):
            return

        log("Node is required for Bluetooth setup. Installing Node.")

        filename = "node_latest_armhf.deb"
        download_file("http://node-arm.herokuapp.com/node_latest_armhf.deb", filename)
        execute_command("sudo dpkg -i node_latest_armhf.deb")
        remove_file(filename)
