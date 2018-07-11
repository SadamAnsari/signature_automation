#!/usr/bin/python

import os
import platform
import logging
from logger import LOGGER_NAME
from selenium import webdriver
from bs4 import BeautifulSoup

logger = logging.getLogger(LOGGER_NAME)


class JavascriptScrapper(object):
    def __init__(self, path, url):
        logger.info("Creating instance of %s. " % self.__class__.__name__)
        self.path = path
        self.url = url

    def get_path(self):
        # print platform.architecture()
        if platform.system() == 'Windows':
            PHANTOMJS_PATH = '%s/phantomjs/phantomjs.exe' % self.path
        else:
            PHANTOMJS_PATH = '%s/phantomjs/bin/phantomjs' % self.path
        return PHANTOMJS_PATH

    def get_dynamic_data(self):
        try:
            browser = webdriver.PhantomJS(executable_path=self.get_path(), service_log_path=os.path.devnull)
            browser.get(self.url)
            html_source = browser.page_source
            browser.quit()
            soup = BeautifulSoup(html_source, "html.parser")
            content = soup.find_all('div', {'id': 'grid-example'})
            # print content
            return content

        except Exception, ex:
            logger.exception(ex)
