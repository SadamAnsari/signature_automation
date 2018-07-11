#!/usr/bin/python

import requests
import logging
import warnings
from bs4 import BeautifulSoup as bs
from logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
warnings.simplefilter("ignore")


class McaFee(object):

    def __init__(self, revision_number, file_path=None):
        logger.info("Creating instance of %s." % self.__class__.__name__)

        self.url = ""
        self.scrape_url = ""
        self.revision_number = revision_number
        self.file_path = file_path
        self.latest_version = ''
        self.signature_dict = {}

    def scrape_data(self):
        try:
            logger.info("Inside scrape_data function. Scrapping data from url: %s" % self.scrape_url)
        except Exception, ex:
            logger.exception(ex)
            raise Exception("Error caught in scrape_date(%s) function." % self.__class__.__name__)

    def parse_data(self, content):
        pass