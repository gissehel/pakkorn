# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\home\dev\eclipse\workspace-3.3\pakkorn3\src\pakkorn\gui\qt\package_info.ui'
#
# Created: Sat Feb 02 20:08:46 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PackageInfo(object):
    def setupUi(self, PackageInfo):
        PackageInfo.setObjectName("PackageInfo")
        PackageInfo.resize(QtCore.QSize(QtCore.QRect(0,0,623,610).size()).expandedTo(PackageInfo.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(PackageInfo)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label_icons = QtGui.QLabel(PackageInfo)
        self.label_icons.setObjectName("label_icons")
        self.gridlayout.addWidget(self.label_icons,5,0,1,1)

        self.line_edit_idproj = QtGui.QLineEdit(PackageInfo)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit_idproj.sizePolicy().hasHeightForWidth())
        self.line_edit_idproj.setSizePolicy(sizePolicy)
        self.line_edit_idproj.setObjectName("line_edit_idproj")
        self.gridlayout.addWidget(self.line_edit_idproj,0,1,1,1)

        self.label_categories = QtGui.QLabel(PackageInfo)
        self.label_categories.setObjectName("label_categories")
        self.gridlayout.addWidget(self.label_categories,4,0,1,1)

        self.label_description = QtGui.QLabel(PackageInfo)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_description.sizePolicy().hasHeightForWidth())
        self.label_description.setSizePolicy(sizePolicy)
        self.label_description.setObjectName("label_description")
        self.gridlayout.addWidget(self.label_description,3,0,1,1)

        self.line_edit_icons = QtGui.QLineEdit(PackageInfo)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit_icons.sizePolicy().hasHeightForWidth())
        self.line_edit_icons.setSizePolicy(sizePolicy)
        self.line_edit_icons.setObjectName("line_edit_icons")
        self.gridlayout.addWidget(self.line_edit_icons,5,1,1,1)

        self.text_edit_description = QtGui.QTextEdit(PackageInfo)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.text_edit_description.sizePolicy().hasHeightForWidth())
        self.text_edit_description.setSizePolicy(sizePolicy)
        self.text_edit_description.setObjectName("text_edit_description")
        self.gridlayout.addWidget(self.text_edit_description,3,1,1,1)

        self.label_idproj = QtGui.QLabel(PackageInfo)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_idproj.sizePolicy().hasHeightForWidth())
        self.label_idproj.setSizePolicy(sizePolicy)
        self.label_idproj.setObjectName("label_idproj")
        self.gridlayout.addWidget(self.label_idproj,0,0,1,1)

        self.line_edit_fullname = QtGui.QLineEdit(PackageInfo)
        self.line_edit_fullname.setObjectName("line_edit_fullname")
        self.gridlayout.addWidget(self.line_edit_fullname,2,1,1,1)

        self.list_categories = QtGui.QListWidget(PackageInfo)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.list_categories.sizePolicy().hasHeightForWidth())
        self.list_categories.setSizePolicy(sizePolicy)
        self.list_categories.setObjectName("list_categories")
        self.gridlayout.addWidget(self.list_categories,4,1,1,1)

        self.label_fullname = QtGui.QLabel(PackageInfo)
        self.label_fullname.setObjectName("label_fullname")
        self.gridlayout.addWidget(self.label_fullname,2,0,1,1)

        self.line_edit_version = QtGui.QLineEdit(PackageInfo)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_edit_version.sizePolicy().hasHeightForWidth())
        self.line_edit_version.setSizePolicy(sizePolicy)
        self.line_edit_version.setObjectName("line_edit_version")
        self.gridlayout.addWidget(self.line_edit_version,1,1,1,1)

        self.label_version = QtGui.QLabel(PackageInfo)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_version.sizePolicy().hasHeightForWidth())
        self.label_version.setSizePolicy(sizePolicy)
        self.label_version.setObjectName("label_version")
        self.gridlayout.addWidget(self.label_version,1,0,1,1)
        self.vboxlayout1.addLayout(self.gridlayout)

        self.label_properties = QtGui.QLabel(PackageInfo)
        self.label_properties.setObjectName("label_properties")
        self.vboxlayout1.addWidget(self.label_properties)

        self.tree_view_properties = QtGui.QTreeView(PackageInfo)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.tree_view_properties.sizePolicy().hasHeightForWidth())
        self.tree_view_properties.setSizePolicy(sizePolicy)
        self.tree_view_properties.setObjectName("tree_view_properties")
        self.vboxlayout1.addWidget(self.tree_view_properties)
        self.vboxlayout.addLayout(self.vboxlayout1)

        self.buttonBox = QtGui.QDialogButtonBox(PackageInfo)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(PackageInfo)
        QtCore.QMetaObject.connectSlotsByName(PackageInfo)

    def retranslateUi(self, PackageInfo):
        PackageInfo.setWindowTitle(QtGui.QApplication.translate("PackageInfo", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_icons.setText(QtGui.QApplication.translate("PackageInfo", "Icons", None, QtGui.QApplication.UnicodeUTF8))
        self.label_categories.setText(QtGui.QApplication.translate("PackageInfo", "Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.label_description.setText(QtGui.QApplication.translate("PackageInfo", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.label_idproj.setText(QtGui.QApplication.translate("PackageInfo", "Project Identifier", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fullname.setText(QtGui.QApplication.translate("PackageInfo", "Fullname", None, QtGui.QApplication.UnicodeUTF8))
        self.label_version.setText(QtGui.QApplication.translate("PackageInfo", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.label_properties.setText(QtGui.QApplication.translate("PackageInfo", "Properties", None, QtGui.QApplication.UnicodeUTF8))

