#!/usr/bin/python

import re
import requests
import warnings
import logging
from bs4 import BeautifulSoup as bs
from logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
warnings.simplefilter("ignore")


class Snort(object):
    def __init__(self, revision_number, file_path=None):

        logger.info("Creating instance of %s." % self.__class__.__name__)

        self.url = "https://support.sourcefire.com"
        self.scrape_url = "%s/notices/seus" % self.url
        self.revision_number = revision_number
        self.file_path = file_path
        self.latest_version = ''
        self.signature_dict = {}

    def scrape_data(self):
        try:
            logger.info("Inside Snort scrape_data function. Scrapping data from url: %s" % self.scrape_url)
            response = requests.get(self.scrape_url)
            self.latest_version, href_dict = self.parse_data(response.text)
            if self.latest_version and len(href_dict) > 0:
                for key, value in href_dict.iteritems():
                    url = "%s%s" % (self.url, value)
                    result = requests.get(url)
                    soup = bs(result.text)
                    link = soup.select('ul dt a[href]')
                    if link:
                        next_url = "%s%s" % (self.url, link[0]['href'])
                        data = requests.get(next_url)
                        self.signature_dict[key] = self.get_signature_detail(data.text, key)
            if len(self.signature_dict) == 0:
                logger.info("No signatures found.")
            return self.latest_version, self.signature_dict
        except Exception, ex:
            logger.exception(ex)
            raise Exception("Error caught in scrape_data(%s) function." % self.__class__.__name__)

    def get_signature_detail(self, content, name):
        soup = bs(content)
        data_dict = {}
        try:
            logger.info("Inside get_signature_detail function.")
            for table in soup.find_all("table"):
                tr_tag = table.find_all("tr")[2:]
                for tr in tr_tag:
                    td_list = tr.find_all("td")
                    data_dict[td_list[1].text] = td_list[3].text
            logger.info("Total %s signature(s) found for Release %s." % (len(data_dict), name))
            return data_dict
        except Exception, ex:
            logger.exception("Error caught in parse_data function. %s" % ex)
            raise

    def parse_data(self, content):
        soup = bs(content)
        revision_list = []
        href_dict = {}
        try:
            logger.info("Inside parse_data function.")
            for h2_tag in soup.find_all("h2"):
                anchor_tag = h2_tag.find("a")
                match = re.findall('(\d+)', anchor_tag.text)[0]
                revision_list.append(match)
                if int(match) > int(self.revision_number):
                    href_dict[match] = anchor_tag.get("href")
            logger.info("Latest revision information:: Version: %s" % revision_list[0])
            return revision_list[0], href_dict
        except Exception, ex:
            logger.exception("Error caught in parse_data function. %s" % ex)
            raise