#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
from os import path
import logging
from logEntry import LogEntry, LogFile
import argparse
import sys
from versionNumber import VersionNumber
import zipfile
import fileHandling

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger(__name__)


class MVD:

    def __init__(self, _path=None):
        if _path is None:
            mvd_folder, log_file_path, trunk = "", "", ""
        mvd_folder, log_file_path, trunk = self.findMVDFolder(_path)
        if mvd_folder is None:
            logger.error(
                "Trying to perform operations on a directory that is not under version control. Please init first")
            exit(-1)
        else:
            self.log_file = LogFile(log_file_path)

    def initMVD(self, _path):
        if os.path.exists(_path) is False:
            logger.error("The folder " + _path + " does not exist.")
            return
        if findMVDFolder(_path) is not None:
            logger.error("The folder " + _path +
                         " already seems to be initialized; aborting.")
            return
        else:
            os.mkdir(_path+"/.mvd")
            os.mkdir(_path+"/.mvd/trunk")
            logfile = LogFile(_path+"/.mvd/mvd.log")
            logfile.writeToJSON()

    def findMVDFolder(self, _path):
        # This function walks up the folder tree starting with _path and looks for a
        # .mvd folder. If found, the complete path of the .mvd folder is returned.
        # If not found, the function returns None

        start_path = path.realpath(_path)

        if os.path.exists(start_path+"/au.mvd"):
            if os.file.exist(start_path+"/.mvd/mvd.log") and os.path.exists(start_path+"/.mvd/trunk"):
                logger.debug("findMVDFolder found: " + start_path)
                return start_path+"/.mvd", start_path+"/.mvd/mvd.log", start_path+"/.mvd/trunk"
            else:
                return None
                logger.debug(
                    "Found .mvd folder but no log file or no trunk folder present")
        else:
            new_path = path.realpath(path.join(start_path, '..'))
            # see if we are at the top
            if new_path == start_path:
                logger.debug(
                    "findMVDFolder reached top without finding anything")
                return None
            else:
                return findMVDFolder(new_path)

    def addFileToMVD(self, _file, _version):
        if os.path.exists(_file) is False:
            logger.error("The file " + _file +
                         " does not exist and can therefore not be added to version control.")
            return

        if _version is None:
            version = VersionNumber(0, 9, 0)
        else:
            version = _version

        mvd_folder, log_file, trunk_folder = findMVDFolder(_file)
        if mvd_folder is None:
            logger.error("No valid .mvd folder found for "+_file +
                         ". Please make sure that the folder has been initialized.")
            return None

        # we create a log entry for this operation
        log_entry = LogEntry(_file, "add")

        # We add the current file to the trunk.
        self.addFileToTrunk(_file, trunk_folder, log_entry.get_UUID)

        # Now, we need to append the version information

        # and then we add the log entry to the log file

    def addFileToTrunk(self, _file, _trunk, _uuid):
        zip_file = _trunk+"\\"+_uuid+"zip"
        if os.path.exists(zipfile) is True:
            logging.debug(
                "This should never happen. The file with the UUID in the trunk is already existing")
            return
        if os.path.exists(_file) is False:
            logging.error("The file " + _file +
                          " is not existing and can therefore not be added to the trunk.")
            return

        zipfile.ZipFile(zip_file, mode='w').write(_file)


def main(command, file):
    print(command)
    print(file)



def add(file):
    print("adding file")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='(m)eaningful (v)ersion (c)ontrol for documents')

    subparsers = parser.add_subparsers(help='commands', dest='command')

    # A list command
    add_parser = subparsers.add_parser(
        'init', help='Initialize a folder for version control')
    add_parser.add_argument('folder', action='store', help='folder to init')

    # A list command
    add_parser = subparsers.add_parser(
        'add', help='Add file under version control')
    add_parser.add_argument('file', action='store', help='file to add')

    args = parser.parse_args()

    if (args.command == "add"):
        add(args.file)
    elif (args.command == "init"):
        print(args)
        initMVD(args.folder)
        # initMVD(folder)
