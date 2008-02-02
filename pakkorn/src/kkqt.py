#!/usr/bin/env python

from PyQt4 import QtCore
from PyQt4 import QtGui
from pakkorn.gui.qt.pakkorn import PakkornMainWindowBase
from pakkorn.gui.qt.pakkorn import start_application
from pakkorn.gui.qt.package_info import PackageInfoBase

from pakkorn.engine.engine import Engine
from pakkorn.engine.commandline import parse_command_line
from pakkorn.config import config

PackageInfoBase

class PakkornStatus (object):
    READY = 0
    UPDATING = 1
    DOWNLOADING = 2
    INSTALLING = 3
    UNINSTALLING = 4
    SEARCHING = 5


class PackageInfo(PackageInfoBase) :
    def disable_edit(self) :
        self.line_edit_idproj.setReadOnly(True)
        self.line_edit_version.setReadOnly(True)
        self.line_edit_fullname.setReadOnly(True)
        self.text_edit_description.setReadOnly(True)
        #self.list_categories.setReadOnly(True)
        self.line_edit_icons.setReadOnly(True)
        
    def set_package(self,package) :

        idproj = package.get_idproj()
        self.line_edit_idproj.setText(idproj)
        
        version = package.get_version()
        self.line_edit_version.setText(unicode(version))
        
        fullname = package.get_fullname()
        self.line_edit_fullname.setText(unicode(fullname))
        
        description = package.get_description()
        self.text_edit_description.setText(unicode(description))
        
        for category in package.iter_categories() :
            self.list_categories.addItem(unicode(category))

        icon_string_list = []
        for iconsize in package.iter_iconsizes() :
            icon = package.get_icon(iconsize)
            icon_string_list.append("%s : %s" % (iconsize,icon))
        icon_string = ", ".join(icon_string_list)
        self.line_edit_icons.setText(unicode(icon_string))

        for property_name in package.iter_properties() :
            property_value = package.get_property(property_name)
            
            self._property_model.appendRow(QtGui.QStandardItem(""))
            idrow = self._property_model.rowCount()-1
            for column,value in enumerate((property_name,property_value)) :
                self._property_model.setData(self._property_model.index(idrow, column), QtCore.QVariant(unicode(value)))

class PakkornMainWindow(PakkornMainWindowBase):
    CATEGORIE_ALL = "_ :: All packages"
    CATEGORIE_NONE = "_ :: No categories"

    def __init__(self, parent=None):
        self._engine = Engine(config)
        self._engine.event_error += self.on_error
        self._engine.event_downloading += self.on_download
        self._engine.event_installing += self.on_install
        self._engine.event_uninstalling += self.on_uninstall

        self._categories = set()
        self._current_status = PakkornStatus.READY
        self._current_status_args = {}

        super(PakkornMainWindow, self).__init__(parent)

        QtCore.QObject.connect(self.categoriesWidget,QtCore.SIGNAL("itemSelectionChanged()"),self.on_categorie_changed)
        QtCore.QObject.connect(self.push_update,QtCore.SIGNAL("clicked()"),self.on_action_update)
        QtCore.QObject.connect(self.push_download,QtCore.SIGNAL("clicked()"),self.on_action_download)
        QtCore.QObject.connect(self.push_install,QtCore.SIGNAL("clicked()"),self.on_action_install)
        QtCore.QObject.connect(self.searchFilter,QtCore.SIGNAL("editTextChanged(QString)"),self.on_search_changed)
        QtCore.QObject.connect(self.detailWidget,QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*,int)"),self.on_action_package_info)
        #on_action_package_info

        self.refreshPackages()

    def changeStatus(self,status,**kwargs):
        busy = False
        if status == PakkornStatus.READY :
            busy = True
        # TODO : use busy to change the cursor
        busy # unused

        self._current_status = status
        self._current_status_args = kwargs

        messages = {
            PakkornStatus.READY : 'Ready',
            PakkornStatus.UPDATING : 'Updating %(idproj)s',
            PakkornStatus.DOWNLOADING : 'Downloading %(idproj)s',
            PakkornStatus.INSTALLING : 'Installing %(idproj)s',
            PakkornStatus.UNINSTALLING : 'Installing %(idproj)s',
            PakkornStatus.SEARCHING : 'Searching database',
            }

        self.statusbar.showMessage(messages[self._current_status] % self._current_status_args)

    def refreshPackages(self) :
        self.detailWidget.clear()

        self.changeStatus(PakkornStatus.SEARCHING)

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

        self.changeStatus(PakkornStatus.READY)

    def on_categorie_changed(self) :
        self.refreshPackages()

    def on_search_changed(self,newtext) :
        self.refreshPackages()

    def on_action_update(self) :
        self._engine.update()
        self.refreshPackages()

    def do_command_name(self,command_name) :
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
                self.on_error(error)
                # raise Exception(error)
        self.refreshPackages()

    def on_error(self,message):
        QtGui.QMessageBox.critical(None,"Error",message)

    def on_action_download(self) :
        self.do_command_name('download_install')
        self.changeStatus(PakkornStatus.READY)

    def on_action_install(self) :
        self.do_command_name('install')
        #self.addPackage("//L/gimp/The xGimp/4.2.2".split("/"))

    def on_action_package_info(self,item,pos) :
        # package_info = PackageInfoBase()
        package_param = {
            'idproj': str(item.text(3)),
            'version': str(item.text(5))
        }
        packages = self._engine.get_packages_by_package_param(package_param)
        if len(packages) == 0 :
            self.on_error('No package found for "%(idproj)s" version "%(version)s"' % package_param)
        else :
            for package in packages :
                package_info = PackageInfo(self)
                package_info.disable_edit()
                package_info.set_package(package)
                package_info.setModal(True)
                package_info.exec_()
                
        
        
    def on_download(self,idproj='???') :
        self.changeStatus(PakkornStatus.DOWNLOADING,idproj=idproj)
    def on_install(self,idproj='???') :
        self.changeStatus(PakkornStatus.INSTALLING,idproj=idproj)
    def on_uninstall(self,idproj='???') :
        self.changeStatus(PakkornStatus.UNINSTALLING,idproj=idproj)

parse_command_line(lambda :start_application(PakkornMainWindow))
