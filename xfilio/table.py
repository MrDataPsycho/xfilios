from __future__ import annotations

import base64
import io
import typing as t

import pandas as pd

from .exceptions import TableHandlerError
from xfilio.html import create_download_link


class TableHandler:
    """Table data handler for the application a wrapper on top of dataframes"""

    def __init__(self, df: pd.DataFrame, schema: t.List, label: str) -> None:
        """
        Initializer of the TableHandler class
        :param df: A pandas dataframe
        :param schema: A Column Name list of the DataFrame to use
        :param label: A label/tag which will be used as excel sheet name when creating a excel file
        """
        self.df = df
        self.schema = schema
        self.label = label

    @classmethod
    def from_records(
            cls,
            data: t.List[t.Dict],
            col_headers: t.Optional[t.OrderedDict[str, str]],
            label: str
    ) -> TableHandler:
        """
        Create A TableHandler object from list of records
        :param data: List of records, similar structure as pd.DataFrame().to_dict(orient="records")
        :param col_headers: Column Rename Map, if Not provided default DataFrame column will be used
        :param label: A label/tag which will be used when creating sheet name in excel file
        :return: Object of type TableHandler
        """
        try:
            df = pd.DataFrame(data)
            if col_headers:
                schema = list(col_headers.values())
                df = df.rename(columns=dict(col_headers))
                df = df[schema]

                return cls(df=df, schema=schema, label=label)
            return cls(df=df, schema=list(df.columns), label=label)
        except Exception as e:
            raise TableHandlerError(e)

    @classmethod
    def from_list(
            cls,
            data: t.List,
            col_headers: t.Optional[t.List[str]],
            label: str
    ) -> TableHandler:
        """
        Create A TableHandler object from list of list e.g data = [[...], [...]] or data = [(...), (...)]
        :param data: list of a list of rows to create DataFrame
        :param col_headers: column name to use for the DataFrame, if not provided default will be used
        :param label: A label/tag which will be used when creating sheet name in excel file
        """
        try:
            df = pd.DataFrame(data)
            if col_headers:
                if len(col_headers) != len(df.columns):
                    raise TableHandlerError("Length of col_headers does not match with the length of DataFrame columns")
                df.columns = col_headers
            return cls(df=df, schema=col_headers, label=label)
        except Exception as e:
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
            raise TableHandlerError(e)
        except Exception as e:
            raise TableHandlerError(e)

    def get_dataframe(self) -> pd.DataFrame:
        """Get the DataFrame store in the class"""
        return self.df

    def get_label(self) -> str:
        """Getter for the label field"""
        return self.label

    def get_schema(self) -> t.List:
        """Getter for the schema field"""
        return self.schema

    def get_records(self) -> t.List[t.Dict]:
        """Get the records stored in the dataframe as List of Dict"""
        return self.df.to_dict(orient="records")

    def __str__(self) -> str:
        """String Representation of the class"""
        return f"{self.__class__.__name__}(df=({self.df.shape}), {self.schema}, {self.label})"

    def __repr__(self) -> str:
        """Dev string representation of the class"""
        return f"{self.__class__.__name__}({self.df}, {self.schema}, {self.label})"

    def __len__(self) -> int:
        """Len representation provides the len of the DataFrame attached"""
        return len(self.df)


class ExcelHandler:
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
        :param args: List of TableHandlers Object
        :return: Instance of Type ExcelHandler
        """
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

    def __str__(self) -> str:
        """String representation of the class"""
        return f"{self.__class__.__name__}([...])"

    def __repr__(self) -> str:
        """Dev string representation of the class"""
        return f"{self.__class__.__name__}({self.tables})"

    def __len__(self) -> int:
        """Len implementation provides total number of TableHandler"""
        return len(self.tables)




