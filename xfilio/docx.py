from __future__ import annotations

import base64
import io
import os
import typing as t
from io import BytesIO

from docx import Document as read_document
from docx.document import Document

from exception.fileio import DocxHandlerError
from xfilio.html import create_download_link


def python_docx_to_byte(doc: Document) -> bytes:
    """
    Convert a Python Docx file into byte
    :param doc: Python Document type from Docx
    :return: Bytes of Document
    """
    byte_stream = BytesIO()
    doc.save(byte_stream)
    byte_stream.seek(0)
    return byte_stream.read()


class DocxHandler:
    def __init__(self, document: Document, name: str) -> None:
        """
        Handle all the conversion to and from document file
        :param document: A docx file like object
        """
        self.document = document
        self.name = name

    def __len__(self) -> int:
        """Determine if there is any table in the docx or not"""
        return len([table for table in self.document.tables])

    def get_stat(self) -> t.Dict:
        total_tables = self.__len__()
        total_paragraphs = len([paragraph for paragraph in self.document.paragraphs])
        return {"tables": total_tables, "paragraphs": total_paragraphs}

    def to_byte(self) -> bytes:
        """
        Convert a Python Docx file into byte
        :param doc: Python Document type from Docx
        :return: Bytes of Document
        """
        byte_stream = BytesIO()
        self.document.save(byte_stream)
        byte_stream.seek(0)
        return byte_stream.read()

    def to_base64_str(self) -> str:
        """
        Convert bytes data to base64
        :param byte_data: data as byte
        :return: base 64 encoded string of the byte data
        """
        byte_data = self.to_byte()
        b64_encoded_str = base64.b64encode(byte_data).decode("utf-8")
        return b64_encoded_str

    @classmethod
    def from_base64(cls, b64_str: str, filename: t.Optional[str] = None) -> DocxHandler:
        """
        Create a instance of DocxHandler from base64 encoded string
        :return: a DocxHandler object
        """
        bytes_stream = base64.b64decode(b64_str.encode("utf-8"))
        document = read_document(io.BytesIO(bytes_stream))
        if filename:
            return cls(document=document, name=filename)
        return cls(document=document, name="document")

    def write_to_local(self, path: str, filename: str) -> None:
        full_path = os.path.join(path, filename)
        self.document.save(full_path)

    @classmethod
    def from_file_like(cls, content: t.Union[t.TextIO, t.BinaryIO]) -> DocxHandler:
        """
        Create itself from a file like object from streamlit
        """
        try:
            document = read_document(content)
            return cls(document=document, name=content.name)

        except DocxHandlerError:
            raise DocxHandlerError
        except Exception as e:
            print(e)
            raise DocxHandlerError

    def create_download_link(self, filename: str) -> str:
        content = self.to_base64_str()
        return create_download_link(base64_str=content, filename=filename, filetype="docx")





