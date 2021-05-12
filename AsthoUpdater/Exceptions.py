class JsonNotFound(Exception):
    def __init__(self, json_url: str):
        super().__init__(f"I can't get {json_url}!")
