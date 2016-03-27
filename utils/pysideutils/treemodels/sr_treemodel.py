from PySide import QtGui

import sys
import yaml

from treemodel_pyside_example import NamesModel


class NameElement(object): # your internal structure

    def __init__(self, name, subelements):
        self.name = name
        self.subelements = subelements if isinstance(subelements, list) else [subelements]

    def __getitem__(self, key):
        item = filter(lambda x: x.name[0] == key, self.subelements)
        if len(item) > 1:
            raise Exception("More than one element named {} in subelements".format(key))
        elif len(item) < 1:
            return IndexError("{} was not found among subelements of NameElement".format(key))
        else:
            return item[0]


    @classmethod
    def generateFromDict(cls, input):
        if isinstance(input, dict):
            # if non of the dict values are themselves dicts:
            return_list = []
            for key, val in input.items():
                if isinstance(val, dict):
                    return_list.append(cls([key], cls.generateFromDict(val)))
                else:
                    return_list.append(cls([key, val], []))
            return return_list

        elif isinstance(input, list):
            return ([cls(["list"], cls.generateFromDict(val)) for val in input])
            return sibling_elements

        else:
            return cls(input, [])

    @classmethod
    def generateFromNestedList(cls, input):
        raise NotImplementedError

class MyWindow(QtGui.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setLayout(QtGui.QFormLayout(self))
        self.treeview = QtGui.QTreeView(self)

        objects = yaml.load(open("objects.yml", "rU"))
        self.els_from_yml = NameElement.generateFromDict(objects)

        self.model_from_yml = NamesModel(self.els_from_yml, headers=["Parameter", "Value"])

        self.treeview.setModel(self.model_from_yml)
        self.layout().addRow(self.treeview)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = MyWindow()
    win.show()
    app.exec_()