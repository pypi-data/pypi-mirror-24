from __future__ import absolute_import
# Copyright (c) 2010-2016 openpyxl
from pyexcelios.compat import unicode

from pyexcelios.descriptors.serialisable import Serialisable
from pyexcelios.descriptors import (
    Sequence,
    Alias
)


class AuthorList(Serialisable):

    tagname = "authors"

    author = Sequence(expected_type=unicode)
    authors = Alias("author")

    def __init__(self,
                 author=(),
                ):
        self.author = author
