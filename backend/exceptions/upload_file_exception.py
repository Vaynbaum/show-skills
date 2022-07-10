class UploadFileException(Exception):
    def __init__(self, message):
        message = message

    def __str__(self):
        return self.message
