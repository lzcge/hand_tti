
class File:
    def __init__(self):
        self._file_path_name = ""
        self._info_list = []

    @property
    def file_path_name(self):
        return self._file_path_name

    @file_path_name.setter
    def file_path_name(self, value):
        self._file_path_name = value

    @property
    def info_list(self):
        return self._info_list

    @info_list.setter
    def info_list(self, value):
        self._info_list = value
