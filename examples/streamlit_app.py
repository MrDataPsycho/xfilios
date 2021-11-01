import streamlit as st

from xfilios.docx import DocxHandler
from xfilios.excel import ExcelHandler
from xfilios.table import TableHandler


def docx_handler_demo():
    st.title("Demo of xfilios DocxHandler")
    content = st.file_uploader("Upload Docx File", type="docx")
    if content:
        handler = DocxHandler.from_file_like(content)
        # Now you can send the encoded string over Http post request
        document_base_64 = handler.to_base64_str()
        # requests.post(body={"data": document_base_64})
        st.text(
            "Here is the base64 encoded document {}...".format(document_base_64[:10])
        )

        # Or if you received a base64 encoded binary document you can create a downloadable link
        download_link = handler.create_download_link(filename="demo.docx")
        download_text = f"Please Download the document back {download_link}"
        st.markdown(download_text, unsafe_allow_html=True)
        st.download_button(
            label="Download",
            data=handler.to_byte(),
            mime="application/octet-stream",
            file_name="demo.docx",
        )


def excel_handler_demo():
    st.title("Demo of xfilios ExcelHandler")
    content = st.file_uploader("Upload Docx File", type="xlsx")
    if content:
        # Each table handler will consist one table
        table_handler = TableHandler.from_file_like(content)
        # You can put multiple table handler into a list [table_handler1, table_handler2 ...]
        excel_handlers = ExcelHandler([table_handler])
        download_link = excel_handlers.create_download_link(filename="demo.xlsx")
        download_text = f"Please Download the File back {download_link}"
        st.markdown(download_text, unsafe_allow_html=True)
        st.download_button(
            label="Download",
            data=excel_handlers.to_bytes(),
            mime="application/octet-stream",
            file_name="demo.xlsx",
        )
        st.markdown("Here is the content of the file")
        st.table(table_handler.get_data_as_dataframe())


radio_button_factory = {
    "Demo DocxHandler": {"func": docx_handler_demo, "activate": True},
    "Demo ExcelHandler": {"func": excel_handler_demo, "activate": True},
}


def create_app() -> None:
    """
    Create the main app from the page repository
    :param app: streamlit module
    :return: No Return
    """
    active_sections = {
        key: value for key, value in radio_button_factory.items() if value["activate"]
    }
    sorted(active_sections)
    st.sidebar.header(":open_book: Menu")
    option = st.sidebar.radio("", list(active_sections.keys()))
    func = active_sections[option]["func"]
    func()  # type: ignore


if __name__ == "__main__":
    create_app()
