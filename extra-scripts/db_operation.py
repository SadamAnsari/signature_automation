#!/usr/bin/python

import sys
import logging
from logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def get_signature_data_from_db(connection_obj, device_type_id):
    try:
        logger.info("Inside get_signature_data_from_db function.")
        query_cursor = connection_obj.cursor()
        query = "select alarmid, name from DEVICETYPEALARMS where DEVICETYPEID=%s" % device_type_id
        logger.info("Query to fetch the signature details from the database: %s " % query)
        response = query_cursor.execute(query)
        logger.info("Successfully got response from database server.")
        query_count = 0
        query_data = {}
        for row in response:
            query_data[row[0]] = str(row[1]).strip()
            query_count += 1
            # if query_count == 500:
            #     break
        logger.info("Preparing result dictionary from database results.")
        query_cursor.close()
        return query_data
    except Exception, ex:
        logger.exception("Exception Caught: %s" % ex)
        sys.exit("Exiting Script.....")