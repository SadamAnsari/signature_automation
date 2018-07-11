#!/usr/bin/python
import os
import sys
import logging
import datetime
from logger import setup_logging, LOGGER_NAME

from nfxSignatureAutomation.content.snort import Snort
from nfxSignatureAutomation.content.juniper import Juniper
from nfxSignatureAutomation.content.fortiguard import FortiGuard
from nfxSignatureAutomation.content.cisco import CiscoIPS
from nfxSignatureAutomation.content.mcafee import McaFee
from utility import *

logger = logging.getLogger(LOGGER_NAME)

main_map = dict(snort=Snort,
                juniper=Juniper,
                cisco=CiscoIPS,
                fortiguard=FortiGuard,
                mcafee=McaFee)


def main():
    root_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_path)
    date_formatter = datetime.datetime.now().strftime("%d-%m-%Y")
    files_path = os.path.join(root_path, "data", "Signatures", date_formatter)
    if not os.path.exists(files_path):
        os.makedirs(files_path)
    setup_logging(logdir=os.path.join(root_path, "data", "logs"), logfile="signature_details.log", scrnlog=True)
    csv_file_name = "products.csv"
    product_list = read_from_csv(csv_file_name)
    # print product_list
    data_list = []
    try:
        for item in product_list:
            if item['name'] in main_map.keys():
                class_instance = main_map[item['name']](revision_number=item['latest_version'], file_path=root_path)
                latest_version, data = class_instance.scrape_data()
                if latest_version != item['latest_version']:
                    save_file(file_path=files_path, csv_dict=data, name=item['name'], version=latest_version)
                    data_list.append(dict(name=item['name'], last_version=item['latest_version'], latest_version=latest_version))
                else:
                    data_list.append(dict(name=item['name'], last_version=item['last_version'], latest_version=item['latest_version']))
        write_to_csv(file_path=csv_file_name, data_array=data_list)
        print("SignatureAutomation script completed successfully.")
    except Exception, ex:
        logger.exception(ex)
        sys.exit()

if __name__ == '__main__':
    main()
