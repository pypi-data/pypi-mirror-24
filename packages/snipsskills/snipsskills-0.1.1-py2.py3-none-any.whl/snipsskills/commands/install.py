# -*-: coding utf-8 -*-
"""The install command."""

import os
import shutil

from .base import Base, SNIPSFILE, ASSISTANT_DIR, ASSISTANT_ZIP_FILENAME, \
    ASSISTANT_ZIP_PATH, INTENTS_DIR

from ..utils.assistant_downloader import AssistantDownloader, \
    AssistantDownloaderException
from ..utils.intent_class_generator import IntentClassGenerator
from ..utils.snipsfile_parser import Snipsfile, SnipsfileParseException, \
    SnipsfileNotFoundError
from ..utils.pip_installer import PipInstaller


# pylint: disable=too-few-public-methods
class Install(Base):
    """The install command."""

    def run(self):
        """ Command runner. """
        try:
            snipsfile = Snipsfile(SNIPSFILE)
        except SnipsfileNotFoundError:
            print("Snipsfile not found. Please create one.")
            return
        except SnipsfileParseException as err:
            print(err)
            return

        if snipsfile.assistant_url is None:
            print("No assistants found in Snipsfile.")

        print("Fetching assistant")
        try:
            AssistantDownloader.download(snipsfile.assistant_url,
                                         ASSISTANT_DIR,
                                         ASSISTANT_ZIP_FILENAME)
        except AssistantDownloaderException:
            print("Error downloading assistant. " +
                  "Make sure the provided URL in the Snipsfile is correct, " +
                  "and that there is a working network connection.")
            return

        print("Generating definitions")
        try:
            shutil.rmtree(INTENTS_DIR)
        except Exception:
            pass

        generator = IntentClassGenerator()
        generator.generate(ASSISTANT_ZIP_PATH, INTENTS_DIR)

        if snipsfile.skills is not None and len(snipsfile.skills) > 0:
            print("Installing skills")
            for skill in snipsfile.skills:
                print("Installing {}".format(skill.package_name))
                PipInstaller.install(skill.package_name)

        print("Cleaning up")
        os.remove(ASSISTANT_ZIP_PATH)
