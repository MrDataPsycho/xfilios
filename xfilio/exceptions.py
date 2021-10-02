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
    def __init__(self, message=None) -> None:  # type: ignore
        self.message = "Could not read the content from excel file, either no excel sheet provided, or it is malformed."
        if message:
            self.message = message
        super().__init__(self.message)


class DocxHandlerError(Exception):
    def __init__(self, message=None) -> None:  # type: ignore
        self.message = "Could not read the content from decx file, either no tables in the file or it is malformed."
        if message:
            self.message = message
        super().__init__(self.message)

