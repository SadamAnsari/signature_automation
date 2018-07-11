
import sys
import getopt
import csv
import os
import xml.etree.ElementTree as ET
from db_operation import *
from django.utils.encoding import smart_str, smart_unicode


# xml_path = "C:\\Users\\Smit\\Desktop\\nFXSIM-4.1.1-SIGUPD-Snort-v1681.xml"
xml_path = "C:\\Users\\Smit\\Desktop\\nFXSIM-4.1.1-SIGUPD-PALOALTOIPS-v225.xml"
file_name = "C:\\Users\\Smit\\Desktop\\\palo_alto\\threatlist.csv"


def read_from_csv():
    try:
        data_list = {}
        csv_file = open(file_name, 'r')
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


def main():
    try:
        results = read_from_csv()
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
                                help_text.text = results[app_id]['description']
                                # print app_id
                        except Exception, ex:
                            print app_id
                            print ex

        tree.write("nFXSIM-4.1.1-SIGUPD-PALOALTOIPS-v225.xml")

    except Exception, ex:
        print(ex)

if __name__ == '__main__':
    main()