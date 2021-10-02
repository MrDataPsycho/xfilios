from global_utils import collect_utc_now


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


def create_download_link(base64_str: str, filename: str, filetype: str) -> str:
    accepted_type = ["docx", "xlsx"]
    if filetype not in accepted_type:
        raise FileTypeError(filetype=filetype)
    # file_suffix = collect_utc_now()
    # file_suffix = file_suffix.replace(":", "-")
    # file_name = f"{filename}_{file_suffix}.{filetype}"
    return f'<a href="data:application/octet-stream;base64,{base64_str}" download="{filename}">Click To Download</a>'
