# Xfilios
Excel and Docx FileIO handlers in the client side for Streamlit (in future Dash will also be considered) Framework. The library provides easy to use classes to encode or decode Docx and Excel at the client side. The following core features are available in the library:
- Convert an uploaded Docx-file into base64 encoded string to send over HTTP post request (a wrapper over python-docx package)
- Convert Data received from an HTTP get/post request into Downloadable Excel file (a wrapper over pandas and openpyxl)
- Combine multiple data source into multi-sheet Downloadable Excel file at the frontend (a wrapper using pandas ReadExcel function with openpyxl)

This package is actually a wrapper over pandas and python-docx package. It is possible to extend other fileIO types like csv, text etc in further release. 