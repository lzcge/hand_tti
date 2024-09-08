import os
import time
from openpyxl import Workbook
import linecache
from common.info_class import InfoClass
from common.search_keyword_enum import SearchKeyword


class File:
    def __init__(self):
        self.file_path_name = ""
        self.info_list = []


