# coding: utf-8
from urllib.request import urlopen, urlretrieve
from bs4 import beautifulsoup4
import re
import os

headers = {                                         #伪装浏览器
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                 ' Chrome/32.0.1700.76 Safari/537.36'
}