import inspect
from typing import Union

import yaml

from remotemanager.connection.url import URL
from remotemanager.script.script import Script
from remotemanager.utils import get_version

package_collect = [
    "host",
    "user",
    "port",
    "timeout",
    "max_timeouts",
    "python",
    "submitter",
    "shell",
    "raise_errors",
    "sshpass_override",
    "cmd_history_depth",
    "landing_dir",
    "ssh_insert",
    "quiet_ssh",
    "shebang",
]


class Computer(Script, URL):
    """
    Combo class that allows for connection to a machine and generating jobscripts
    """

    def __init__(self, template, **kwargs):
        # super() behaves strangely with multiple inheritance
        # explicitly call the __init__ with self
        URL.__init__(self, **kwargs)
        Script.__init__(self, template=template, **kwargs)

    def pack(
            self,
            collect_values: bool = True,
            ignore_none: bool = True,
            prune_defaults: bool = True,
            *args,
            **kwargs,
    ) -> dict:
        """
        Package up this Computer to a dictionary that can be stored as a yaml file.

        A note on collection:
        The collected values are explicitly stated in `package_collect`.
        Automated collection is possible, but not feasible for "human readable" outputs

        __dict__ collects the internal variables
        So instead of `user`, you get the `_conn` dictionary

        Using dir() is an option, but collects far too many variables, and also
        has the possibility to accidentally call functions as it crawls the object

        Args:
            collect_values (bool):
                Also collect any stored values if True. Defaults to True.
            ignore_none (bool):
                skip any None values in serialisation. Defaults to True.
            prune_defaults (bool):
                Collects only non-default values if True. Defaults to True.

        Returns:
            dict:
                serialised output
        """
        # preface the data with the version info
        spec = {"remotemanager_version": get_version()}
        # collect info
        for item in package_collect:
            val = getattr(self, item, None)
            if val is None:
                continue
            spec[item] = val

        # cleanup for non-serialisable entities
        try:
            spec["verbose"] = self.verbose.level
        except AttributeError:
            spec["verbose"] = self.verbose

        # gather any non-private vals
        for k, v in self.__dict__.items():
            if k in spec:
                continue
            if ignore_none and v is None:
                continue
            if k not in self.args and not k.startswith("_"):
                spec[k] = v

        manual_defaults = {"landing_dir": "$HOME", "port": 22}
        if prune_defaults:
            # grab defaults for removal
            signature = inspect.signature(URL.__init__)
            for k, v in signature.parameters.items():
                if k in spec and spec.get(k, None) == v.default:
                    del spec[k]
            # special handler, for complex defaults
            for k, v in manual_defaults.items():
                if spec.get(k, None) == v:
                    del spec[k]

        spec["template"] = Script.pack(self, values=collect_values)

        return spec

    @classmethod
    def unpack(cls, data: dict) -> "Computer":
        return cls(**data)

    def to_dict(self, *args, **kwargs) -> dict:
        if "collect_values" not in kwargs:
            kwargs["collect_values"] = False
        return self.pack(*args, **kwargs)

    @classmethod
    def from_dict(cls, data: dict) -> "Computer":
        return cls.unpack(data)

    def to_yaml(self, file: str = None) -> Union[None, str]:
        """
        Dump the computer to yaml. Returns the yaml content as a string if file is None
        """
        data = self.to_dict()

        # extract template so we can format it manually
        template = data.pop("template")
        template = "\n".join([f"  {line}" for line in template.split("\n")])

        content = yaml.dump(data, sort_keys=False)
        content += f"template: |\n{template}"

        if file is None:
            return content

        with open(file, mode="w+", encoding="utf8") as o:
            o.write(content)

    @classmethod
    def from_yaml(cls, file: str = None, data: str = None) -> "Computer":
        if file is not None:
            with open(file, mode="r", encoding="utf8") as o:
                data = yaml.safe_load(o)

            return cls(**data)

        if data is not None:
            return cls(**yaml.safe_load(data))

        raise ValueError("Please provide a file path to file, or yaml content to data")
