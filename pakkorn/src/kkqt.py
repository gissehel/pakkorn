#!/usr/bin/env python

from PyQt4 import QtCore
from pakkorn.gui.qt.pakkorn import PakkornMainWindowBase
from pakkorn.gui.qt.pakkorn import start_application

from pakkorn.engine.engine import Engine
from pakkorn.engine.commandline import parse_command_line
from pakkorn.config import config

class PakkornMainWindowTest(PakkornMainWindowBase):
    CATEGORIE_ALL = "_ :: All packages"
    CATEGORIE_NONE = "_ :: No categories"

    def __init__(self, parent=None):
        self._engine = Engine(config)
        self._categories = set()
        super(PakkornMainWindowTest, self).__init__(parent)

        QtCore.QObject.connect(self.categoriesWidget,QtCore.SIGNAL("itemSelectionChanged()"),self.onCategorieChanged)
        QtCore.QObject.connect(self.push_update,QtCore.SIGNAL("clicked()"),self.onUpdate)
        QtCore.QObject.connect(self.push_download,QtCore.SIGNAL("clicked()"),self.onDownload)
        QtCore.QObject.connect(self.push_install,QtCore.SIGNAL("clicked()"),self.onInstall)
        QtCore.QObject.connect(self.searchFilter,QtCore.SIGNAL("editTextChanged(QString)"),self.onSearchChanged)

        self.refreshPackages()

    def refreshPackages(self) :
        self.detailWidget.clear()

        currentCategorie = None
        hascategorie = None

        currentCategorieItem = self.categoriesWidget.currentItem()
        if currentCategorieItem is not None :
            currentCategorie = currentCategorieItem.text()
            if currentCategorie == self.CATEGORIE_ALL :
                currentCategorie = None
            if currentCategorie == self.CATEGORIE_NONE :
                currentCategorie = None
                hascategorie = False

        # print "[%s]" % currentCategorie

        for package in self._engine.search(str(self.searchFilter.currentText()),categorie=currentCategorie,hascategorie=hascategorie) :
            self.addPackage([
                package.get_internal('downloaded')=='true' and 'D' or ' ',
                package.get_internal('installed')=='true' and 'I' or ' ',
                package.get_internal('lastcatalog')=='true' and 'L' or ' ',
                str(package.get_idproj()),
                str(package.get_fullname()),
                str(package.get_version()),
                ])

        categories = self._engine.get_all_categories()
        if self._categories != categories :
            categories = list(categories)
            categories.sort()
            self._categories = set(categories)
            self.categoriesWidget.clear()
            self.addCategorie(self.CATEGORIE_ALL)
            self.addCategorie(self.CATEGORIE_NONE)
            for categorie in categories :
                self.addCategorie(categorie)

    def onCategorieChanged(self) :
        self.refreshPackages()

    def onSearchChanged(self,newtext) :
        self.refreshPackages()

    def onUpdate(self) :
        self._engine.update()
        self.refreshPackages()

    def onDoCommandName(self,command_name) :
        currentItem = self.detailWidget.currentItem()
        if currentItem is not None :
            package_params = []
            package_param = {
                'idproj': str(currentItem.text(3)),
                'version': str(currentItem.text(5))
                }
            package_params.append(package_param)
            error = self._engine.do_commands_name(command_name,*package_params)
            if error is not None :
                raise Exception(error)
        self.refreshPackages()

    def onDownload(self) :
        self.onDoCommandName('download_install')

    def onInstall(self) :
        self.onDoCommandName('install')
        #self.addPackage("//L/gimp/The xGimp/4.2.2".split("/"))

parse_command_line(lambda :start_application(PakkornMainWindowTest))
