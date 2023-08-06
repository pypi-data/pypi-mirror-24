# Copyright (c) 2010-2016 openpyxl

# Python stdlib imports
from zipfile import ZipFile
from datetime import datetime

# test imports
import pytest

# package imports
from pyexcelios.tests.helper import compare_xml
from pyexcelios.writer.workbook import (
    write_properties_app
)
from pyexcelios.xml.constants import ARC_CORE
from pyexcelios.utils.datetime  import CALENDAR_WINDOWS_1900
from pyexcelios.workbook import DocumentProperties, Workbook


@pytest.mark.parametrize("filename", ['sample.xlsx', 'empty_libre.xlsx'])
def test_read_sheets_titles(datadir, filename):
    from pyexcelios.reader.workbook import read_sheets

    datadir.join("genuine").chdir()
    archive = ZipFile(filename)
    sheet_titles = [s['name'] for s in read_sheets(archive)]
    assert sheet_titles == ['Sheet1 - Text', 'Sheet2 - Numbers', 'Sheet3 - Formulas', 'Sheet4 - Dates']


def test_write_properties_app(datadir):
    datadir.join("writer").chdir()
    wb = Workbook()
    wb.create_sheet()
    wb.create_sheet()
    content = write_properties_app(wb)
    with open('app.xml') as expected:
        diff = compare_xml(content, expected.read())
    assert diff is None, diff
