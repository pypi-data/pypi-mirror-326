# coding=utf-8
#
# Copyright © Splunk, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function, unicode_literals

from abc import ABCMeta, abstractmethod
from builtins import object
from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE
from collections import namedtuple
from os import path
import os
import io
import re
from future.utils import with_metaclass


from . file_reader import FileReader
from ... utils.internal import string


class FileBuffer(with_metaclass(ABCMeta, object)):

    def __init__(self, filename):
        self._filename = path.abspath(filename)
        self._records = []

    # region Properties

    @property
    def filename(self):
        return self._filename

    # endregion

    # region Methods

    def dump(self, file=None):  # pylint: disable=redefined-builtin
        if file is None:
            file = self.filename
        if isinstance(file, string):
            with io.open(file, encoding='utf-8', mode='w', newline='') as ostream:
                self._dump(ostream)
            return
        self._dump(ostream=file)

    def load(self, **kwargs):

        file_no = os.open(self._filename, self._access_mode)

        try:
            header = os.read(file_no, 4)
            encoding = 'utf-8-sig'
            offset = 0

            for supported_encoding, byte_order_marks in self._supported_encodings:
                for bom in byte_order_marks:
                    if header.startswith(bom):
                        encoding = supported_encoding
                        offset = len(bom)
                        break

            os.lseek(file_no, offset, io.SEEK_SET)

            # noinspection PyTypeChecker
            with io.open(file_no, closefd=False, encoding=encoding) as text_stream:
                self._load(FileReader(text_stream, self._filename), **kwargs)

        finally:
            os.close(file_no)

    # pylint: disable=redefined-builtin
    def save(self, file=None):

        if file is None:
            file = self._filename

        if not isinstance(file, string):
            self._save(file)
        else:
            # TODO: write to a temporary file, then delete the original, and give the temporary file its name
            with io.open(file, encoding='utf-8', mode='w', newline='') as ostream:
                self._save(ostream)

    # endregion

    # region Protected

    _access_mode = os.O_RDONLY | getattr(os, 'O_BINARY', 0)

    _supported_encodings = (
        ('utf-8-sig', (BOM_UTF8,)), ('utf-16', (BOM_UTF16_LE, BOM_UTF16_BE)), ('utf-32', (BOM_UTF32_LE, BOM_UTF32_BE))
    )

    def _append(self, item, position, indentation):
        """ Appends an item with the given indentation to the current Buffer

        """
        records = self._records
        records.append(FileBuffer._Record(item, position, indentation))

    def _dump(self, ostream):
        pass  # TODO: implement FileBuffer._dump

    @abstractmethod
    def _load(self, reader, **kwargs):
        pass

    _match_assignment_statement = re.compile(r'(?!\*)((?:\\.|[^\\=])*?)\s*=\s*(.*)\s*\n?$', re.M | re.S | re.U).match

    def _save(self, ostream):
        for record in self._records:
            indentation = record.column
            item = record.item
            if isinstance(item, string):
                if indentation > 0:
                    ostream.write(' ' * indentation)
                ostream.write(item)
            else:
                ostream.write(string(item))
                ostream.write('\n')

    _search_right_square_bracket = re.compile(r'\]\s*$', re.M | re.U).search

    _skip_whitespace = re.compile(r'\s*', re.M | re.U).match

    # endregion

    class _Error(Exception):
        pass

    # noinspection PyClassHasNoInit
    class _Record(namedtuple('_Record', ('item', 'position', 'column'))):
        __slots__ = ()  # no extra slots required for this derived type

        def __str__(self):
            return ' ' * self.column + string(self.item)

    pass  # pylint: disable=unnecessary-pass
