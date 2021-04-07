# AsthoUpdater
A useful lib for download files.

## Install prerequisites
* Execute command : ```python3 -m pip install AsthoUpdater```

## Examples
**Simple Update :**
```python
from AsthoUpdater import AsthoUpdater

updater = AsthoUpdater(json_url='yourJsonUrl')
updater.start_update()
```

**AsthoUpdater args :**
```
json_url : Your json url, required (string)
logger_state : Logger state, default True, optional (string)
logger_name : The logger name, default AsthoUpdater, optional (string)
```

**AsthoUpdater properties :**
```
get_total_files_to_download : Return total file to download (int)
get_logger_name : Return logger name (string)
get_logger_state : Return logger state (boolean)
get_total_files_in_json : Return total file in json file (int)
```

**AsthoUpdater setters :**
```
set_logger_state : Set logger state (boolean)
set_logger_name : Set logger name (string)
set_json_url : Set json url (string)
```

**AsthoUpdater json example :**
```json
{
  "maintenance": "off",
  "files": [
      {
        "crc32": "theCrc32",
        "name": "filename",
        "url": "linkOfFile",
        "path": "pathOfFile"
      },
      {
        "crc32": "theCrc32",
        "name": "filename",
        "url": "linkOfFile",
        "path": "pathOfFile"
      }
  ]
}
```

## Author
[<img width="64" src="https://avatars3.githubusercontent.com/u/59535754?s=400&u=48aecdd175dd2dd8867ae063f1973b64d298220b&v=4" alt="Asthowen">](https://github.com/Asthowen)

## License
**[AsthoUpdater](https://github.com/Asthowen/AsthoUpdater) | [Mozilla Public License 2.0](https://github.com/Asthowen/AsthoUpdater/blob/main/LICENSE)**