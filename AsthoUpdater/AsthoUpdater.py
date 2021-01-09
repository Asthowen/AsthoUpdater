from urllib import request
import binascii
import json
import time
import os


class AsthoUpdater(object):

    def __init__(self, json_url: str, logger_state: bool = None, logger_name: str = None):
        self.json_url = json_url
        self.logger_state = logger_state
        self.logger_name = logger_name
        self.total_files_to_download = 0
        self.total_files_in_json = 0

        if not logger_name:
            self.logger_name = "AsthoUpdater"

    def start_update(self):
        json_to_download = request.Request(self.json_url, headers={'User-Agent': 'Mozilla/5.0'})
        content = json.loads(request.urlopen(json_to_download).read())

        if content['maintenance'] != "off":
            self.logger("Error", "Maintenance mod activate, I can't download files !")
            return

        for file in content['files']:
            self.total_files_in_json += 1
            if not os.path.isfile(file['path'] + file['name']):
                self.total_files_to_download += 1

        file_number = 1

        for file in content['files']:

            total_path = file['path'] + file['name']

            if not os.path.isfile(total_path) or self.__get_crc_32(total_path) != file['crc32']:
                request.urlretrieve(file['url'], total_path)

                if self.__get_crc_32(file_path=total_path) != file['crc32']:
                    self.logger("Error",
                                f"Error when download file : {file['name']}, the CRC32 is not correct, the CRC32 in JSON is {file['crc32']}, the real CRC32 of download's file is {self.__get_crc_32(file_path=total_path)}, I'm trying to redownload it !")

                    request.urlretrieve(file['url'], file['path'] + file['name'])

                    if self.__get_crc_32(file_path=file['path'] + file['name']) != file['crc32']:
                        self.logger("Fatal Error", f"Same error, download of this file aborted !")
                        os.remove(total_path)
                        self.logger("Fatal Error", f"File removed !")


                    else:
                        self.logger("Log",
                                    f"Downloaded file {file_number}/{self.total_files_to_download} ({file['name']} - {os.path.getsize(file['path'] + file['name']) / (1024 * 1024)} MB)")

                else:
                    self.logger("Log",
                                f"Downloaded file {file_number}/{self.total_files_to_download} ({file['name']} - {os.path.getsize(file['path'] + file['name']) / (1024*1024)} MB)")

                file_number += 1

        self.logger("Log", "Update Finished !")

    @property
    def get_total_files_to_download(self):
        return self.total_files_to_download

    @property
    def get_logger_name(self):
        return self.logger_name

    @property
    def get_logger_state(self):
        return True if self.logger_state is not None else False

    @property
    def get_total_files_in_json(self):
        return self.total_files_in_json

    def logger(self, error_type: str, log: str):
        if self.logger_state is True or self.logger_state is None:
            print(f"[{self.logger_name}] [{time.strftime('%d/%m/20%y - %H:%M:%S')}] [{error_type}] {log}")

    @staticmethod
    def __get_crc_32(file_path: str):
        return str(binascii.crc32(open(file_path, 'rb').read()) & 0xFFFFFFFF)

    def set_logger_state(self, state: bool):
        self.logger_state = state

    def set_logger_name(self, logger_name: str):
        self.logger_name = logger_name

    def set_json_url(self, json_url: str):
        self.json_url = json_url
