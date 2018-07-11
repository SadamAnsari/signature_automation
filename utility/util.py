#!/usr/bin/python

import os
import csv
import logging
from logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def save_file(file_path, csv_dict, name, version):
    # print "data:============== %s" % csv_dict
    output_file_path = os.path.join(file_path, name)
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)
    check_empty_dict_flag = bool([a for a in csv_dict.values() if a != {}])
    if check_empty_dict_flag:
        try:
            file_path = os.path.join(output_file_path, "%s_%s.csv" % (name, version))
            logger.info("Writing signature details to file %s" % file_path)
            fp_csv = open(file_path, 'w')
            csv_writer = csv.writer(fp_csv, delimiter=',', lineterminator="\n")
            data = ["version", "sign_id", "name"]
            csv_writer.writerow(data)
            for item in csv_dict:
                if len(csv_dict[item]) > 0:
                    for key, value in csv_dict[item].iteritems():
                        csv_writer.writerow([item, key, value])
            fp_csv.close()
            logger.info("Writing to %s file completed successfully." % file_path)
        except IOError, e:
            logger.exception("File I/O error: %s" % e)
        except Exception, ex:
            logger.exception(ex)
            raise Exception(" Error caught in save_file function.")
    return


# def check_for_updates(version, data, file_path, name):
#     check_path = os.path.join(file_path, 'nfxSignatureAutomation', 'signatures')
#     if os.path.isdir(check_path):
#         file_path = os.path.join(check_path, name, "%s_%s.csv" % (name, version))
#         if os.path.isfile(file_path):
#             my_dict = read_last_csv_file(file_path)
#             if version in data.keys():
#                 for key in data[version]:
#                     if key not in my_dict:
#                         data[version][key] = my_dict[key]
#         print len(data[version])


def read_last_csv_file(file_path):
    infile = open(file_path, mode='r')
    reader = infile.readlines()
    mydict = {}
    for row in reader[1:]:
        row_item = row.split(',')
        mydict[row_item[0]] = row_item[1].strip()
    return mydict


def read_from_csv(file_path):
    try:
        csv_file = open(file_path, 'rb')
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        results = []
        for row in csv_reader:
            results.append({header[0]: row[0], header[1]: row[1], header[2]: row[2]})
        return results
    except IOError, e:
        logger.info("Could not read file: I/O error({0}): {1}".format(e.errno, e.strerror))
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Error caught in read_from_csv function.")


def write_to_csv(file_path, data_array):
    try:
        fp_csv = open(file_path, mode='wb')
        csv_writer = csv.writer(fp_csv, delimiter=',', lineterminator="\n")
        data = ["name", "last_version", "latest_version"]
        csv_writer.writerow(data)
        for item in data_array:
            data = [item["name"], item["last_version"], item["latest_version"]]
            csv_writer.writerow(data)
        return
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Error caught in write_to_csv function.")
