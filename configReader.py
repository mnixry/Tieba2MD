import os
from typing import Any

from yaml import safe_load

CONFIG_DIR = './settings.yml'
DEFAULT_DIR = './settings.default.yml'


class NewDict(dict):
    default = dict()

    def __getattr__(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError:
            if key in self.default.keys():
                return self.default[key]
            else:
                raise

    __setaddr__ = dict.__setitem__

    def __delattr__(self, key: str) -> Any:
        try:
            del self[key]
        except KeyError:
            if key in self.default.keys():
                del self.default[key]
            else:
                raise


def Convert2NewDict(oldDict: dict) -> NewDict:
    newDict = NewDict()
    for perKey in oldDict:
        value: Any = oldDict[perKey]
        if isinstance(value, dict):
            newDict[perKey] = Convert2NewDict(value)
        else:
            newDict[perKey] = value
    return newDict


def initConfigFile() -> NewDict:
    if not os.path.isfile(CONFIG_DIR):
        with open(DEFAULT_DIR, 'rb') as df, open(CONFIG_DIR, 'wb') as cf:
            cf.write(df.read())
    with open(CONFIG_DIR, 'rt', encoding='utf-8') as f:
        configRead: Any = safe_load(f)
    with open(DEFAULT_DIR, 'rt', encoding='utf-8') as f:
        defaultRead: dict = safe_load(f)
    newDict = Convert2NewDict(configRead)
    newDict.default = defaultRead
    return newDict


CONFIG_READ = initConfigFile()
