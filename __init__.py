# Copyright (c) 2021 ritzenhoffj
# The LulzbotMenuPlugin is released under the terms of the AGPLv3 or higher.

from . import LulzbotMenuPlugin


def getMetaData():
    return {}

def register(app):
    return {"extension": LulzbotMenuPlugin.LulzbotMenuPlugin()}
