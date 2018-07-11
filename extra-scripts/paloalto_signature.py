#!/usr/bin/python

import sys
import os
import csv
import argparse
import cx_Oracle
import logging

from db_operation import *
from logger import setup_logging, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

# DEVICE_TYPE_ID = 162


def read_from_csv(file_name):
    try:
        data_list = []
        csv_file = open(file_name, 'rb')
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            data_list.append(dict(id=str(row[0]), name=row[1], description=row[2]))
        return data_list
    except IOError, e:
        print("Could not read file: I/O error({0}): {1}".format(e.errno, e.strerror))
    except Exception, ex:
        print(ex)
        raise Exception("Error caught in read_from_csv function.")


class NFArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

    def initialize(self):
        group = self.add_argument_group('Server Inputs')
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

        group.add_argument('-c', '--csv_file',
                           action="store",
                           help="CSV File",
                           dest="csv_file")

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
        if not parsed_result.csv_file:
            self.error("Missing CSV file.")
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
    setup_logging(logfile="paloalto_signature.log", scrnlog=result.verbose)
    logger.info(
        "Running Script with -> Oracle Server: %s, Oracle User: %s, DeviceType ID: %s, CSV File: %s, Verbose: %s"
        % (result.server, result.username, result.device_type_id, result.csv_file, result.verbose))
    database_name = 'nfdb'
    data_path = os.path.join(root_path, "PaloAltoIPS_Signature")
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    file_path = os.path.join(data_path, "paloalto_ips_difference.txt")
    try:
        connection = cx_Oracle.connect('%s/%s@%s/%s' % (result.username, result.password, result.server, database_name))
        logger.info("Connection object created. User: %s, Database: %s, Server: %s" %
                    (result.username, database_name, result.server))
        db_signature_details = get_signature_data_from_db(connection_obj=connection,
                                                          device_type_id=result.device_type_id)
        logger.info("Total %s records fetch from the database for device_type_id: %s" %
                    (len(db_signature_details), result.device_type_id))
        results = read_from_csv(file_name=result.csv_file)
        logger.info("Total %s records fetched from the csv file." % (len(results)))
        file_object = open(file_path, 'w')
        file_object.write('"%s","%s","%s"\n' % ("alarm_id", "alarm_name", "alarm_description"))
        for item in results:
            if str(item['id']) not in db_signature_details.keys():
                file_object.write('"%s","%s","%s"\n' % (item['id'], item['name'], item['description']))
        file_object.close()
        logger.info("Output file: %s successfully generated." % file_path)
    except Exception, ex:
        logger.exception(ex)


if __name__ == '__main__':
    main()
