# -*-: coding utf-8 -*-
""" Skill definition from a YAML config. """

# pylint: disable=too-few-public-methods
class SkillDef:
    """ Skill definition from a YAML config. """

    def __init__(self, package_name, class_name, pip, params, intent_defs):
        """ Initialisation.

        :param package_name: the name of the Python module
        :param class_name: the name of the Python class
        :param pip: the pip package (name or url).
        :param params: the parameters to pass to the skills constructor.
        :param intent_defs: a list of intent definitions
        """
        self.package_name = package_name
        self.class_name = class_name
        self.pip = pip
        self.params = params
        self.intent_defs = intent_defs

    def find(self, intent):
        for intent_def in self.intent_defs:
            if intent_def.name == intent.intentName:
                return intent_def
        return None