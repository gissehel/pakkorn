from PyQt4.QtCore import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui
import ui_package_info

class PackageInfoBase(QtGui.QDialog, ui_package_info.Ui_PackageInfo):
    def __init__(self, parent=None):
        super(PackageInfoBase, self).__init__(parent)
        self.setupUi(self)

        self._property_model = QtGui.QStandardItemModel(0, 2, parent)
        
        columns = ["Property","Value"]
        for count,column in enumerate(columns) :
            self._property_model.setHeaderData(count,QtCore.Qt.Horizontal,QtCore.QVariant(column))
        
        self._property_proxy_model = QtGui.QSortFilterProxyModel()
        self._property_proxy_model.setSourceModel(self._property_model)
        self._property_proxy_model.setDynamicSortFilter(True)
        
        self.tree_view_properties.setModel(self._property_proxy_model)
        self.tree_view_properties.setRootIsDecorated(False)
        
        #self.setItemAlignement(headerItem)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),self.rejected)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),self.accepted)
        
    def rejected(self) :
        self.done(2)

    def accepted(self) :
        self.done(1)

def create_application(WindowClass):
    import sys
    app = QtGui.QApplication(sys.argv)
    form = WindowClass()
    form.show()
    return app,form

def start_application(WindowClass) :
    app, form = create_application(WindowClass)
    app.exec_()

if __name__ == "__main__":
    start_application(PackageInfoBase)
