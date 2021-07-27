<h1 align="center">
  AsthoUpdater
</h1>
<p align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Made With Python">
    </a>
    <a href="https://github.com/Asthowen/AsthoUpdater">
        <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Use git">
    </a>
    <br>
      <a href="https://github.com/Asthowen/AsthoUpdater">
        <img src="https://img.shields.io/pypi/v/AsthoUpdater?style=for-the-badge" alt="PyPI version">
    </a>
    <a href="https://github.com/Asthowen/AsthoUpdater/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/Asthowen/AsthoUpdater?style=for-the-badge" alt="License">
    </a>
    <a href="https://github.com/Asthowen/AsthoUpdater/stargazers">
        <img src="https://img.shields.io/github/stars/Asthowen/AsthoUpdater?style=for-the-badge" alt="Stars">
    </a>
</p>
<h3 align="center">
    <strong>A lib for update files written in Python.</strong>
</h3>

## Made with
* [**async-timeout**](https://pypi.org/project/async-timeout/)
* [**aiofiles**](https://pypi.org/project/aiofiles/)
* [**aiohttp**](https://pypi.org/project/aiohttp/)

## Install
Execute the command:
```bash
pip3 install AsthoUpdater
```

## Examples
### Simple Update
By default, the verification algorithm is sha512, you can choose another one with the `algorithm` parameter, available: sha256, sha512, crc32, md5. 
If you want to use another one you can contact me.

```python
from astho_updater import AsthoUpdater

async with AsthoUpdater("jsonUrl", "pathToUpdate") as a:
    await a.download()
```

### AsthoUpdater args
```yaml
json_url: Your json url, required (str)
download_path: The download path, required (str)
download_timeout: The timeout to download file, optionnal, 12 at default (int)
overwrite_files: If you want re-download all files, optionnal, False at default (bool)
file_deleter: If you want dl older files, optionnal, False at default (bool)
logger_status: If you want enable/disable the logger, optionnal, True at default (bool)
logger_name: If you want set the logger name, optionnal, 'astho_updater' at default (str)
logger_date_format: If you want set the logger name format, optionnal, '%H:%M:%S - %d/%m/%Y' at default (str)
algorithm: If you want set the used algorithm, optionnal, 'sha512' at default (str)
download_limit: Limit the number of files that can be downloaded simultaneously, optionnal, 10 at default (int)
```

### AsthoUpdater properties
```yaml
get_total_files_to_download: Return total file to download (int)
get_total_files_downloaded: Return total files downloaded (int)
```

### AsthoUpdater json example
```json
{
  "maintenance": "off",
  "files": [
      {
        "checksum": "theChecksum",
        "name": "filename",
        "url": "linkOfFile",
        "path": "pathOfFile"
      },
      {
        "checksum": "theChecksum",
        "name": "filename",
        "url": "linkOfFile",
        "path": "pathOfFile"
      }
  ]
}
```

## Author
[<img width="45" src="https://avatars3.githubusercontent.com/u/59535754?s=400&u=48aecdd175dd2dd8867ae063f1973b64d298220b&v=4" alt="Asthowen">](https://github.com/Asthowen)

## License
**[AsthoUpdater](https://github.com/Asthowen/AsthoUpdater) | [GNU General Public License v3.0](https://github.com/Asthowen/AsthoUpdater/blob/main/LICENSE)**