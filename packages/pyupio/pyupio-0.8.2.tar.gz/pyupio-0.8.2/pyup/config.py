# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import yaml
try:  # pragma: no cover
    basestring
except NameError:  # pragma: no cover
    basestring = str
import re


SCHEDULE_REGEX = re.compile(
    # has to begin with every
    "^every "
    # followed by day/month
    "((day|month)$"
    # or week/two weeks
    "|(week|two weeks))"
    # with an optional weekday
    "( on (monday|tuesday|wednesday|thursday|friday|saturday|sunday))?"
)


class Config(object):

    UPDATE_ALL = "all"
    UPDATE_INSECURE = "insecure"
    # the docs had a typo at some point that incorrectly reffered to 'security'
    # instead of 'insecure'.
    UPDATE_INSECURE_TYPO = "security"
    UPDATE_NONE = ["False", "false", False, None]

    def __init__(self):
        self.close_prs = True
        self.branch = "master"
        self.branch_prefix = "pyup-"
        self.pr_prefix = ""
        self.pin = True
        self.search = True
        self.requirements = []
        self.label_prs = False
        self.schedule = ""
        self.assignees = []
        self.update = Config.UPDATE_ALL
        self.update_hashes = True

    def update_config(self, d):
        """
        Updates the config object.
        :param d: dict
        """
        for key, value in d.items():
            if hasattr(self, key):
                if key == "requirements":
                    items, value = value, []
                    for item in items:
                        if isinstance(item, basestring):
                            req = RequirementConfig(path=item)
                        elif isinstance(item, dict):
                            path, item = item.popitem()
                            req = RequirementConfig(
                                path=path,
                                pin=item.get("pin", None),
                                compile=item.get("compile", False),
                                update=item.get("update", Config.UPDATE_ALL)
                            )
                        value.append(req)
                        # add constraint requirement files to config
                        if req.compile:
                            for spec in req.compile.specs:
                                value.append(RequirementConfig(path=spec, pin=False))
                elif key == "assignees":
                    # assignees can be a string or a list. If it's a string, convert it to a list
                    # to make things consistent
                    if isinstance(value, basestring):
                        value = [value, ]
                elif key == 'pr_prefix':
                    # make sure that pr prefixes don't contain a PIPE
                    if "|" in value:
                        continue
                # cast ints and floats to str
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    value = str(value)

                setattr(self, key, value)

    @staticmethod
    def generate_config_file(config):
        return "\n\n".join([
            "# autogenerated pyup.io config file \n# see https://pyup.io/docs/configuration/ "
            "for all available options",
            yaml.safe_dump(config, default_flow_style=False)
        ])

    def _get_requirement_attr(self, attr, path):
        """
        Gets the attribute for a given requirement file in path
        :param attr: string, attribute
        :param path: string, path
        :return: The attribute for the requirement, or the global default
        """
        for req_file in self.requirements:
            if path.strip("/") == req_file.path.strip("/"):
                return getattr(req_file, attr)
        return getattr(self, attr)

    def can_pin(self, path):
        """
        Checks if requirements in `path` can be pinned.
        :param path: string, path to requirement file
        :return: bool
        """
        return self._get_requirement_attr(attr="pin", path=path)

    def can_update_all(self, path):
        """
        Checks if requirements in `path` can be updated.
        :param path: string, path to requirement file
        :return: bool
        """
        return self._get_requirement_attr("update", path=path) == Config.UPDATE_ALL

    def can_update_insecure(self, path):
        """
        Checks if requirements in `path` can be updated if insecure.
        :param path: string, path to requirement file
        :return: bool
        """
        return self._get_requirement_attr("update", path=path) in (Config.UPDATE_ALL,
                                                                   Config.UPDATE_INSECURE,
                                                                   Config.UPDATE_INSECURE_TYPO)

    def is_valid_schedule(self):
        return SCHEDULE_REGEX.search(self.schedule) is not None

    def __repr__(self):
        return str(self.__dict__)


class RequirementConfig(object):

    def __init__(self, path, pin=None, compile=False, update=Config.UPDATE_ALL):
        self.path = path
        self.pin = pin
        self.compile = CompileConfig(specs=compile.get("specs", [])) if compile else False
        self.update = update

        # set pin default
        if self.pin is None:
            self.pin = True

    def __repr__(self):
        return str(self.__dict__)


class CompileConfig(object):

    def __init__(self, specs=list()):
        self.specs = specs

    def __repr__(self):
        return str(self.__dict__)
