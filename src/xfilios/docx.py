from __future__ import annotations

import base64
import io
import os
import typing as t
from io import BytesIO

from docx import Document as ReadDocFunc
from docx.document import Document

from .exceptions import DocxHandlerError
from .handler import Handler
from .html import create_download_link


class DocxHandler(Handler):
    def __init__(self, document: Document, name: str) -> None:
        """
        Handle all the conversion to and from document file
        :param document: A docx file like object
        """
        self.document = document
        self.name = name

    def get_stat(self) -> t.Dict:
        total_tables = len([table for table in self.document.tables])
        total_paragraphs = self.__len__()
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
        document = ReadDocFunc(io.BytesIO(bytes_stream))
        if filename:
            return cls(document=document, name=filename)
        return cls(document=document, name="document")

    def write_to_local(self, path: str, filename: str) -> None:
        full_path = os.path.join(path, filename)
        self.document.save(full_path)

    @classmethod
    def from_file_like(cls, content: t.Union[t.TextIO, t.BinaryIO]) -> DocxHandler:
        """
        Create itself from a file like object from framework like Streamlit/Dash
        """

        try:
            document = ReadDocFunc(content)
            return cls(document=document, name=content.name)

        except DocxHandlerError:
            raise DocxHandlerError
        except Exception as e:
            raise e

    def create_download_link(self, filename: str) -> str:
        """
        Create a html annotated tag to show in the front end
        :param filename: Name of the File when downloaded
        :return: Html anchor tag annotated String
        """

        content = self.to_base64_str()
        return create_download_link(
            base64_str=content, filename=filename, filetype="docx"
        )

    def __str__(self) -> str:
        """String representation of the class"""
        return f'{self.__class__.__name__}(document="...", name={self.name})'

    def __repr__(self):
        raise NotImplementedError

    def __len__(self) -> int:
        """Determine if there is any table in the docx or not"""
        return len(
            [para for para in self.document.paragraphs if len(para.text.strip()) > 0]
        )
