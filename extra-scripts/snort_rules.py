#!/usr/bin/python

import re
import sys
import os
import logging
import argparse
import cx_Oracle

from db_operation import *
from logger import setup_logging, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def get_signature_data_from_files(dir_path):
    try:
        logger.info("Inside get_signature_data_from_files function.")
        results = []
        if os.path.isdir(dir_path):
            logger.info("Reading files for alarms from %s directory." % dir_path)
            # file = open('snort_rules_output.txt', 'w')
            for filename in os.listdir(dir_path):
                if filename.endswith(".rules"):
                    file_path = os.path.join(dir_path, filename)
                    string_name = os.path.splitext(filename)[0].upper()
                    file_object = open(file_path, 'r')
                    content = file_object.readlines()
                    for line in content:
                        match_object = re.findall('msg:"([^"]*).*sid:(\d+)', line, re.M | re.I)
                        if match_object:
                            alarm_name = str(match_object[0][0]).strip().replace(string_name, "", 1)
                            sign_id = match_object[0][1]
                            results.append({'file_name': filename, 'sign_id': sign_id, 'alarm_name': alarm_name})
                            # file.write("%s, %s, %s\n" % (filename, sign_id, alarm_name))
                    file_object.close()
                    # file.close()
        return results
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Error caught in get_signature_data_from_files function. %s" % ex)


class NFArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

    def initialize(self):
        group = self.add_argument_group('Script Inputs')
        group.add_argument('-s', '--server',
                           action="store",
                           help="Oracle DB Server Address/Name",
                           dest="server")

        group.add_argument('-u', '--user',
                           action="store",
                           help="User Name to access Oracle DB Server",
                           dest="username")

        group.add_argument('-p', '--password',
                           action="store",
                           help="Password to access Oracle DB Server",
                           dest="password")

        group.add_argument('-d', '--device_type_id',
                           action="store",
                           help="DeviceType ID",
                           dest="device_type_id")

        group.add_argument('-f', '--dir_path',
                           action="store",
                           help="DIRECTORY PATH",
                           dest="dir_path")

        self.add_argument('-v', '--verbose',
                          action="store_true",
                          default=False,
                          help="Print verbose logging on screen")

        if len(sys.argv) == 1:
            self.print_help()
            sys.exit(1)

    def validate(self):
        parsed_result = self.parse_args()
        if not parsed_result.server:
            self.error("Missing Oracle DB Server Address")
        if not parsed_result.username:
            self.error("Missing Oracle DB UserName")
        if not parsed_result.password:
            self.error("Missing Oracle DB Password")
        if not parsed_result.device_type_id:
            self.error("Missing DeviceType ID")
        if not parsed_result.dir_path:
            self.error("Missing Directory Path.")
        return parsed_result


def do_input_validation():
    parser = NFArgumentParser(add_help=True)
    parser.initialize()
    return parser.validate()


def main():
    root_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_path)
    result = do_input_validation()
    result.verbose = True
    setup_logging(logfile="Snort_Rules_Signature.log", scrnlog=True)
    data_path = os.path.join(root_path, "Snort_Rules_Signature")
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    logger.info(
        "Running Script with -> Oracle Server: %s, Oracle User: %s, DeviceType ID: %s, DIR Path: %s, Verbose: %s"
        % (result.server, result.username, result.device_type_id, result.dir_path, result.verbose))
    directory_path = result.dir_path
    database_name = 'nfdb'
    file_path = os.path.join(data_path, "snort_rules_difference.txt")
    try:
        connection = cx_Oracle.connect('%s/%s@%s/%s' % (result.username, result.password, result.server, database_name))
        logger.info("Connection object created. User: %s, Database: %s, Server: %s" %
                    (result.username, database_name, result.server))
        db_signature_details = get_signature_data_from_db(connection_obj=connection,
                                                          device_type_id=result.device_type_id)
        results = get_signature_data_from_files(dir_path=directory_path)
        logger.info("Total %s records found from files inside directory %s" % (len(results), directory_path))
        file_object = open(file_path, 'w')
        file_object.write("%s,%s\n" % ("sign_id", "alarm_name"))
        for item in results:
            if item['sign_id'] not in db_signature_details.keys():
                file_object.write("%s,%s\n" % (item['sign_id'], item['alarm_name']))
        file_object.close()
        logger.info("Output file: %s successfully generated." % file_path)
    except Exception, ex:
        logger.exception(ex)


if __name__ == '__main__':
    main()
