#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
urlextract.py - file with definition of URLExtract class

.. Created on 2016-07-29
.. Licence MIT
.. codeauthor:: Jan Lipovský <janlipovsky@gmail.com>, janlipovsky.cz
.. contributors: Rui Silva
"""
import os
import re
import string
import sys
import urllib2
from datetime import datetime, timedelta

import idna
import uritools

from version import __VERSION__


class URLExtract:
    """
    Class for finding and extracting URLs from given string.

    **Examples:**

    .. code-block:: python

        from urlextract import URLExtract

        extractor = URLExtract()
        urls = extractor.find_urls("Let's have URL janlipovsky.cz as an example.")
        print(urls) # prints: ['janlipovsky.cz']

        # Another way is to get a generator over found URLs in text:
        for url in extractor.gen_urls(example_text):
            print(url) # prints: ['janlipovsky.cz']

        # Or you if you want to just check if there is at least one URL in text you can do:
        if extractor.has_urls(example_text):
            print("Given text contains some URL")
    """
    # file name of cached list of TLDs downloaded from IANA
    _cache_file_name = '.tlds'

    def __init__(self):
        """
        Initialize function for URLExtract class.
        Tries to get cached .tlds, if cached file does not exist it will try to download new list from IANNA
        and save it to users home directory.
        """
        # get directory for cached file
        dir_path = os.path.dirname(__file__)
        if not os.access(dir_path, os.W_OK):
            # get path to home dir
            dir_path = os.path.expanduser('~')

        # full path for cached file with list of TLDs
        self._tld_list_path = os.path.join(dir_path, self._cache_file_name)
        if not os.access(self._tld_list_path, os.F_OK):
            if not self._download_tlds_list():
                sys.exit(-1)

        # check if cached file is readable
        if not os.access(self._tld_list_path, os.R_OK):
            print("ERROR: Cached file is not readable for current user. ({})".format(self._tld_list_path))
            sys.exit(-2)

        # try to update cache file when cache is older than 7 days
        if not self.update_when_older(7):
            print("WARNING: Could not update file, using old version of TLDs list. ({})".format(self._tld_list_path))

        self._tlds = None
        self._tlds_re = None
        self._reload_tlds_from_file()

        self._hostname_re = re.compile("^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])$")

        self.stop_chars = list(string.whitespace) + ['\"', '\'', '<', '>', ';', '@']
        # characters that are allowed to be right after TLD
        self.after_tld_chars = list(string.whitespace) + ['/', '\"', '\'', '<', '?', ':', '.', ',']

    def _reload_tlds_from_file(self):
        """
        Reloads TLDs from file and compile regexp.
        """
        # check if cached file is readable
        if not os.access(self._tld_list_path, os.R_OK):
            print("ERROR: Cached file is not readable for current user. ({})".format(self._tld_list_path))
        else:
            self._tlds = sorted(self._load_cached_tlds(), key=len, reverse=True)
            self._tlds_re = re.compile('|'.join([re.escape(unicode(tld)) for tld in self._tlds]))

    def _download_tlds_list(self):
        """
        Function downloads list of TLDs from IANA 'https://data.iana.org/TLD/tlds-alpha-by-domain.txt'.

        :return: True if list was downloaded, False in case of an error
        :rtype: bool
        """
        url_list = 'https://data.iana.org/TLD/tlds-alpha-by-domain.txt'

        # check if we can write cache file
        if os.access(self._tld_list_path, os.F_OK) and not os.access(self._tld_list_path, os.W_OK):
            print("ERROR: Cache file is not writable for current user. ({})".format(self._tld_list_path))
            return False

        with open(self._tld_list_path, 'w') as ftld:
            try:
                f = urllib2.urlopen(url_list)
                page = f.read().decode('utf-8')
                ftld.write(page)
            except urllib2.HTTPError as e:
                print("ERROR: Can not download list ot TLDs. (HTTPError: {})".format(e.reason))
                return False
            except urllib2.URLError as e:
                print("ERROR: Can not download list ot TLDs. (URLError: {})".format(e.reason))
                return False
        return True

    def _load_cached_tlds(self):
        """
        Loads TLDs from cached file to set.

        :return: Set of current TLDs
        :rtype: set
        """

        list_of_tlds = set()
        with open(self._tld_list_path, 'r') as f:
            for line in f:
                tld = line.strip().lower()
                # skip empty lines
                if len(tld) <= 0:
                    continue
                # skip comments
                if tld[0] == '#':
                    continue

                list_of_tlds.add("." + tld)
                list_of_tlds.add("." + idna.decode(tld))

        return list_of_tlds

    def _get_last_cachefile_modification(self):
        """
        Get last modification of cache file with TLDs.

        :return: Date and time of last modification or None when file does not exist
        :rtype: datetime|None
        """

        try:
            mtime = os.path.getmtime(self._tld_list_path)
        except OSError:
            return None

        return datetime.fromtimestamp(mtime)

    def update(self):
        """
        Update TLD list cache file.

        :return: True if update was successfull False otherwise
        :rtype: bool
        """

        if not self._download_tlds_list():
            return False

        self._reload_tlds_from_file()

        return True

    def update_when_older(self, days):
        """
        Update TLD list cache file if the list is older than number of days given in parameter `days`.

        :param int days: number of days from last change
        :return: True if update was successfull, False otherwise
        :rtype: bool
        """

        last_cache = self._get_last_cachefile_modification()
        if last_cache is None:
            return False

        time_to_update = last_cache + timedelta(days=days)

        if datetime.now() >= time_to_update:
            return self.update()

        return True

    @staticmethod
    def get_version():
        """
        Returns version number.

        :return: version number
        :rtype: str
        """

        return __VERSION__

    def get_after_tld_chars(self):
        """
        Returns list of chars that are allowed after TLD

        :return: list of chars that are allowed after TLD
        :rtype: list
        """

        return self.after_tld_chars

    def set_after_tld_chars(self, after_tld_chars):
        """
        Set chars that are allowed after TLD.

        :param list after_tld_chars: list of characters
        """

        self.after_tld_chars = after_tld_chars

    def get_stop_chars(self):
        """
        Returns list of stop chars.

        :return: list of stop chars
        :rtype: list
        """

        return self.stop_chars

    def set_stop_chars(self, stop_chars):
        """
        Set stop characters used when determining end of URL.

        :param list stop_chars: list of characters
        """

        self.stop_chars = stop_chars

    def _complete_url(self, text, tld_pos):
        """
        Expand string in both sides to match whole URL.

        :param str text: text where we want to find URL
        :param int tld_pos: position of TLD
        :return: returns URL
        :rtype: str
        """

        left_ok = True
        right_ok = True

        max_len = len(text) - 1
        end_pos = tld_pos
        start_pos = tld_pos
        while left_ok or right_ok:
            if left_ok:
                if start_pos <= 0:
                    left_ok = False
                else:
                    if text[start_pos - 1] not in self.stop_chars:
                        start_pos -= 1
                    else:
                        left_ok = False
            if right_ok:
                if end_pos >= max_len:
                    right_ok = False
                else:
                    if text[end_pos + 1] not in self.stop_chars:
                        end_pos += 1
                    else:
                        right_ok = False

        complete_url = text[start_pos:end_pos + 1].lstrip('/')
        if not self._is_domain_valid(complete_url):
            return ""

        return complete_url

    def _validate_tld_match(self, text, matched_tld, tld_pos):
        """
        Validate TLD match - tells if at found position is really TLD.

        :param str text: text where we want to find URLs
        :param str matched_tld: matched TLD
        :param int tld_pos: position of matched TLD
        :return: True if match is valid, False otherwise
        :rtype: bool
        """
        right_tld_pos = tld_pos + len(matched_tld)
        if len(text) > right_tld_pos:
            if text[right_tld_pos] in self.after_tld_chars:
                if tld_pos > 0 and text[tld_pos - 1] not in self.stop_chars:
                    return True
        else:
            if tld_pos > 0 and text[tld_pos - 1] not in self.stop_chars:
                return True

        return False

    def _is_domain_valid(self, url):
        """
        Checks if given URL has valid domain name (ignores subdomains)

        :param str url: complete URL that we want to check
        :return: True if URL is valid, False otherwise
        :rtype: bool

        >>> extractor = URLExtract()
        >>> extractor._is_domain_valid("janlipovsky.cz")
        True

        >>> extractor._is_domain_valid("https://janlipovsky.cz")
        True

        >>> extractor._is_domain_valid("invalid.cz.")
        False

        >>> extractor._is_domain_valid("in.v_alid.cz")
        False

        >>> extractor._is_domain_valid("-is.valid.cz")
        True

        >>> extractor._is_domain_valid("not.valid-.cz")
        False

        >>> extractor._is_domain_valid("http://blog/media/reflect.io.jpg")
        False
        """

        if not url:
            return False

        scheme_pos = url.find('://')
        if scheme_pos != -1:
            url = url[scheme_pos+3:]

        url = 'http://'+url

        url_parts = uritools.urisplit(url)
        # <scheme>://<authority>/<path>?<query>#<fragment>
        host = url_parts.host
        if not host:
            return False

        host_parts = host.split('.')
        if len(host_parts) <= 1:
            return False

        tld = '.'+host_parts[-1]
        if tld not in self._tlds:
            return False

        top = host_parts[-2]

        if self._hostname_re.match(top) is None:
            return False

        return True

    def gen_urls(self, text):
        """
        Creates generator over found URLs in given text.

        :param str text: text where we want to find URLs
        :yields: URL found in text or empty string if no found
        :rtype: str
        """
        tld_pos = 0
        matched_tlds = self._tlds_re.findall(text)

        for tld in matched_tlds:
            tmp_text = text[tld_pos:]
            offset = tld_pos
            tld_pos = tmp_text.find(tld)
            if tld_pos != -1 and self._validate_tld_match(text, tld, offset + tld_pos):
                tmp_url = self._complete_url(text, offset + tld_pos)
                if tmp_url:
                    yield tmp_url

            tld_pos += len(tld) + offset

    def find_urls(self, text, only_unique=False):
        """
        Find all URLs in given text.

        >>> extractor = URLExtract()
        >>> extractor.find_urls("Let's have URL http://janlipovsky.cz as an example.")
        ['http://janlipovsky.cz']

        >>> extractor.find_urls("Let's have text without URLs.")
        []

        >>> extractor.find_urls("Get unique URL from: http://janlipovsky.cz http://janlipovsky.cz", True)
        ['http://janlipovsky.cz']

        >>> extractor.find_urls("Get unique URL from: in.v_alid.cz", True)
        []

        :param str text: text where we want to find URLs
        :param bool only_unique: return only unique URLs
        :return: list of URLs found in text
        :rtype: list
        """
        urls = self.gen_urls(text)
        urls = set(urls) if only_unique else urls
        return list(urls)

    def has_urls(self, text):
        """
        Checks if text contains any valid URL. Returns True if text contains at least one URL.

        >>> extractor = URLExtract()
        >>> extractor.has_urls("Get unique URL from: http://janlipovsky.cz")
        True

        >>> extractor.has_urls("Clean text")
        False

        :param text: text where we want to find URLs
        :return: True if et least one URL was found, False otherwise
        :rtype: bool
        """

        return any(self.gen_urls(text))
