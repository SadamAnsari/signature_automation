#!/usr/bin/python
import re
import requests
import logging
import warnings
from bs4 import BeautifulSoup as bs
from logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
warnings.simplefilter("ignore")


class Juniper(object):

    def __init__(self, revision_number, file_path=None):
        logger.info("Creating instance of %s." % self.__class__.__name__)
        self.url = "http://rss.juniper.net"
        self.scrape_url = "%s/f/100001s3n1db7dccla3.rss" % self.url
        self.revision_number = revision_number
        self.file_path = file_path
        self.latest_version = ''
        self.signature_dict = {}

    def scrape_data(self):
        try:
            logger.info("Inside scrape_data function. Scrapping data from url: %s" % self.scrape_url)
            # print self.scrape_url
            response = requests.get(self.scrape_url)
            self.latest_version, href_dict = self.parse_data(response.text)
            for item in href_dict:
                # print href_dict[item]
                result = requests.get(href_dict[item])
                self.signature_dict[item] = self.get_signature_detail(result.text, item)
            if len(self.signature_dict) == 0:
                logger.info("No Signature records found.")
            return self.latest_version, self.signature_dict
        except Exception, ex:
            logger.exception(ex)
            raise Exception("Error caught in scrape_data(%s) function." % self.__class__.__name__)

    def get_signature_detail(self, content, name):
        try:
            logger.info("Inside get_signature_detail. Fetching Signature ID and description.")
            soup = bs(content)
            data_dict = {}
            for element in soup.find_all('div', class_='scmDefault clear'):
                for p_tag in element.find_all("p"):
                    # print p_tag.text
                    if "new signatures:" in p_tag.text or 'new signature:' in p_tag.text:
                        table = p_tag.find_next("table")
                        tr_tag = table.find_all("tr")
                        for tr in tr_tag:
                            td_list = tr.find_all("td")
                            data_dict[td_list[1].text] = td_list[2].text
                        break
            logger.info("Total %s signature(s) found for Version %s." % (len(data_dict), name))
            return data_dict
        except Exception, ex:
            logger.exception("Error caught in get_signature_detail function. %s" % ex)
            raise

    def parse_data(self, content):
        try:
            logger.info("Inside parse_data function.")
            tmp_dict = {}
            version_list = []
            soup_content = bs(content)
            item_tag = soup_content.find_all("item")
            for item in item_tag:
                soup_item = bs(str(item))
                url_info = soup_item.find("simplefeed:itempath")
                url_text = url_info.text.replace("rssin:", "")
                if url_text:
                    update_version = re.findall("(\d+)", url_text)[0]
                    if int(update_version) > int(self.revision_number):
                        version_list.append(update_version)
                        tmp_dict[update_version] = url_text
            if version_list:
                self.revision_number = version_list[0]
            logger.info("Latest revision information:: Version: %s" % self.revision_number)
            return self.revision_number, tmp_dict
        except Exception, ex:
            logger.exception("Error caught in parse_data function. %s" % ex)
            raise

    def parse_data_old(self):  # DO NOT USE THIS FUNCTION: FOR REFERENCE ONLY
        try:
            scrape_url = "http://www.juniper.net/us/en/security/#tab=dtabs-1"
            logger.info("Inside parse_data function. url :: %s " % scrape_url)
            response = requests.get(scrape_url)
            logger.info("Inside parse_data function.")
            soup_iframe = bs(response.text)
            iframe_src = soup_iframe.find_all('iframe')[1].attrs['src']
            url = "%s%s" % (self.url, iframe_src)
            result = requests.get(url)
            soup_table = bs(result.text)
            table = soup_table.find("table")
            tr_tag = table.find_all("tr")[1:]
            tmp_dict = {}
            version_list = []
            for tr in tr_tag:
                td_tag = tr.find_all("td")
                if 'new signature:' in td_tag[1].text.strip() or 'new signature:' in td_tag[1].text.strip():
                    anchor_tag = td_tag[0].select("a[href]")[0]
                    update_version = anchor_tag.text.replace("#", "")
                    if int(update_version) > int(self.revision_number):
                        version_list.append(update_version)
                        tmp_dict[update_version] = anchor_tag.get("href")
            if version_list:
                self.revision_number = version_list[0]
            logger.info("Latest revision information:: Version: %s" % self.revision_number)
            return self.revision_number, tmp_dict
        except Exception, ex:
            logger.exception("Error caught in parse_data function. %s" % ex)
            raise
#
# instance = Juniper(2841)
# instance.scrape_data()