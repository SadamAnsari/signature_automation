#!/usr/bin/python

import re
import sys
import os
import logging
import getopt

from logger import setup_logging, LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

# <br>&nbsp;<b id=2>New Filters: <br></b><br>&nbsp;&nbsp;&nbsp;
# <br>&nbsp;<b id=2>New Filters:</b><br><br>&nbsp;&nbsp;&nbsp;
# pattern = re.compile(r'&nbsp;<b id=2>New Filters:.*&nbsp;\s*<b id=3>', re.I | re.M)
# pattern = re.compile(r'&nbsp;New Filters:.*&nbsp;\s*<b id=3>', re.I | re.M)
pattern = re.compile(r'(?:&nbsp;<b id=2>New Filters|&nbsp;New Filters):.*&nbsp;\s*<b id=3>', re.I | re.M)


def main(root_path, file_name):
    data_path = os.path.join(root_path, "TPTI_DV")
    setup_logging(logfile="TPTI_DV_Signature.log", scrnlog=True)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    try:
        file_object = open(file_name, 'r')
        logger.info("Reading %s file started." % file_name)
        html_text = file_object.read()
        logger.info("Reading of %s file completed." % file_name)
        html_text = "".join(html_text.split('\n'))
        # print html_text
        result = pattern.findall(html_text)
        # print result
        output_file = "%s.txt" % os.path.splitext(os.path.os.path.basename(file_name))[0]
        output_file_path = os.path.join(data_path, output_file)
        logger.info("Opening %s file for writing signature details." % output_file_path)
        output_file_object = open(output_file_path, 'w')
        output_file_object.write("%s,%s,%s,%s\n" % ("sign_id", "alarm_name", "alarm_desc", "CV_Exposures"))
        if result:
            text = "".join(result[0].replace('&nbsp;', ""))
            text = text.replace("<b id=2>New Filters: <br></b><br> ", "")
            text = text.replace("<b id=2>New Filters:</b><br><br> ", "").replace("<br><br> <b id=3>", "")
            text_element = text.split('<br><br>')
            logger.info("Total %s signatures found from %s file." %
                        (len(text_element), os.path.os.path.basename(file_name)))
            # print text_element
            for item in text_element:
                pattern1 = re.findall("(\d+: [^\<]*)", item, re.M | re.I)
                pattern2 = re.findall("(Description: [^\<]*)", item, re.M | re.I)
                pattern3 = re.findall("(Common Vulnerabilities andExposures: [^\<]*)", item, re.M | re.I)
                if pattern1 and pattern2 and pattern3:
                    sign_info = pattern1[0].split(":", 1)
                    description = pattern2[0].split(":", 1)[1]
                    cv_exposure = pattern3[0].split(":", 1)[1]
                else:
                    sign_info = pattern1[0].split(":", 1)
                    description = pattern2[0].split(":", 1)[1]
                    cv_exposure = ""
                output_file_object.write("%s,%s,%s,%s\n" % (sign_info[0].strip(), sign_info[1].strip(),
                                                            description.strip(), cv_exposure.strip()))
        output_file_object.close()
        logger.info("Output file %s successfully generated." % output_file_path)
    except Exception, ex:
        print (ex)
        logger.exception("Exception caught: %s" % ex)


def usage():
    print ("%s -f <FILE NAME>" % __file__)
    sys.exit(1)


if __name__ == '__main__':
    file_name = None
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:", ["File_Name=", "help"])
    except getopt.GetoptError:
        usage()
    if len(opts) <= 0:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-f", "--File_Name"):
            file_name = arg.strip()
    main(path, file_name)
