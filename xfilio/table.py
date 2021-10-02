from __future__ import annotations

import base64
import io
import typing as t
from collections import OrderedDict

import pandas as pd

from exception.fileio import TableHandlerError
from xfilio.xml import create_download_link
from global_utils import clean_text


class TableHandler:
    """Table data handler for the application a wrapper on top of dataframes"""

    def __init__(self, df: pd.DataFrame, schema: t.List, label: str) -> None:
        """
        Initializer for the class
        :param df: A dataframe
        :param schema
        """
        self.df = df
        self.schema = schema
        self.label = clean_text(label)

    @classmethod
    def from_collection(
            cls, data: t.List[t.Dict],
            label: str,
            column_map: t.Optional[OrderedDict] = None
    ) -> TableHandler:
        try:
            df = pd.DataFrame(data)
            # df = df.dropna(subset=list(df.columns))
            if column_map:
                schema = list(column_map.values())
                df = df.rename(columns=dict(column_map))
                df = df[schema]

                return cls(df=df, schema=schema, label=label)
            return cls(df=df, schema=list(df.columns), label=label)
        except Exception as e:
            print(e)
            raise TableHandlerError

    @classmethod
    def from_data_list(cls, data_list: t.List, schema: t.List, label: str) -> TableHandler:
        """
        Create a object of itself from inputs
        :param data_list: list of a list of rows to create dataframe
        :param schema: column name for the dataframe
        :param label: sheet name when creating the dataframe
        """
        try:
            df = pd.DataFrame(data_list)
            df.columns = schema
            return cls(df=df, schema=schema, label=label)
        except Exception as e:
            print(e)
            raise TableHandlerError

    @classmethod
    def from_file_like(cls, content: t.Union[t.TextIO, t.BinaryIO]) -> TableHandler:
        """
        Create itself from a file like object from streamlit
        :param content: File like object from frontend
        """
        try:
            all_sheets = pd.ExcelFile(content)
            sheet_name = all_sheets.sheet_names[0]
            df = pd.read_excel(content, sheet_name=sheet_name)
            schema = list(df.columns)
            label = sheet_name
            df = df.dropna()
            return cls(df, schema, label)
        except TableHandlerError as e:
            print(e)
            raise TableHandlerError
        except Exception as e:
            print(e)
            raise TableHandlerError

    def get_dataframe(self) -> pd.DataFrame:
        return self.df

    def get_label(self) -> str:
        return self.label

    def get_schema(self) -> t.List:
        return self.schema

    def get_records(self) -> t.List[t.Dict]:
        return self.df.to_dict(orient="records")


class ExcelHandler:
    """Excel handler to create downloadable excel file using Excel Writer"""

    def __init__(self, tables: t.List[TableHandler]):
        """
        Table Handler objects init
        :param tables: list of table handler
        """
        self.tables = tables

    @classmethod
    def from_table_handlers(cls, *args: TableHandler) -> ExcelHandler:
        handlers = [handler for handler in args]
        return cls(tables=handlers)

    def to_base64_str(self) -> str:
        """
        Convert table handlers into base64 encoded downloadable string
        """
        with io.BytesIO() as output:
            writer = pd.ExcelWriter(output)
            for table in self.tables:
                df = table.get_dataframe()
                label = table.get_label()
                df.to_excel(writer, sheet_name=label, index=False)
            writer.save()
            output.seek(0)
            decoded_data = base64.b64encode(output.read()).decode("utf-8")
            return decoded_data

    def create_download_link(self, filename: str) -> str:
        """
        Create download links from base 64 encoded string for the frontend
        :param filename: filename to be used when creating downloadable link
        """
        content = self.to_base64_str()
        return create_download_link(base64_str=content, filename=filename, filetype="xlsx")

