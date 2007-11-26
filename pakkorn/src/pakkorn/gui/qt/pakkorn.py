from PyQt4.QtCore import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui
import ui_pakkorn

class PakkornMainWindowBase(QtGui.QMainWindow, ui_pakkorn.Ui_Pakkorn):
    def __init__(self, parent=None):
        super(PakkornMainWindowBase, self).__init__(parent)
        self.setupUi(self)
        
        headerItem = self.detailWidget.headerItem()
        self.setItemAlignement(headerItem)
        
        self.onCategorieChanged()
        
        for index in xrange(self.detailWidget.columnCount()) : 
            self.detailWidget.resizeColumnToContents(index)

    def setItemAlignement(self, item) :
        item.setTextAlignment(0,Qt.AlignHCenter)
        item.setTextAlignment(1,Qt.AlignHCenter)
        item.setTextAlignment(2,Qt.AlignHCenter)
        item.setTextAlignment(3,Qt.AlignLeft)   
        item.setTextAlignment(4,Qt.AlignLeft)   
        item.setTextAlignment(5,Qt.AlignLeft)   

    def addPackage(self, array) :
        q = QtGui.QTreeWidgetItem()

        for index,value in enumerate(array) :
            q.setText(index,value)
        self.setItemAlignement(q)

        self.detailWidget.insertTopLevelItem(0,q)
        
    def addCategorie(self, categorie) :
        item = QtGui.QListWidgetItem()
        item.setText(categorie)
        self.categoriesWidget.addItem(item)

class PakkornMainWindowTest(PakkornMainWindowBase):
    def __init__(self, parent=None):
        super(PakkornMainWindowTest, self).__init__(parent)

        QtCore.QObject.connect(self.categoriesWidget,QtCore.SIGNAL("itemSelectionChanged()"),self.onCategorieChanged)
        QtCore.QObject.connect(self.push_update,QtCore.SIGNAL("clicked()"),self.onUpdate)

        self.addCategorie("Type :: Audio :: Editor")
        self.addCategorie("Type :: Video :: Editor")
        self.addCategorie("License :: OSI Approved :: GPL")
        self.addCategorie("License :: OSI Approved :: BSD Like")
        self.addCategorie("License :: OSI Approved :: Artistic")
        self.addCategorie("License :: OSI Approved :: Python-License")
        self.addCategorie("License :: Freeware")
        self.addCategorie("License :: Shareware")


    def onCategorieChanged(self) :
        self.detailWidget.clear()
        self.addPackage("I/D/L/totalcommander/Total Commander/7.02a".split("/"))
        self.addPackage("/D//totalcommander/Total Commander/7.01".split("/"))
        self.addPackage("I///gimp/The Gimp/4.2.1".split("/"))
        
    def onUpdate(self) :
        self.addPackage("//L/gimp/The Gimp/4.2.2".split("/"))


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
    start_application(PakkornMainWindowTest)
