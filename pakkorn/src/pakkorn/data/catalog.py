
class Catalog(object) :
    """This class store every aspects of a pakkorn catalog which is a collection of packages"""
    
    def __init__(self, uri_catalog=None, packages=[]) :
        """Create a new catalog. Some packages (iterable) can be pass as arguments"""
    
        self._uri_catalog = uri_catalog
        self._packages = []
        self._idprojs = {}
        self._packages_by_idproj = {}
        self._packages_by_packagekeys = {}

        for package in packages :
            self.add_package(package)

    def add_package(self, package) :
        """Add a new package at the end of the catalog"""
        idproj = package.get_idproj()
        packagekeys = package.get_keys()

        if packagekeys in self._packages_by_packagekeys :
            oldpackage = self._idprojs[idproj]
            self._packages.remove(oldpackage)
            self._packages_by_idproj[idproj].remove(oldpackage)

        self._idprojs[idproj] = package

        self._packages.append(package)

        if idproj not in self._packages_by_idproj :
            self._packages_by_idproj[idproj] = []

        self._packages_by_idproj[idproj].append(package)

        self._packages_by_packagekeys[package.get_keys()] = package

    def iter_idprojs(self) :
        """Iterate threw all idprojs"""
        idprojs = self._idprojs.keys()
        idprojs.sort()
        return iter(idprojs)

    def iter_idproj(self,idproj) :
        """Iterate threw all packages with a given idproj"""
        if idproj not in self._packages_by_idproj :
            return iter([])
        return iter(self._packages_by_idproj[idproj])

    def __iadd__(self,catalog) :
        """Add a new catalog at the end of the current one"""
        for package in catalog :
            self.add_package(package)
        return self

    def __iter__(self) :
        """Iterate threw all packages"""
        return iter(self._packages)

    def __len__(self) :
        """return the number of packages in the catalog"""
        return len(self._packages)

    def __contains__(self,idproj) :
        """Check if an idproj (AND NOT A PACKAGE) is in the catalog"""
        return idproj in self._idprojs

    def __getitem__(self,index) :
        """Get a package with its index"""
        return self._packages[index]

    def __setitem__(self,index,package) :
        """Set a package with its index"""
        self._idprojs[package.get_idproj()] = index
        self._packages[index] = package

