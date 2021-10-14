import pytest
from docx.document import Document

from tests import create_demo_docx
from xfilios.docx import DocxHandler


class TestDocxHandler:
    NAME = "demo.docx"

    @pytest.fixture
    def subject(self):
        handler = DocxHandler(document=create_demo_docx(), name=self.NAME)
        return handler

    def test_docx_init(self, subject):
        assert subject.name == self.NAME
        assert isinstance(subject.document, Document)

    def test_docx_len(self, subject):
        expected = 3
        assert len(subject) == expected

    def test_docx_str(self, subject):
        assert str(subject) == f'DocxHandler(document="...", name={self.NAME})'

    def test_get_stat(self, subject):
        expected = {"tables": 1, "paragraphs": 3}
        assert subject.get_stat() == expected
