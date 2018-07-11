#!/usr/bin/python

import logging
import warnings
from bs4 import BeautifulSoup as bs
from nfxSignatureAutomation.javascriptScrapper import JavascriptScrapper
from logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
warnings.simplefilter("ignore")


class CiscoIPS(object):
    def __init__(self, revision_number, file_path=None):
        logger.info("Creating instance of %s." % self.__class__.__name__)

        self.url = "https://tools.cisco.com"
        self.scrape_url = "%s/security/center/ipshome.x" % self.url
        self.revision_number = revision_number
        self.signature_dict = {}
        self.html_content = JavascriptScrapper(path=file_path, url=self.scrape_url).get_dynamic_data()

    def scrape_data(self):
        try:
            logger.info("Inside scrape_data function. Scrapping data from url: %s" % self.scrape_url)
            soup = bs(str(self.html_content))
            main_div_tag = soup.find("div", id="grid-example")
            div_tag = main_div_tag.find("div", class_="x-grid3-body")
            table = div_tag.find_all("table")
            versions = []
            for tr_tag in table:
                td = tr_tag.find_all("td")
                sign_id = td[0].text.split('/')[0]
                sign_name = td[1].text
                release_version = td[4].text
                versions.append(release_version)
                if release_version > str(self.revision_number):
                    if release_version not in self.signature_dict.keys():
                        self.signature_dict[release_version] = {}
                    self.signature_dict[release_version][sign_id] = sign_name
            if versions[0] != str(self.revision_number):
                self.revision_number = versions[0]
            logger.info("Latest revision information:: Version: %s" % self.revision_number)
            if len(self.signature_dict) == 0:
                logger.info("No signatures found.")
            else:
                for item in self.signature_dict:
                    logger.info("Total %s signature(s) found for Release %s." % (len(self.signature_dict[item]), item))
            return self.revision_number, self.signature_dict

        except Exception, ex:
            logger.exception(ex)
            raise Exception("Error caught in scrape_data(%s) function." % self.__class__.__name__)

#instance = CiscoIPS('S975', "root/Sadam/SignatureAutomation")
#instance.scrape_data()
