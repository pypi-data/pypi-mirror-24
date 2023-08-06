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

import logging

from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

logger = logging.getLogger(__name__)

from .utils import StandardItemProxyModel

class MetadataTreeView(QtWidgets.QTreeView):
    item_selected = QtCore.pyqtSignal(QtGui.QStandardItem)
    header_visibility_changed = QtCore.pyqtSignal(str, bool)
    header_created = QtCore.pyqtSignal(str)
    model_reset = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._treeish = 'HEAD'
        self.sortByColumn(0, Qt.Qt.AscendingOrder)

    def setModel(self, model):
        self._bare_model = model
        self._proxy_model = StandardItemProxyModel(model)
        self._proxy_model.setSourceModel(model)
        super().setModel(self._proxy_model)

        signal = self.selectionModel().selectionChanged
        signal.connect(self._on_selection_changed)

        signal = self._bare_model.headerDataChanged
        signal.connect(self._on_header_data_changed)

        signal = self._bare_model.modelReset
        signal.connect(self._on_model_reset)

    @QtCore.pyqtSlot(str)
    @QtCore.pyqtSlot(str, bool)
    def show_header(self, title, visible=True):
        if title not in self._bare_model.fields:
            return
        idx = self._bare_model.fields.index(title)
        header = self.header()
        if header.isSectionHidden(idx) != (not visible):
            header.setSectionHidden(idx, not visible)
            self.header_visibility_changed.emit(title, visible)

        fmt = "{} tree column for field '{}'."
        msg = fmt.format('Showing' if visible else 'Hiding', title)
        logger.info(msg)

    @QtCore.pyqtSlot(str)
    def hide_header(self, title):
        self.show_header(title, False)

    @QtCore.pyqtSlot(str)
    def create_header(self, title):
        self._bare_model.insert_field(title)

    @QtCore.pyqtSlot(str)
    def set_treeish_to_build(self, treeish):
        if treeish:
            self._treeish = treeish
        else:
            self._treeish = 'HEAD'

    @QtCore.pyqtSlot()
    def rebuild_treeish(self):
        if not self.model():
            return

        fmt = "Building tree for git treeish '{}'."
        msg = fmt.format(self._treeish)
        logger.info(msg)

        self._bare_model.setTreeish(self._treeish)

    def _on_selection_changed(self, selected, deselected):
        indexes = selected.indexes()
        if not indexes:
            return

        index = indexes[0]
        src_index = index.model().mapToSource(index)
        item = src_index.model().itemFromIndex(src_index)

        self.item_selected.emit(item)

    def _on_header_data_changed(self, orientation, first, last):
        fields = self._bare_model.fields[1:]

        for field in fields:
            if field not in self._fields:
                self.header_created.emit(field)

        self._fields = fields

    def _on_model_reset(self):
        self._fields = []
        self.model_reset.emit()

    def __repr__(self):
        return "{name}.{cls}({args})".format(
            name=__name__,
            cls=self.__class__.__name__,
            args='',
        )
