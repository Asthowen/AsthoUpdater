import requests
import binascii
import json
import time
import os


class Constants(enumerate):
    HEADERS = {'User-Agent': 'Mozilla/5.0'}


class AsthoUpdater(object):

    def __init__(
            self,
            json_url: str,
            logger_state: bool = None,
            logger_name: str = None
    ):
        self.json_url = json_url
        self.logger_state = True if logger_state is None else logger_state
        self.logger_name = "AsthoUpdater" if logger_name is None else logger_name

        self.total_files_to_download = 0
        self.total_files_in_json = 0

    def start_update(self):
        content = json.loads(requests.get(self.json_url, headers=Constants.HEADERS).content)

        if content['maintenance'] != "off":
            self.logger("ERROR", "Maintenance mod activate, I can't download files!")
            return

        for file in content['files']:
            self.total_files_in_json += 1
            if not os.path.isfile(file['path'] + file['name']):
                self.total_files_to_download += 1

        file_number = 1

        for file in content['files']:

            total_path = file['path'] + file['name']

            if not os.path.isfile(total_path) or self.__get_crc_32(total_path) != file['crc32']:
                with open(file['path'] + file['name'], 'wb') as f:
                    f.write(requests.get(file['url'], allow_redirects=True, headers=Constants.HEADERS).content)

                if self.__get_crc_32(file_path=total_path) != file['crc32']:
                    self.logger("ERROR",
                                f"Error when download file: {file['name']}, the CRC32 is not correct, I'm trying to re-download it!")

                    with open(file['path'] + file['name'], 'wb') as f:
                        f.write(requests.get(file['url'], allow_redirects=True, headers=Constants.HEADERS).content)

                    if self.__get_crc_32(file_path=file['path'] + file['name']) != file['crc32']:
                        self.logger("ERROR", f"Same error, download of this file aborted!")
                        os.remove(total_path)
                        self.logger("ERROR", f"File removed!")
                    else:
                        self.logger("LOG",
                                    f"Downloaded file {file_number}/{self.total_files_to_download} ({file['name']} - {os.path.getsize(file['path'] + file['name']) / (1024 * 1024)} MB)")

                else:
                    self.logger("LOG",
                                f"Downloaded file {file_number}/{self.total_files_to_download} ({file['name']} - {round(os.path.getsize(file['path'] + file['name']) / (1024 * 1024), 3)} MB)")

                file_number += 1

        self.logger("LOG", "Update Finished!")

    @property
    def get_total_files_to_download(self) -> int:
        return self.total_files_to_download

    @property
    def get_logger_name(self) -> str:
        return self.logger_name

    @property
    def get_logger_state(self) -> bool:
        return self.logger_state

    @property
    def get_total_files_in_json(self) -> int:
        return self.total_files_in_json

    def logger(self, error_type: str, log: str):
        if self.logger_state:
            print(f"[{self.logger_name}] [{time.strftime('%d/%m/%Y - %H:%M:%S')}] [{error_type}] {log}")

    @staticmethod
    def __get_crc_32(file_path: str) -> str:
        return str(binascii.crc32(open(file_path, 'rb').read()) & 0xFFFFFFFF)

    def set_logger_state(self, state: bool):
        self.logger_state = state

    def set_logger_name(self, logger_name: str):
        self.logger_name = logger_name

    def set_json_url(self, json_url: str):
        self.json_url = json_url
