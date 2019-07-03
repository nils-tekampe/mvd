import uuid
from datetime import datetime
from serpy import Serializer, IntField, StrField, MethodField
from json import JSONEncoder
import json
import os
import logging


logger = logging.getLogger(__name__)


class VersionNumber:

    def __init__(self, _major, _minor, _patch=None):
        self.major = _major
        self.minor = _minor
        self.patch = _patch

    def __str__(self):
        return "V" + self.major + "." + self.minor + "." + self.patch
       