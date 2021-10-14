import typing as t


class FileTypeError(Exception):
    filetypes = ["docx", "xlsx"]

    def __init__(self, filetype: str) -> None:
        self.filetype = filetype
        self.message = self.create_message()
        super().__init__(self.message)

    def create_message(self) -> str:
        text1 = f"{self.filetype} is not a excepted file type."
        text2 = "Only excepted file types are {}".format(", ".join(self.filetypes))
        return f"{text1} {text2}"


class TableHandlerError(Exception):
    def __init__(self, message: t.Optional[t.Union[Exception, str]] = None) -> None:
        self.message = (
            "Could not read the content from excel file, either no excel sheet "
            "provided, or it is malformed."
        )
        if message:
            self.message = str(message)
        super().__init__(self.message)


class DocxHandlerError(Exception):
    def __init__(self, message: t.Optional[t.Union[Exception, str]] = None) -> None:
        self.message = "Could not read the content from docx file, either no content in the file or it is malformed."
        if message:
            self.message = str(message)
        super().__init__(self.message)
