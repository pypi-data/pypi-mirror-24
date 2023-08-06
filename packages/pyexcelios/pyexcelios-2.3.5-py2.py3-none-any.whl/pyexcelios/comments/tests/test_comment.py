from __future__ import absolute_import
# Copyright (c) 2010-2016 openpyxl

from pyexcelios.comments import Comment
from pyexcelios.workbook import Workbook
from pyexcelios.worksheet import Worksheet

def test_init():
    wb = Workbook()
    ws = Worksheet(wb)
    c = Comment("text", "author")
    ws.cell(coordinate="A1").comment = c
    assert c._parent == ws.cell(coordinate="A1")
    assert c.text == "text"
    assert c.author == "author"
