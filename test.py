import unittest
import mvd
import uuid
import hashlib
import random
import json
from logEntry import LogEntry, LogFile
import filecmp
import os
from fileHandling import carriesValidVersionInformation
import shutil

TESTFOLDER = "/tmp/testfolderMVD/"


class Test_TestInfrastructure(unittest.TestCase):
    def test_createLogFileStoreAndReadBack(self):
        print("Starting Test")
        log_file = LogFile("logfile.json")
        for i in range(1000):
            entry = LogEntry('test.txt', 'add', None)
            log_file.addLogEntry(entry)
        log_file.writeToJSON()

        log_file = LogFile("logfile2.json")
        log_file.readFromJSON("logfile.json")
        log_file.writeToJSON()
        self.assertTrue(filecmp.cmp('logfile.json', 'logfile2.json'))
        os.remove('logfile.json')
        os.remove('logfile2.json')

    def test_doesFileNameCarryVersionInformation(self):
        self.assertTrue(carriesValidVersionInformation("textV1.0.0.txt"))
        self.assertTrue(carriesValidVersionInformation(
            "textV33332323231.0.1.txt"))
        self.assertTrue(carriesValidVersionInformation(
            "textV2.024234234.0.txt"))
        self.assertTrue(carriesValidVersionInformation(
            "/home/test/textV1.0.0.txt"))
        self.assertTrue(carriesValidVersionInformation(
            "üüüü/textV1.0.0.txtasdfasdf"))

        self.assertFalse(carriesValidVersionInformation("textX1.0.00.txt"))
        self.assertFalse(carriesValidVersionInformation("textV1.0a.1.txt"))
        self.assertFalse(carriesValidVersionInformation("text_2.0.0.txt"))
        self.assertFalse(carriesValidVersionInformation(
            "/home/test/textV_1.0.0.txt"))

    def test_initMVD(self):

        if os.path.exists(TESTFOLDER) is True:
            shutil.rmtree(TESTFOLDER)

        os.mkdir(TESTFOLDER)
        mvd.initMVD(TESTFOLDER)
        assert(os.path.exists(TESTFOLDER + "./mvd"), True)
        assert(os.path.exists(TESTFOLDER + "./mvd/mvd.log"), True)


if __name__ == '__main__':
    unittest.main()
