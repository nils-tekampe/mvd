import uuid
from datetime import datetime
from serpy import Serializer, IntField, StrField, MethodField
from json import JSONEncoder
import json
import os
import logging


logger = logging.getLogger(__name__)


class LogEntry:

    def __init__(self, _file, _operation, _uuid=None, _hash=None):
        if _uuid is None:
            self.uuid = uuid.uuid1()
        else:
            self.uuid = uuid.UUID(_uuid)

        self.file = _file
        if (_operation in ["init", "add", "delete"]):
            self.operation = _operation

        else:
            logger.error(
                "This should never happen. Somehow an unknown type of operation slipped into the constructor.")
            return

        if (_hash == None):
            self.hash = "none"
        else:
            self.hash = _hash

    def get_UUID(self):
        return str(self.uuid)

    def getJSON(self):
        ret = "{"
        ret = ret + "\"operation\":" + '\"' + self.operation + '\"' + ","
        ret = ret + "\"file\":" + '\"' + self.file + '\"' + ","
        ret = ret + "\"hash\":" + '\"' + self.hash + '\"' + ","
        ret = ret + "\"uuid\":" + '\"' + self.get_UUID() + '\"' + "}"
        return ret


class LogFile:

    def __init__(self, _logfile_path=None):
        self.path = _logfile_path
        self.store = {}
        self.addLogEntry(LogEntry(logfile_path, "init"))
        
        if (os.path.exists(_logfile_path):
            readFromJSON(_logfile_path)
        

    def readFromJSON(self, file):
        self.clearLog()
        with open(file) as json_file:
            data = json.load(json_file)
            for entry in data['LogFile']['logentry']:
                self.addLogEntry(
                    LogEntry(entry['file'], entry['operation'], entry['uuid'], entry['hash']))

    def writeToJSON(self):
        # TODO: eine prüfsumme wäre nicht schlecht
        json_string = "{\"LogFile\": { \n"
        json_string = json_string+"\"logentry\": [ \n"
        for key, value in self.store.items():
            json_string = json_string+value.getJSON()+",\n"

        json_string = json_string[:-2] + "\n"
        json_string = json_string+"]}}"

        with open(self.path, "w") as write_file:
            write_file.write(json_string)

    def addLogEntry(self, log_entry):
        self.store[log_entry.get_UUID()] = log_entry

    def deleteLogEntry(self, log_entry):
        del self.store[log_entry.get_UUID()]

    def clearLog(self):
        self.store = {}
