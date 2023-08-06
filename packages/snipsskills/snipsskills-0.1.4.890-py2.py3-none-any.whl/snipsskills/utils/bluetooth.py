# -*-: coding utf-8 -*-
""" Bluetooth setup utilities. """

import getpass
import os
import subprocess
import time

from snipsskillscore.logging import log, log_warning

from .os_helpers import cmd_exists, download_file, execute_command, remove_file, ask_yes_no
from .systemd import Systemd

SNIPSBLE_SERVICE_NAME = "snipsble"


class Bluetooth:
    """ Bluetooth setup utilities. """

    @staticmethod
    def setup():
        """ Setting up Bluetooth Relay MQTT service. """
        if ask_yes_no("Would you like to enable Bluetooth for this device?") == False:
            return

        try:
            Bluetooth.install_node()
        except Exception:
            log_warning("Could not download Node, which is required for Bluetooth. " +
                        "Please install Node manually, and restart the snipsskills installation script.")
            return

        Bluetooth.install_mqtt_relay()
        Bluetooth.setup_systemd()

    @staticmethod
    def install_node():
        """ Install node using dpkg, if it is not installed. """
        if cmd_exists('node'):
            return

        log("Node is required for Bluetooth setup. Installing Node.")

        filename = "node_latest_armhf.deb"

        log("Downloading Node.")
        download_file(
            "http://node-arm.herokuapp.com/node_latest_armhf.deb", filename)

        log("Installing Node.")
        execute_command("sudo dpkg -i node_latest_armhf.deb")
        remove_file(filename)

    @staticmethod
    def install_mqtt_relay():
        """ Install snips-mqtt-relay. """
        if not cmd_exists('node'):
            return

        log("Installing snips-mqtt-relay.")
        execute_command("npm install -g snips-mqtt-relay")

    @staticmethod
    def setup_systemd():
        (username, snipsble_path) = Bluetooth.get_params()
        contents = Systemd.get_template(SNIPSBLE_SERVICE_NAME)
        if contents is None:
            return
        contents = contents.replace("{{SNIPSBLE_PATH}}", snipsble_path)
        Systemd.write_systemd_file(SNIPSBLE_SERVICE_NAME, username, contents)

    @staticmethod
    def get_params():
        current_username = getpass.getuser()
        username = raw_input(
            "Run as user [default: {}]: ".format(current_username))
        if username is None or username.strip() == "":
            username = current_username

        try:
            snipsble_path = subprocess.check_output(
                ['which', 'snipsble']).strip()
        except subprocess.CalledProcessError:
            snipsble_path = None

        if snipsble_path is None or len(snipsble_path.strip()) == 0:
            snipsble_path = raw_input("Path to the Snips BLE library: ")

        return (username, snipsble_path)
