import os
from pakkorn.database.base import Database as BaseDataBase
from pakkorn.data import Catalog
from pakkorn.dataxml import Xml

LOCAL_BASE = 'local_catalog.pakkorn'
LOCAL_BASE_TMP = 'local_catalog_tmp.pakkorn'

class Database(BaseDataBase) :
    """Database implemented as xml"""
    def __init__(self,path) :
        """Create a new Database (using xml catalog)"""
        self._database_file = os.path.join(path,LOCAL_BASE)
        self._database_file_tmp = os.path.join(path,LOCAL_BASE_TMP)

        self._xml = Xml(filename=self._database_file,internals=True)
        self._xml_tmp = Xml(filename=self._database_file_tmp,internals=True)

        if os.path.exists(self._database_file) :
            self._catalog = self._xml.read()
        else :
            if os.path.exists(self._database_file_tmp) :
                self._catalog = self._xml_tmp.read()
            else :
                self._catalog = Catalog()
            self._write()

    def update(self,catalog) :
        """Update database with the given catalog"""
        new_catalog = Catalog()
        trash_catalog = Catalog()
        for idproj in self._catalog.iter_idprojs() :
            if idproj in catalog :
                # idproj is in both new catalog and old self._catalog
                packages = {}
                catalogs = {'old':self._catalog,'new':catalog}
                for catalog_type in catalogs :
                    # catalog_type is 'new' or 'old'
                    for package in catalogs[catalog_type].iter_idproj(idproj) :
                        version = package.get_version()
                        if version not in packages : 
                            packages[version] = {}
                        packages[version][catalog_type] = package
                for version in packages :
                    if 'new' in packages[version] and 'old' in packages[version] :
                        # For this version, there is a new and an old package
                        # We must migrate internal properties
                        
                        # TODO : If other items doesn't point to the same files, we must clean caches
                        
                        for name in packages[version]['old'].iter_internals() :
                            value = packages[version]['old'].get_internal(name)
                            packages[version]['new'].set_internal(name,value)

                        package = packages[version]['new']
                        package.set_internal(name='lastcatalog',value='true')
                        new_catalog.add_package(package)

                    elif 'new' in packages[version] :
                        # Only neeeeeewwwwww catalog contains this version
                        package = packages[version]['new']
                        package.set_internal(name='downloaded',value='false')
                        package.set_internal(name='installed',value='false')
                        package.set_internal(name='lastcatalog',value='true')
                        new_catalog.add_package(package)
                        pass
                    elif 'old' in packages[version] :
                        # Only old catalog contains this version
                        package = packages[version]['old']
                        if package.get_internal('installed')=='true' :
                            # If the package is currently installed, I'm adding it to the new catalog
                            package.set_internal(name='lastcatalog',value='false')
                            new_catalog.add_package(package)
                        else :
                            # If the package is not currently installed, I'm trashing it
                            trash_catalog.add_package(package)
                    else :
                        # We should never be here.
                        pass
                    
                pass
            else :
                # is only in old self._catalog, this is a removed package
                for package in self._catalog.iter_idproj(idproj) :
                    if package.get_internal('installed')=='true' :
                        # If the package is currently installed, I'm adding it to the new catalog
                        package.set_internal(name='lastcatalog',value='false')
                        new_catalog.add_package(package)
                    else :
                        # If the package is not currently installed, I'm trashing it
                        trash_catalog.add_package(package)

        for idproj in catalog.iter_idprojs() :
            if idproj not in self._catalog :
                # I'm only intersted in this case, this is a new package
                for package in catalog.iter_idproj(idproj) :
                    package.set_internal(name='downloaded',value='false')
                    package.set_internal(name='installed',value='false')
                    package.set_internal(name='lastcatalog',value='true')
                    new_catalog.add_package(package)


        self._catalog = new_catalog
        self._write()

        return trash_catalog
        
    def _search(self,multifilters) :
        """Search the database with only a multifilters"""

        for package in self._catalog :
            if multifilters.check_filters(package,package.constraints) :
                yield package.clone()

    def change(self,package,*args) :
        """Change the status of a given package"""
        #packages = list(self.search(idproj=package.get_idproj(),package.get_))
        self._catalog.add_package(package)
        for otherpackage in args :
            self._catalog.add_package(otherpackage)
        self._write()
        
    def _write(self,catalog=None) :
        """Write the database content within the database filename"""
        if catalog == None :
            catalog = self._catalog
        
        self._xml_tmp.write(self._catalog)
        if os.path.exists(self._database_file) :
            os.unlink(self._database_file)
        os.rename(self._database_file_tmp,self._database_file)

    def get_categories(self) :
        """Get all the categories"""
        categories = set()
        for package in self._catalog :
            categories.update(package.iter_categories())
        
        return categories
