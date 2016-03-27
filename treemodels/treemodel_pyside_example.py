from PySide import QtCore

from PySide.QtCore import QAbstractItemModel, QModelIndex, Qt


class TreeNode(object):
    def __init__(self, parent, row):
        self.parent = parent
        self.row = row
        self.subnodes = self._getChildren()

    def _getChildren(self):
        raise NotImplementedError()

    def row_path(self):
        '''rowpath = [self.row]
        if self.parent is not None:
            rowpath.append(self.parent.row_path())'''
        if self.parent is not None:
            return self.parent.row_path(), self.row
        else:
            return self.row



class TreeModelSimple(QAbstractItemModel):
    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.rootNodes = self._getRootNodes()

    def _getRootNodes(self):
        raise NotImplementedError()

    def index(self, row, column, parent):
        if not parent.isValid():
            return self.createIndex(row, column, self.rootNodes[row])
        parentNode = parent.internalPointer()
        return self.createIndex(row, column, parentNode.subnodes[row])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0, node.parent)

    def reset(self):
        self.rootNodes = self._getRootNodes()
        QAbstractItemModel.reset(self)

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.rootNodes)
        node = parent.internalPointer()
        return len(node.subnodes)




class NamedNode(TreeNode):

    @property
    def itemData(self): return self.ref.name

    def __init__(self, ref, parent, row):
        self.ref = ref
        TreeNode.__init__(self, parent, row)

    def _getChildren(self):
        return [NamedNode(elem, self, index)
            for index, elem in enumerate(self.ref.subelements)]

    def data(self, column):
        if len(self.ref.name) >= column + 1:
            return self.itemData[column]
        else:
            return None

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column] = value
        print "in treenode.setData()"
        print self.row_path()

        return True

    def add_subelement(self, name_element):
        row = len(self.ref.subelements)
        self.ref.subelements.append(name_element)
        return NamedNode(name_element, self, row)


class NamesModel(TreeModelSimple):
    def __init__(self, rootElements, headers=None):
        self.headers = ["Name"] if not headers else headers
        self.rootElements = rootElements
        TreeModelSimple.__init__(self)

    def _getRootNodes(self):
        return [NamedNode(elem, None, index)
            for index, elem in enumerate(self.rootElements)]

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return None

        item = self.getItem(index)
        return item.data(index.column())
        '''
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node.ref.name
        return None'''

    def flags(self, index):
        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result

    #--- Public
    def findIndex(self, rowPath):
        """Returns the QModelIndex at `rowPath`

        `rowPath` is a sequence of node rows. For example, [1, 2, 1] is the 2nd child of the
        3rd child of the 2nd child of the root.
        """
        result = QModelIndex()
        for row in rowPath:
            result = self.index(row, 0, result)
        return result
