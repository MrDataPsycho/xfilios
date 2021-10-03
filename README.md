# Xfilio
Excel and Docx FileIO handlers in the client side for Streamlit and Dash Framework. The library provides easy to use classes to encode or decode Docx and Excel at the client side. The following core features are available:
- Convert an uploaded Docx-file into base64 encoded string to send over HTTP post request using Python-Docx
- Convert Data received from an HTTP get/post request into Downloadable Excel file 
- Combine multiple data source into multi-sheet Downloadable Excel file at the frontend

This package is actually a wrapper over pandas and python-docx package. 