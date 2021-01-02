class InvalidConfig(Exception):
    file: str
    message: str

    def __init__(self, message, file=None):
        self.file = file
        self.message = message

    def __str___(self):
        return f"Invalid config: {self.message} in {self.file or '[unknown]'} file"
