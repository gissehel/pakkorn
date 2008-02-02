# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\home\dev\eclipse\workspace-3.3\pakkorn3\src\pakkorn\gui\qt\pakkorn.ui'
#
# Created: Sat Feb 02 20:08:48 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Pakkorn(object):
    def setupUi(self, Pakkorn):
        Pakkorn.setObjectName("Pakkorn")
        Pakkorn.resize(QtCore.QSize(QtCore.QRect(0,0,737,411).size()).expandedTo(Pakkorn.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Pakkorn.sizePolicy().hasHeightForWidth())
        Pakkorn.setSizePolicy(sizePolicy)
        Pakkorn.setWindowIcon(QtGui.QIcon("../../../../ressources/pakkorn-02.png"))

        self.centralwidget = QtGui.QWidget(Pakkorn)
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(3)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.searchFilter = QtGui.QComboBox(self.centralwidget)
        self.searchFilter.setEditable(True)
        self.searchFilter.setObjectName("searchFilter")
        self.vboxlayout1.addWidget(self.searchFilter)

        self.categoriesWidget = QtGui.QListWidget(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoriesWidget.sizePolicy().hasHeightForWidth())
        self.categoriesWidget.setSizePolicy(sizePolicy)
        self.categoriesWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.categoriesWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.categoriesWidget.setTabKeyNavigation(True)
        self.categoriesWidget.setDragEnabled(True)
        self.categoriesWidget.setIconSize(QtCore.QSize(16,16))
        self.categoriesWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.categoriesWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.categoriesWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.categoriesWidget.setUniformItemSizes(True)
        self.categoriesWidget.setSortingEnabled(False)
        self.categoriesWidget.setObjectName("categoriesWidget")
        self.vboxlayout1.addWidget(self.categoriesWidget)
        self.hboxlayout.addLayout(self.vboxlayout1)

        self.detailWidget = QtGui.QTreeWidget(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detailWidget.sizePolicy().hasHeightForWidth())
        self.detailWidget.setSizePolicy(sizePolicy)
        self.detailWidget.setRootIsDecorated(False)
        self.detailWidget.setAllColumnsShowFocus(True)
        self.detailWidget.setObjectName("detailWidget")
        self.hboxlayout.addWidget(self.detailWidget)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(3)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setMaximum(10)
        self.progressBar.setProperty("value",QtCore.QVariant(7))
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.hboxlayout1.addWidget(self.progressBar)

        spacerItem = QtGui.QSpacerItem(91,24,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.push_update = QtGui.QPushButton(self.centralwidget)
        self.push_update.setObjectName("push_update")
        self.hboxlayout1.addWidget(self.push_update)

        self.push_download = QtGui.QPushButton(self.centralwidget)
        self.push_download.setObjectName("push_download")
        self.hboxlayout1.addWidget(self.push_download)

        self.push_install = QtGui.QPushButton(self.centralwidget)
        self.push_install.setObjectName("push_install")
        self.hboxlayout1.addWidget(self.push_install)
        self.vboxlayout.addLayout(self.hboxlayout1)
        Pakkorn.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(Pakkorn)
        self.menubar.setGeometry(QtCore.QRect(0,0,737,19))
        self.menubar.setFocusPolicy(QtCore.Qt.TabFocus)
        self.menubar.setObjectName("menubar")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")

        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        Pakkorn.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(Pakkorn)
        self.statusbar.setObjectName("statusbar")
        Pakkorn.setStatusBar(self.statusbar)

        self.action_Close = QtGui.QAction(Pakkorn)
        self.action_Close.setObjectName("action_Close")

        self.action_Open_2 = QtGui.QAction(Pakkorn)
        self.action_Open_2.setObjectName("action_Open_2")

        self.action_Update = QtGui.QAction(Pakkorn)
        self.action_Update.setObjectName("action_Update")

        self.action_Install = QtGui.QAction(Pakkorn)
        self.action_Install.setObjectName("action_Install")

        self.action_Show = QtGui.QAction(Pakkorn)
        self.action_Show.setIcon(QtGui.QIcon("../../../../../../../../../../usr/lib/Qt/4.2.3/tools/designer/src/components/formeditor/images/submenu.png"))
        self.action_Show.setObjectName("action_Show")

        self.action_website = QtGui.QAction(Pakkorn)
        self.action_website.setObjectName("action_website")

        self.action_Configuration = QtGui.QAction(Pakkorn)
        self.action_Configuration.setObjectName("action_Configuration")
        self.menuFile.addAction(self.action_Open_2)
        self.menuFile.addAction(self.action_Close)
        self.menu_Help.addAction(self.action_website)
        self.menu_Edit.addAction(self.action_Update)
        self.menu_Edit.addAction(self.action_Install)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Show)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Configuration)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(Pakkorn)
        QtCore.QObject.connect(self.categoriesWidget,QtCore.SIGNAL("itemSelectionChanged()"),Pakkorn.repaint)
        QtCore.QObject.connect(self.push_update,QtCore.SIGNAL("clicked()"),Pakkorn.update)
        QtCore.QMetaObject.connectSlotsByName(Pakkorn)

    def retranslateUi(self, Pakkorn):
        Pakkorn.setWindowTitle(QtGui.QApplication.translate("Pakkorn", "pakkorn", None, QtGui.QApplication.UnicodeUTF8))
        self.detailWidget.headerItem().setText(0,QtGui.QApplication.translate("Pakkorn", "D", None, QtGui.QApplication.UnicodeUTF8))
        self.detailWidget.headerItem().setText(1,QtGui.QApplication.translate("Pakkorn", "I", None, QtGui.QApplication.UnicodeUTF8))
        self.detailWidget.headerItem().setText(2,QtGui.QApplication.translate("Pakkorn", "L", None, QtGui.QApplication.UnicodeUTF8))
        self.detailWidget.headerItem().setText(3,QtGui.QApplication.translate("Pakkorn", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.detailWidget.headerItem().setText(4,QtGui.QApplication.translate("Pakkorn", "Full Name", None, QtGui.QApplication.UnicodeUTF8))
        self.detailWidget.headerItem().setText(5,QtGui.QApplication.translate("Pakkorn", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.push_update.setText(QtGui.QApplication.translate("Pakkorn", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.push_download.setText(QtGui.QApplication.translate("Pakkorn", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.push_install.setText(QtGui.QApplication.translate("Pakkorn", "Install", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("Pakkorn", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("Pakkorn", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Edit.setTitle(QtGui.QApplication.translate("Pakkorn", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Close.setText(QtGui.QApplication.translate("Pakkorn", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_2.setText(QtGui.QApplication.translate("Pakkorn", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Update.setText(QtGui.QApplication.translate("Pakkorn", "&Update", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Install.setText(QtGui.QApplication.translate("Pakkorn", "&Install", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Show.setText(QtGui.QApplication.translate("Pakkorn", "&Show", None, QtGui.QApplication.UnicodeUTF8))
        self.action_website.setText(QtGui.QApplication.translate("Pakkorn", "&website", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Configuration.setText(QtGui.QApplication.translate("Pakkorn", "&Configuration", None, QtGui.QApplication.UnicodeUTF8))

