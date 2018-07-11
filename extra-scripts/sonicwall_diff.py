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

DEVICE_TYPE_ID = 125


def read_file(file_name):
    try:
        logger.info("Inside read_file function. Reading '%s' file." % file_name)
        file_object = open(file_name, 'r')
        content = file_object.read().split("\n")
        result = []
        for line in content:
            if line:
                # print line
                line = line.split('\t')
                result.append(dict(id=line[0], name=line[1]))
        return result
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

        group.add_argument('-c', '--file',
                           action="store",
                           help="FILE",
                           dest="file")

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
        if not parsed_result.file:
            self.error("Missing text file.")
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
    setup_logging(logfile="sonicwall_diff_signature.log", scrnlog=result.verbose)
    logger.info(
        "Running Script with -> Oracle Server: %s, Oracle User: %s, DeviceType ID: %s, File: %s, Verbose: %s"
        % (result.server, result.username, result.device_type_id, result.file, result.verbose))
    database_name = 'nfdb'
    data_path = os.path.join(root_path, "Sonicwall_Signature")
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    file_path = os.path.join(data_path, "sonicwall_difference.txt")
    try:
        connection = cx_Oracle.connect('%s/%s@%s/%s' % (result.username, result.password, result.server, database_name))
        logger.info("Connection object created. User: %s, Database: %s, Server: %s" %
                    (result.username, database_name, result.server))
        db_signature_details = get_signature_data_from_db(connection_obj=connection,
                                                          device_type_id=result.device_type_id)
        logger.info("Total %s records fetch from the database for device_type_id: %s" %
                    (len(db_signature_details), result.device_type_id))
        results = read_file(file_name=result.file)
        logger.info("Total %s records fetched from the csv file." % (len(results)))
        insert_file_path = os.path.join(data_path, "sonicwall_new_list.txt")
        insert_file_object = open(insert_file_path, 'w')
        insert_file_object.write("%s\t%s\n" % ("alarm_id", "alarm_name"))

        update_file_path = os.path.join(data_path, "sonicwall_update_list.txt")
        update_file_object = open(update_file_path, 'w')
        update_file_object.write("%s\t%s\t%s\n" % ("alarm_id", "old_name", "new_name"))

        for item in results:
            if str(item['id']) in db_signature_details.keys():
                if item['name'] != db_signature_details[item['id']]:
                    update_file_object.write("%s\t%s\t%s\n" % (item['id'], db_signature_details[item['id']], item['name']))
            else:
                insert_file_object.write("%s\t%s\n" % (item['id'], item['name']))

        insert_file_object.close()
        update_file_object.close()
        logger.info("Output file with New Signatures %s successfully generated." % insert_file_path)
        logger.info("Output file with updated Signatures %s successfully generated." % update_file_path)
    except Exception, ex:
        logger.exception(ex)


if __name__ == '__main__':
    main()
