import sys
import getopt
import csv
import os
import xml.etree.ElementTree as ET
from db_operation import *


def read_from_csv(file_path):
    try:
        data_list = {}
        csv_file = open(file_path, 'rb')
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            sign_id = str(row[0])
            data_list[sign_id] = dict(name=row[1], description=row[2])
        return data_list
    except IOError, e:
        print("Could not read file: I/O error({0}): {1}".format(e.errno, e.strerror))
    except Exception, ex:
        print(ex)
        raise Exception("Error caught in read_from_csv function.")


def main(path, xml, csv_file):
    try:
        print root_path
        print csv_path
        results = read_from_csv(file_path=csv_file)
        print("Total %s records fetched from the csv file." % (len(results)))
        tree = ET.ElementTree(file=xml_path)
        root = tree.getroot()
        for child_root in root:
            for child in child_root:
                for element in child:
                    if 'appId' in element.attrib:
                        app_id = element.attrib['appId']
                        try:
                            if app_id in results.keys():
                                help_type, help_text = element.find('helpType'), element.find('helpText')
                                help_type.text = 'TXT'
                                help_text.text = str(results[app_id]['description'].decode('utf-8'))
                                # print app_id
                        except Exception, ex:
                            print ex
                            # sys.exit("Exception caught. Script Exiting....")
        tree.write(os.path.join(root_path, os.path.basename(xml_path)))
    except Exception, ex:
        print(ex)


def usage():
    print ("%s -x <XML File Path> -c  <CSV File Path>" % __file__)
    sys.exit(1)

if __name__ == '__main__':
    root_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_path)
    xml_path = ""
    csv_path = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hx:c:", ["xml_path=", "csv_path="])
    except getopt.GetoptError:
        usage()
    if len(opts) <= 0:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-x", "--xml_path"):
            xml_path = arg.strip()
        elif opt in ("-c", "--csv_path"):
            csv_path = arg.strip()
    main(path=root_path, xml=xml_path, csv_file=csv_path)