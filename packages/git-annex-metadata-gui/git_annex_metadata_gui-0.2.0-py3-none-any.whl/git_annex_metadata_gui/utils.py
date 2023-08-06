#!/usr/bin/env python3

# Git-Annex-Metadata-Gui
# Copyright (C) 2017 Alper Nebi Yasak
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import ast
import functools
import logging
import time

from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore

logger = logging.getLogger(__name__)


def parse_as_set(x):
    if x == '{}':
        return set()

    try:
        xs = ast.literal_eval(x)
        assert isinstance(xs, set)
        return xs

    except Exception as err:
        fmt = "Can't interpret '{}' as a set."
        msg = fmt.format(x)
        raise ValueError(msg) from err


class AutoConsumed:
    _timeout = 0.05

    def __init__(self, function):
        self._function = function
        self._generator = None
        self._instance = None
        functools.update_wrapper(self, function)

    def start(self, *args):
        self._generator = self._function(self._instance, *args)
        self()

    def running(self):
        return self._generator is not None

    def stop(self):
        self._generator = None

    def __call__(self, instance=None):
        if instance is not None and instance is not self._instance:
            fmt = "Instance mismatch on autoconsumer {}, ({} vs {})."
            msg = fmt.format(
                self._function.__name__,
                instance, self._instance,
            )
            logger.critical(msg)

        if self._generator is None:
            return

        try:
            endtime = time.monotonic() + self._timeout
            while time.monotonic() < endtime:
                next(self._generator)

        except StopIteration:
            self._generator = None

        else:
            QtCore.QMetaObject.invokeMethod(
                self._instance, self._function.__name__,
                Qt.Qt.QueuedConnection,
            )

    def __get__(self, instance, owner):
        self._instance = instance
        return self

    def __repr__(self):
        return "{name}.{cls}({args})".format(
            name=__name__,
            cls=self.__class__.__name__,
            args=self._function.__name__,
        )


class DataProxyItem(QtGui.QStandardItem):
    def __init__(self, item):
        super().__init__()
        self._item = item

        model = self._item.model()
        model.dataChanged.connect(self._propagate_changes)

    def type(self):
        return QtGui.QStandardItem.UserType + 3

    def data(self, role=Qt.Qt.DisplayRole):
        return self._item.data(role=role)

    def setData(self, value, role=Qt.Qt.EditRole):
        return self._item.setData(value, role=role)

    def flags(self):
        return self._item.flags()

    def _propagate_changes(self, topLeft, bottomRight, roles):
        rows = range(topLeft.row(), bottomRight.row() + 1)
        columns = range(topLeft.column(), bottomRight.column() + 1)

        if self._item.row() in rows and self._item.column() in columns:
            self.emitDataChanged()

    def __repr__(self):
        return "{name}.{cls}({args})".format(
            name=__name__,
            cls=self.__class__.__name__,
            args=self._item,
        )


class StatusBarLogHandler(logging.Handler):
    def __init__(self, statusbar):
        super().__init__()
        self._statusbar = statusbar

    def emit(self, record):
        msg = self.format(record)
        line = msg.split('\n')[0]
        self._statusbar.showMessage(line, msecs=5000)

    def __repr__(self):
        return "{name}.{cls}({args})".format(
            name=__name__,
            cls=self.__class__.__name__,
            args=self._statusbar,
        )


class StandardItemProxyModel(QtCore.QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        descending = (self.sortOrder() == Qt.Qt.DescendingOrder)

        lhs_flags = source_left.sibling(source_left.row(), 0).flags()
        lhs_is_dir = not bool(lhs_flags & Qt.Qt.ItemNeverHasChildren)

        rhs_flags = source_right.sibling(source_right.row(), 0).flags()
        rhs_is_dir = not bool(rhs_flags & Qt.Qt.ItemNeverHasChildren)

        if lhs_is_dir and (not rhs_is_dir):
            return not descending
        elif (not lhs_is_dir) and rhs_is_dir:
            return descending

        model = self.sourceModel()
        lhs = model.itemFromIndex(source_left)
        rhs = model.itemFromIndex(source_right)

        try:
            return (lhs < rhs)
        except TypeError:
            return super().lessThan(source_left, source_right)

