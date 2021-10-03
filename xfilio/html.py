from .exceptions import FileTypeError


def create_download_link(base64_str: str, filename: str, filetype: str) -> str:
    accepted_type = ["docx", "xlsx"]
    if filetype not in accepted_type:
        raise FileTypeError(filetype=filetype)
    return f'<a href="data:application/octet-stream;base64,{base64_str}" download="{filename}">Click To Download</a>'
