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

import bisect
import logging

from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from .utils import parse_as_set
from .utils import AutoConsumed

logger = logging.getLogger(__name__)


class AnnexedKeyItem(QtGui.QStandardItem):
    def __init__(self, key_obj):
        super().__init__()
        self._obj = key_obj

        self.setText(self.key)
        self.setToolTip(self.key)

        font = QtGui.QFontDatabase.FixedFont
        font = QtGui.QFontDatabase().systemFont(font)
        self.setFont(font)

        icon = QtWidgets.QFileIconProvider.File
        icon = QtWidgets.QFileIconProvider().icon(icon)
        self.setIcon(icon)

        self.setSelectable(True)
        self.setEditable(False)
        self.setEnabled(True)
        self.setFlags(self.flags() | Qt.Qt.ItemNeverHasChildren)

    @property
    def metadata(self):
        return self._obj.metadata

    @property
    def key(self):
        return self._obj.key

    @property
    def contentlocation(self):
        return self._obj.contentlocation

    def type(self):
        return QtGui.QStandardItem.UserType + 1

    def __lt__(self, other):
        if other is None:
            return True

        elif isinstance(other, AnnexedKeyItem):
            lhs = self.data(role=Qt.Qt.DisplayRole)
            rhs = other.data(role=Qt.Qt.DisplayRole)

            lhs_pre, _, lhs_name = lhs.partition('--')
            lhs_backend, *lhs_fields = lhs_pre.split('-')
            lhs_fields = [(f[0], int(f[1:])) for f in lhs_fields]
            lhs = (lhs_backend, *lhs_fields, lhs_name)

            rhs_pre, _, rhs_name = rhs.partition('--')
            rhs_backend, *rhs_fields = rhs_pre.split('-')
            rhs_fields = [(f[0], int(f[1:])) for f in rhs_fields]
            rhs = (rhs_backend, *rhs_fields, rhs_name)

            try:
                return lhs > rhs
            except TypeError:
                return super().__lt__(other)

        else:
            return NotImplemented

    def __repr__(self):
        return "{name}.{cls}({args})".format(
            name=__name__,
            cls=self.__class__.__name__,
            args=self._obj.key,
        )


class AnnexedFieldItem(QtGui.QStandardItem):
    def __init__(self, key_item, field):
        super().__init__()
        self._item = key_item
        self._field = field

        self.setSelectable(True)
        self.setEditable(True)
        self.setEnabled(True)
        self.setFlags(self.flags() | Qt.Qt.ItemNeverHasChildren)

    @property
    def key(self):
        return self._item.key

    @property
    def contentlocation(self):
        return self._item.contentlocation

    @property
    def metadata(self):
        return self._item.metadata.get(self._field, set())

    @metadata.setter
    def metadata(self, value):
        self._item.metadata[self._field] = value
        self.emitDataChanged()

    def type(self):
        return QtGui.QStandardItem.UserType + 2

    def data(self, role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.DisplayRole:
            data = self.metadata

            if len(data) == 0:
                return None
            if len(data) == 1:
                return data.pop()
            else:
                return "<{n} values>".format(n=len(data))

        elif role == Qt.Qt.EditRole:
            data = self.metadata
            if data:
                return str(data)

        elif role == Qt.Qt.ToolTipRole:
            data = self.metadata
            if data:
                return str(data)

        elif role == Qt.Qt.UserRole:
            return self.metadata

        else:
            return super().data(role=role)

    def setData(self, value, role=Qt.Qt.EditRole):
        if role == Qt.Qt.DisplayRole:
            return False

        elif role == Qt.Qt.EditRole:
            try:
                self.metadata = parse_as_set(value)
            except:
                fmt = "Cannot parse '{}' as a set object."
                msg = fmt.format(value)
                logger.error(msg)
                return

        elif role == Qt.Qt.UserRole:
            try:
                self.metadata = value
            except:
                fmt = "Cannot parse '{}' as a set object."
                msg = fmt.format(value)
                logger.error(msg)
                return

        else:
            super().setData(value, role=role)

    def __lt__(self, other):
        if other is None:
            return True

        elif isinstance(other, AnnexedFieldItem):
            lhs = self.data(role=Qt.Qt.UserRole)
            rhs = other.data(role=Qt.Qt.UserRole)
            if len(lhs) == 0:
                return False
            elif len(rhs) == 0:
                return True
            elif len(lhs) == len(rhs) == 1:
                lhs_, rhs_ = lhs.pop(), rhs.pop()
                try:
                    return int(lhs_) > int(rhs_)
                except ValueError:
                    return super().__lt__(other)
            else:
                return len(lhs) > len(rhs)

        else:
            return NotImplemented

    def __repr__(self):
        return "{name}.{cls}({args})".format(
            name=__name__,
            cls=self.__class__.__name__,
            args={
                'item': self._item,
                'field': self._field,
            }
        )


class AnnexedKeyMetadataModel(QtGui.QStandardItemModel):
    key_inserted = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repo = None

    def setRepo(self, repo):
        if self._populate.running():
            self._populate.stop()
            msg = "Aborted loading previous key model."
            logger.info(msg)

        self.repo = repo
        self.fields = ['Git-Annex Key']
        self.key_items = {}
        self._pending = iter(self.repo.annex.values())

        self.clear()
        self.setHorizontalHeaderLabels(self.fields)
        self._populate.start()

    @QtCore.pyqtSlot()
    @AutoConsumed
    def _populate(self):
        msg = "Loading key model..."
        logger.info(msg)

        for obj in self._pending:
            self.insert_key(obj)
            yield

        msg = "Key model fully loaded."
        logger.info(msg)

    def insert_key(self, key_obj):
        key_item = AnnexedKeyItem(key_obj)
        field_items = (
            AnnexedFieldItem(key_obj, field)
            for field in self.fields[1:]
        )
        self.appendRow([key_item, *field_items])
        self.key_items[key_item.key] = key_item

        new_fields = set(key_item.metadata) - set(self.fields)
        for field in new_fields:
            QtCore.QMetaObject.invokeMethod(
                self, 'insert_field',
                Qt.Qt.QueuedConnection,
                QtCore.Q_ARG(str, field)
            )

        self.key_inserted.emit(key_obj.key)

    @QtCore.pyqtSlot(str)
    def insert_field(self, field):
        if field in self.fields:
            return
        col = bisect.bisect(self.fields, field, lo=1)
        items = [
            AnnexedFieldItem(self.item(row, 0), field)
            for row in range(self.rowCount())
        ]
        self.fields.insert(col, field)
        self.insertColumn(col, items)
        self.setHorizontalHeaderLabels(self.fields)

    def __repr__(self):
        return "{name}.{cls}({args})".format(
            name=__name__,
            cls=self.__class__.__name__,
            args=self.repo,
        )

