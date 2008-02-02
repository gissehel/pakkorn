import os
import shutil
from pakkorn.data import Catalog
from pakkorn.data import Package
from pakkorn.dataxml.dataxml import Xml
from pakkorn.engine import WebDownloader
from pakkorn.database.asxml import Database
from pakkorn.data import MultiFilters
import re

RE_VARIABLE = re.compile(r'\$\{(.*?)\}')

class Error(object) :
    NO_PACKAGE_FOUND = "No package found"
    TOO_MANY_PACKAGES_FOUND = "Too many packages found"
    NOT_IMPLEMENTED = "Not implemented"
    PROBLEM_DOWNLOADING = "There is a problem downloading a file"


class Engine(object) :
    """Main pakkorn engine"""

    def __init__(self,config) :
        self._config = config
        self._working_dir = os.path.join(self._config['userdatapath'])

        self._database_dir = os.path.join(self._working_dir,'base')
        self._download_dir = os.path.join(self._working_dir,'download')
        self._cache_dir = os.path.join(self._working_dir,'cache')

        for dirname in (self._database_dir,self._download_dir,self._cache_dir) :
            if not(os.path.exists(dirname)) :
                os.makedirs(dirname)

        self._database_instance = None
        self._web_downloader = WebDownloader(self._config,cache=self._cache_dir)
        self._reference_problem = False

    def _database(self) :
        if self._database_instance is None :
            self._database_instance = Database(self._database_dir)
        return self._database_instance

    def update(self) :
        '''Update de database catalog'''
        uri = self._get_update_uri()
        download_id = self._web_downloader.add_donwload(uri)
        self._web_downloader.wait(download_id)
        filename = self._web_downloader.get_filename(download_id)
        self._web_downloader.clean()

        xml = Xml(filename=filename)
        catalog = xml.read()
        self._database().update(catalog)

        self._web_downloader.expire(uri)

    def search(self,search_string,categorie=None,hascategorie=None) :
        multifilters = MultiFilters()
        multifilters.add_filter(idproj=search_string)
        if categorie is not None :
            multifilters.add_filter(categorie=categorie)
        if hascategorie is not None :
            multifilters.add_filter(hascategorie=hascategorie)

        multifilters.define_new_set()
        multifilters.add_filter(fullname=search_string)
        if categorie is not None :
            multifilters.add_filter(categorie=categorie)
        if hascategorie is not None :
            multifilters.add_filter(hascategorie=hascategorie)

        multifilters.define_new_set()
        multifilters.add_filter(substring=search_string)
        if categorie is not None :
            multifilters.add_filter(categorie=categorie)
        if hascategorie is not None :
            multifilters.add_filter(hascategorie=hascategorie)

        return self._database().search(multifilters)

    def show(self,search_string,version=None) :
        multifilters = MultiFilters()
        multifilters.add_filter(idproj=search_string)
        if version is not None :
            multifilters.add_filter(version=version)

        return self._database().search(multifilters)

    def do_commands_name(self,commands_name,*package_params) :
        '''used for commands_name="install" or commands_name="uninstall" '''

        packages = []
        for package_param in package_params :
            multifilters = MultiFilters(lastcatalog=True)
            if 'idproj' in package_param :
                multifilters.add_filter(idproj=package_param['idproj'])
            if 'version' in package_param :
                multifilters.add_filter(version=package_param['version'])
            sub_packages = list(self._database().search(multifilters))
            if len(sub_packages) == 0 :
               return "No package found for %s version %s" % (package_param.get('idproj','?'),package_param.get('version','?'))
            elif len(sub_packages) > 1 :
               return "Too many package found for %s version %s" % (package_param.get('idproj','?'),package_param.get('version','?'))
            packages.append(sub_packages[0])
        if commands_name in ('install','uninstall') :
            return self._apply_commands(commands_name, *packages)
        elif commands_name == 'download_install' :
            return self.download_install(*packages)

    def download_install(self, *packages) :
        error = self._download(usage='install',*packages)
        return error

    def _apply_commands(self, commands_name, *packages) :
        error = None
        for package in packages :
            if not(package.has_commands(commands_name)) :
                error = "Don't know how to %s %s version %s" % (commands_name,package.get_idproj(),package.get_version())

        if error is None :
            error = self._download(usage=commands_name,*packages)
            if error is None :
                items = self._get_item_informations(usage=commands_name,*packages)
                for package in packages :
                    if not(self._exec_commands(commands_name,package,items)) :
                        error = "Can't %s %s version %s" % (commands_name,package.get_idproj(),package.get_version())
                        break
        return error


    def _download(self, *packages, **kwargs) :
        usage = kwargs.get('usage',None)
        items = self._get_item_informations(usage=usage,*packages)
        download_ids = {}

        for packagekey in items :
            for itemname in items[packagekey] :
                if not(os.path.exists(items[packagekey][itemname]['itemfilename'])) :
                    download_ids[(packagekey,itemname)] = self._web_downloader.add_donwload(url=items[packagekey][itemname]['item'])

        for packagekey,itemname in download_ids :
            download_id = download_ids[(packagekey,itemname)]
            self._web_downloader.wait(download_id)
            filename = self._web_downloader.get_filename(download_id)
            if filename is not None :
                shutil.move(filename,items[packagekey][itemname]['itemfilename'])

        self._web_downloader.clean()

        error = None

        for package in packages :
            packagekey = (str(package.get_idproj()),str(package.get_version()))

            allitems_ok = True
            for itemname in items[packagekey] :
                if not(os.path.exists(items[packagekey][itemname]['itemfilename'])) :
                    error = Error.PROBLEM_DOWNLOADING
                    allitems_ok = False
            if allitems_ok :
                package.set_internal('downloaded','true')
                self._database().change(package)

        return error

    def _exec_commands(self,commands_name,package,items) :
        commands = package.get_commands(commands_name)
        idproj = str(package.get_idproj())
        version = str(package.get_version())

        status_result = True

        local_items = {}
        for itemname in items[(idproj,version)] :
            local_items[itemname] = items[(idproj,version)][itemname]['itemfilename']

        for command in commands :
            command = str(command).replace('%','%%')
            for variable in list(RE_VARIABLE.findall(command)) :
                command = command.replace("${%s}"%variable,'"%%(%s)s"'%variable)

            status_result = self._exec(command % local_items)
            if not(status_result) :
                break

        if status_result and commands_name == 'install' :
            package.set_internal('installed','true')
            self._database().change(package)

        if status_result and commands_name == 'uninstall' :
            package.set_internal('installed','false')
            self._database().change(package)

        return status_result

    def _exec(self,command_line) :
        # print "EXEC:[%s]" % (command_line,)
        handle = os.popen(command_line)
        list(handle)
        result_code = handle.close()
        return (result_code is None)

    def _get_item_informations(self,*packages,**kwargs) :
        items = {}
        usage = None
        if 'usage' in kwargs :
            usage = kwargs['usage']
        for package in packages :
            itemname_set = None
            if usage is not None :
                itemname_set = set()
                if package.has_commands(usage) :
                    for command in package.get_commands(usage) :
                        for variable in list(RE_VARIABLE.findall(str(command))) :
                            itemname_set.add(variable)
            package_key = (str(package.get_idproj()),str(package.get_version()))
            items[package_key] = {}
            package_dir = os.path.join(self._download_dir,str(package.get_idproj()),str(package.get_version()))
            if not(os.path.exists(package_dir)) :
                os.makedirs(package_dir)
            for itemname in package.iter_itemnames() :
                if (itemname_set is None) or (itemname in itemname_set) :
                    item = str(package.get_item(itemname))
                    itembasefilename = item.split('/')[-1]
                    itemfilename = os.path.join(package_dir,itembasefilename)
                    items[package_key][itemname] = {
                        'item' : item,
                        'itemname' : itemname,
                        'itembasefilename' : itembasefilename,
                        'itemfilename' : itemfilename
                        }
        return items
    def upgrade(self) :
        pass

    def aggregate(self,uri,output_filename) :
        try :
            download_id = self._web_downloader.add_donwload(uri)
            self._web_downloader.wait(download_id)
            filename = self._web_downloader.get_filename(download_id)

            xml = Xml(filename=filename)
            catalog = xml.read()

            new_catalog = Catalog()

            for package in catalog :
                new_package = package.clone()
                idproj = package.get_idproj()

                base_url = new_package.get_base_url()

                base_urls = set()

                while base_url is not None :

                    new_package.set_base_url(None)

                    if (base_url is not None) and (base_url not in base_urls):
                        base_package = None

                        base_urls.add(base_url)

                        download_id = self._web_downloader.add_donwload(base_url)
                        self._web_downloader.wait(download_id)
                        filename = self._web_downloader.get_filename(download_id)

                        if filename is not None :
                            xml = Xml(filename=filename)
                            pakkorn_element = xml.read()
                            self._web_downloader.expire(base_url)

                            if isinstance(pakkorn_element,Catalog) :
                                if idproj in pakkorn_element :
                                    # TODO : decide what to do when len(list(pakkorn_element.iter_idproj(idproj))) > 1
                                    base_package = list(pakkorn_element.iter_idproj(idproj))[0]
                                else :
                                    # TODO : else what ?
                                    pass
                            elif isinstance(pakkorn_element,Package) :
                                if pakkorn_element.get_idproj() == idproj :
                                    base_package = pakkorn_element
                                else :
                                    # TODO : else what ?
                                    pass
                            if base_package is not None :
                                if new_package.get_version() is None :
                                    new_package.set_version(base_package.get_version())
                                if new_package.get_fullname() is None :
                                    new_package.set_fullname(base_package.get_fullname())
                                if new_package.get_description() is None :
                                    new_package.set_description(base_package.get_description())

                                if len(list(new_package.iter_itemnames()))==0 :
                                    for itemname in base_package.iter_itemnames() :
                                        new_package.set_item(itemname,base_package.get_item(itemname))

                                if len(list(new_package.iter_commands_names()))==0 :
                                    for commands_name in base_package.iter_commands_names() :
                                        new_package.set_commands(commands_name,base_package.get_commands(commands_name))

                                if len(list(new_package.iter_categories()))==0 :
                                    for category in base_package.iter_categories() :
                                        new_package.add_category(category)

                                if len(list(new_package.iter_iconsizes()))==0 :
                                    for size in base_package.iter_iconsizes() :
                                        new_package.set_icon(size,base_package.get_icon(size))

                                if len(list(new_package.iter_properties()))==0 :
                                    for property in base_package.iter_properties() :
                                        new_package.set_property(property,base_package.get_property(property))

                                if new_package.get_base_url() is None :
                                    new_package.set_base_url(base_package.get_base_url())

                            else :
                                # TODO : else what ?
                                pass

                    base_url = new_package.get_base_url()

                self._reference_problem = False
                version = self.get_unreferenced_string(new_package.get_version())
                fullname = self.get_unreferenced_string(new_package.get_fullname())
                description = self.get_unreferenced_string(new_package.get_description())

                new_package.set_version(version)
                new_package.set_fullname(fullname)
                new_package.set_description(description)

                for itemname in new_package.iter_itemnames() :
                    item = self.get_unreferenced_string(new_package.get_item(itemname))
                    if item is not None :
                        new_package.set_item(itemname,item)

                if self._reference_problem :
                    # TODO : Add the package from the previous aggregation with a special property
                    self.log("There is a problem in the package '%s' : package not added" % (idproj,))
                else :
                    new_catalog.add_package(new_package)


            xml = Xml(filename=output_filename)
            xml.write(new_catalog)
        finally :
            self._web_downloader.clean()

    def get_unreferenced_string(self,referencable_string) :
        unreferenced_string = None

        if referencable_string is not None :
            if referencable_string.is_reference() :
                unreferenced_string = None
                url,pattern = referencable_string.get_reference()

                download_id = self._web_downloader.add_donwload(url)
                self._web_downloader.wait(download_id)
                filename = self._web_downloader.get_filename(download_id)
                web_page = ""

                if filename :
                    handle = open(filename,'rb')
                    web_page = handle.read()
                    handle.close()

                values = re.findall(pattern,web_page)
                # TODO : Handle the case where len(values) == 0
                # TODO : Decide what to do when len(values) > 1

                if len(values) > 0 :
                    if referencable_string.get_reference_container() is None :
                        unreferenced_string = values[0]
                    else :
                        unreferenced_string = referencable_string.get_reference_container() % (values[0],)
                else :
                    self.log("No pattern '%s' found at '%s'" % (pattern,url))
                    self._reference_problem = True

                self._web_downloader.expire(url)
            else :
                unreferenced_string = referencable_string.get_string()
        else :
            self.log("Can't unreference None")
            self._reference_problem = True

        return unreferenced_string

    def log(self,message):
        print message

    def _get_update_uri(self) :
        #Mok !
        return "http://test.giss.mine.nu/pakkorn/engine/reference.pakkorn"

    def get_all_categories(self) :
        return self._database().get_categories()

def test():
    e = Engine(None)
    e.update()

if __name__=="__main__" :
    test()
