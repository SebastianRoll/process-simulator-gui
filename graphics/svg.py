from PySide import QtGui, QtCore, QtSvg
import yaml


class SvgItem(QtSvg.QGraphicsSvgItem):
    '''def __init__(self, svg_filepath, parent=None, scene=None):
        self.filepath = svg_filepath
        super(SvgItem, self).__init__(svg_filepath, parent, scene)'''

    @classmethod
    def from_yaml(cls, yaml_filepath):
        svg_yml = yaml.load(open(yaml_filepath, "rU"))
        svg_path = svg_yml['svg_path']
        item_names = svg_yml['item_names']

        svg_gr_items = []
        for item_name in item_names:
            # todo - fix bug of program terminating when using sharedRenderer
            #renderer = QtSvg.QSvgRenderer('/home/noitapicname/pycharmprojects/processsimulator_gui/PFD symbols.svg')
            svg_item = cls(svg_path)
            #vladsvg.setSharedRenderer(renderer)
            svg_item.setElementId(item_name)
            svg_gr_items.append(svg_item)

        return svg_gr_items


if __name__ == '__main__':
    yaml_filepath = "svgitems.yml"
    svg_gr_items = SvgItem.from_yaml(yaml_filepath)
    print svg_gr_items