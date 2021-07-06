from AsthoUpdater.Exceptions import JsonNotFound
from AsthoUpdater.Logger import Logger
import async_timeout
import aiofiles
import binascii
import hashlib
import aiohttp
import asyncio
import os


class AsthoUpdater(object):
    def __init__(
            self,
            json_url: str,
            download_path: str,
            download_timeout: int = 12,
            overwrite_files: bool = False,
            file_deleter: bool = False,
            logger_status: bool = True,
            logger_name: str = None,
            algorithm: str = 'sha512',
            download_limit: int = 10
    ):
        self.__json_url = json_url
        self.__download_path = download_path if download_path[-1] == os.sep else download_path + os.sep
        self.__logger = Logger(logger_name, logger_status)
        self.__download_timeout = download_timeout
        self.__overwrite_files = overwrite_files
        self.__file_deleter = file_deleter
        self.__algorithm = algorithm
        self.__download_limit = download_limit

        self.__json_content = dict
        self.__client_session = aiohttp.ClientSession()

        self.__file_to_download = 0
        self.__file_downloaded = 0

    async def __aenter__(self) -> object:
        return self

    async def __aexit__(self, *args) -> bool:
        return await self.close()

    async def __get_hash(self, file_path: str) -> str:
        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()

            if self.__algorithm == 'sha256':
                return hashlib.sha256(content).hexdigest()
            elif self.__algorithm == 'sha512':
                return str(hashlib.sha512(content).hexdigest())
            elif self.__algorithm == 'crc32':
                return str(binascii.crc32(content) & 0xFFFFFFFF)
            elif self.__algorithm == 'md5':
                return str(hashlib.md5(content).hexdigest())

    @staticmethod
    async def __limit_tasks(
            number: int,
            *tasks
    ):
        semaphore = asyncio.Semaphore(number)

        async def sem_task(task):
            async with semaphore:
                return await task

        return await asyncio.gather(*(sem_task(task) for task in tasks))

    async def get_all_files(self):
        async with self.__client_session.get(self.__json_url) as r:
            if r.status == 200:
                self.__json_content = await r.json()
                return self.__json_content
            else:
                raise JsonNotFound(self.__json_url)

    async def __download_file(self, url):
        if self.__overwrite_files or os.path.isfile(self.__download_path + url['name']) is False:
            async with async_timeout.timeout(self.__download_timeout):
                async with self.__client_session.get(url['url']) as r:
                    async with aiofiles.open(self.__download_path + url['name'], 'wb') as f:
                        async for data in r.content.iter_chunked(1024):
                            await f.write(data)
                    try:
                        file_hash = await self.__get_hash(self.__download_path + url['name'])

                        if file_hash == url[self.__algorithm]:
                            self.__file_downloaded += 1
                            self.__logger.log(f"File {url['name']} at {url['url']} has been downloaded.")
                        else:
                            self.__logger.log(
                                f"File {url['name']} at {url['url']} has been downloaded but {self.__algorithm} is not valid."
                            )
                            os.remove(self.__download_path + url['name'])
                    except KeyError:
                        raise self.__logger.error("The hash algorithm specified isn't the one present in the json.")

    async def download(self):
        await self.get_all_files()

        self.__file_to_download = len(self.__json_content['files'])

        if self.__file_to_download > 1:
            if self.__json_content['maintenance'] != 'on':
                self.__logger.log('Start to download.')

                await self.__limit_tasks(
                    self.__download_limit,
                    *[self.__download_file(element) for element in self.__json_content['files']]
                )

                if self.__file_downloaded:
                    self.__logger.log('All files has been downloaded.')
                else:
                    self.__logger.log('No files to re-download.')
            else:
                self.__logger.warn('Maintenance mode activated.')
        else:
            self.__logger.log('No files to download.')

        if self.__file_deleter:
            await self.file_deleter()

    async def file_deleter(self):
        file_list = [
            self.__download_path + x['path'] + x['name'] if x['path'] != '/' else self.__download_path + x['name'] for x
            in self.__json_content['files']
        ]

        for r, d, f in os.walk(self.__download_path):
            for file in f:
                if os.path.join(r, file) not in file_list:
                    os.remove(os.path.join(r, file))

    async def close(self) -> bool:
        if self.__client_session is not None:
            await self.__client_session.close()
            return True
        else:
            return False

    @property
    def get_total_files_to_download(self) -> int:
        return self.__file_to_download

    @property
    def get_total_files_downloaded(self) -> int:
        return self.__file_downloaded
