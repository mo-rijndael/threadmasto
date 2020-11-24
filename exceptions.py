class InvalidConfig(Exception):
    file: str
    message: str

    def __init__(self, message, file="[unknown]"):
        self.file = file
        self.message = message

    def __str___(self):
        return f"Invalid config: {self.message} in {self.file} file"
