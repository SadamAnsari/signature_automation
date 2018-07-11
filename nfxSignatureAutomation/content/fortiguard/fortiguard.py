#!/usr/bin/python

import time
import requests
import logging
import warnings
from bs4 import BeautifulSoup as bs
from logger import LOGGER_NAME


logger = logging.getLogger(LOGGER_NAME)
warnings.simplefilter("ignore")


class FortiGuard(object):
    def __init__(self, revision_number, file_path=None):
        logger.info("Creating instance of %s." % self.__class__.__name__)

        self.url = "http://www.fortiguard.com"
        self.scrape_url = "%s/updates/ips" % self.url
        self.revision_number = revision_number.replace("_", '.')
        self.latest_version = ''
        self.signature_dict = {}

    def get_url(self, version):
        return "%s?version=%s" % (self.scrape_url, version)

    def scrape_data(self):
        try:
            logger.info("Inside scrape_data function. Scrapping data from url: %s" % self.scrape_url)
            response = requests.get(self.scrape_url)
            self.latest_version, parse_dict = self.parse_data(response.text)
            for item in parse_dict:
                url = self.get_url(item)
                result = requests.get(url)
                self.signature_dict[item] = self.get_signature_detail(result.text, item)
                time.sleep(0.1)
            if len(self.signature_dict) == 0:
                logger.info("No signature found.")
            return self.latest_version.replace(".", "_"), self.signature_dict
        except Exception, ex:
            logger.exception(ex)
            raise Exception("Error caught in scrape_data(%s) function." % self.__class__.__name__)

    def get_signature_detail(self, content, name):
        soup = bs(content)
        data_dict = {}
        try:
            logger.info("Inside get_signature_detail function.")
            table_tag = soup.find("table", class_="table ")
            tr_tag = table_tag.find_all("tr")
            for tr in tr_tag[1:]:
                td = tr.find_all("td")
                if td[1].text.strip().lower() == "add":
                    sign_href = td[0].find("a").get("href")
                    sign_id = sign_href.split('/')[-1]
                    data_dict[sign_id] = td[0].text.strip()
            logger.info("Total %s Signatures found for version %s" % (len(data_dict), name))
            return data_dict
        except Exception, ex:
            logger.exception("Error caught in parse_data function. %s" % ex)
            raise

    def parse_data(self, content):
        try:
            logger.info("Inside parse_data function.")
            soup = bs(content)
            ul_list = soup.find("ul", class_="updateversions")
            a_tag_list = ul_list.find_all("a")
            href_dict = {}
            version_list = []
            for anchor_tag in a_tag_list:
                version_id = anchor_tag.text.strip()
                version_list.append(version_id)
                if version_id > self.revision_number:
                    href_dict[version_id] = anchor_tag.get("href")
            if self.revision_number != str(version_list[0]):
                self.revision_number = version_list[0]
            logger.info("Latest revision information:: Version: %s" % self.revision_number)
            return self.revision_number, href_dict
        except Exception, ex:
            logger.exception(ex)


# instance = FortiGuard('10.122')
# instance.scrape_data()