from __future__ import annotations

import base64
import io
import typing as t

import pandas as pd

from .handler import Handler
from .html import create_download_link
from .table import TableHandler


class ExcelHandler(Handler):
    """Excel handler to create downloadable excel file using Excel Writer"""

    def __init__(self, tables: t.List[TableHandler]):
        """
        Excel Handler objects init
        :param tables: list of TableHandler instances to convert into Excel downloadable link
        """
        self.tables = tables

    @classmethod
    def from_table_handlers(cls, *args: TableHandler) -> ExcelHandler:
        """
        Create ExcelHandler from list of table Handlers
        :param args: List of TableHandler Object
        :return: Instance of Type ExcelHandler
        """
        handlers = [handler for handler in args]
        return cls(tables=handlers)

    def to_bytes(self) -> bytes:
        with io.BytesIO() as output:
            writer = pd.ExcelWriter(output)
            for table in self.tables:
                df = table.get_data_as_dataframe()
                label = table.get_label()
                df.to_excel(writer, sheet_name=label, index=False)
            writer.save()
            output.seek(0)
            return output.read()

    def to_base64_str(self) -> str:
        """
        Convert table handlers into base64 encoded downloadable string
        """
        byte_data = self.to_bytes()
        decoded_data = base64.b64encode(byte_data).decode("utf-8")
        return decoded_data

    def create_download_link(self, filename: str) -> str:
        """
        Create download links from base 64 encoded string for the frontend
        :param filename: filename to be used when creating downloadable link
        """
        content = self.to_base64_str()
        return create_download_link(
            base64_str=content, filename=filename, filetype="xlsx"
        )

    def __str__(self) -> str:
        """String representation of the class"""
        return f"{self.__class__.__name__}([TableHandler(...), ...])"

    def __repr__(self) -> str:
        """Dev string representation of the class"""
        return f"{self.__class__.__name__}({self.tables})"

    def __len__(self) -> int:
        """Len implementation provides total number of TableHandler"""
        return len(self.tables)
