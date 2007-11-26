from pakkorn.data import ReferencableString
from pakkorn.data import Commands

class Package(object) :
    """This class store every aspects of a pakkorn package"""

    constraints = {
        'idproj' : lambda self,value : self.get_idproj()==value,
        'version' : lambda self,value : self.get_version()==value,
        'fullname' : lambda self,value : str(value).lower() in str(self.get_fullname()).lower(),
        'substring' : lambda self,value : str(value).lower() in str(self.get_description()).lower() or str(value).lower() in str(self.get_fullname()).lower() or str(value).lower() in str(self.get_idproj()).lower(),
        'installed' : lambda self,value : (self.has_internal('installed') and (self.get_internal('installed')=='true'))==value,
        'lastcatalog' : lambda self,value : (self.has_internal('lastcatalog') and (self.get_internal('lastcatalog')=='true'))==value,
        'categorie' : lambda self,value : value in self.iter_categories(),
        'hascategorie' : lambda self,value : (len(list(self.iter_categories()))!=0) == value,
        }

    def __init__(self, idproj=None) :
        """Create a new package. May take an optional project id"""

        self._idproj = idproj
        self._version = None
        self._fullname = None
        self._description = None
        self._items = {}
        self._commands_set = {}
        self._categories = set()
        self._icons = {}
        self._properties = {}
        self._internals = {}
        
        self._base_url = None
        self._base_urls_used = []
        
    def clone(self,instance=None) :
        """Return a new package with exactly the same values"""
        if instance is None :
            instance = Package(self._idproj)

        instance._idproj       = self._idproj 
        instance.set_version(self._version)
        instance.set_fullname(self._fullname)
        instance.set_description(self._description)
        instance.set_version(self._version)
        instance._items        = {}
        for item_name in self._items :
            instance.set_item(item_name,self._items[item_name])
        instance._commands_set = {}
        for commands_name in self._commands_set :
            instance._commands_set[commands_name] = Commands(commands=self._commands_set[commands_name])
        instance._categories   = set(self._categories)
        instance._icons        = self._icons.copy()
        instance._properties   = self._properties.copy()
        instance._internals    = self._internals.copy()
        instance._base_url     = self._base_url
        instance._base_urls_used = self._base_urls_used

        return instance

    def get_idproj(self) :
        "Get the idproj value of the package"
        return self._idproj

    def set_idproj(self,idproj) :
        "Set the idproj value of the package"
        self._idproj = idproj

    def get_version(self) :
        "Get the version of the package"
        return self._version

    def set_version(self,version) :
        "Set the version of the package"
        if version is None :
            self._version = None
        else :
            self._version = ReferencableString(string=version)

    def get_fullname(self) :
        "Get the fullname of the package"
        return self._fullname

    def set_fullname(self,fullname) :
        "Set the fullname of the package"
        if fullname is None :
            self._fullname = None
        else :
            self._fullname = ReferencableString(string=fullname)

    def get_description(self) :
        "Get the description of the package"
        return self._description

    def set_description(self,description) :
        "Set the description of the package"
        if description is None :
            self._description = None
        else :
            self._description = ReferencableString(string=description)

    def iter_itemnames(self) :
        "Iter threw item names"
        sorted_keys = self._items.keys()
        sorted_keys.sort()
        return iter(sorted_keys)

    def get_item(self,itemname) :
        "Get an item from the package"
        return self._items[itemname]

    def set_item(self,itemname,item) :
        "Set an item into the package"
        if item is None :
            self._items[itemname] = None
        else :
            self._items[itemname] = ReferencableString(string=item)
        
    def del_item(self,itemname) :
        "Delete an item from the package"
        del self._items[itemname]

    def iter_commands_names(self) :
        "Iterate threw commands names"
        sorted_keys = self._commands_set.keys()
        sorted_keys.sort()
        return iter(sorted_keys)

    def get_commands(self,commands_name) :
        "Get the commands named commands_name"
        return self._commands_set[commands_name]

    def set_commands(self,commands_name,commands) :
        "Set the commands named commands_name"
        self._commands_set[commands_name] = commands

    def has_commands(self,commands_name) :
        "Test if the commands named commands_name exists"
        return commands_name in self._commands_set

    def iter_categories(self) :
        "Iterate threw categories"
        sorted_keys = list(self._categories)
        sorted_keys.sort()
        return iter(sorted_keys)

    def add_category(self,category) :
        "Add a new category"
        self._categories.add(category)

    def del_category(self,category) :
        "Delete an existing category"
        self._categories.remove(category)

    def iter_iconsizes(self) :
        "Iterate threw icon sizes"
        sorted_keys = self._icons.keys()
        sorted_keys.sort()
        return iter(sorted_keys)

    def get_icon(self,size) :
        "Add the icon url for the given size"
        return self._icons[size]

    def set_icon(self,size,icon) :
        "Set the icon url for the given size"
        self._icons[size] = icon

    def del_icon(self,size) :
        "Delete the icon for the given size"
        del self._icons[size]

    def iter_properties(self) :
        "Iterate threw all property names"
        sorted_keys = self._properties.keys()
        sorted_keys.sort()
        return iter(sorted_keys)

    def get_property(self,property) :
        "Get the value for the given property"
        return self._properties[property]

    def set_property(self,property,value) :
        "Set the value for the given property"
        self._properties[property] = value

    def del_property(self,property) :
        "Delete the given property"
        del self._properties[property]

    def has_property(self,property) :
        "Test if the given property exists"
        return property in self._properties

    def iter_internals(self) :
        "Iterate threw all internals names"
        sorted_keys = self._internals.keys()
        sorted_keys.sort()
        return iter(sorted_keys)

    def get_internal(self,name) :
        "Get the value for the given internal name"
        return self._internals[name]

    def set_internal(self,name,value) :
        "Set the value for the given internal name"
        self._internals[name] = value

    def del_internal(self,name) :
        "Delete the given internal name"
        del self._internals[name]

    def has_internal(self,name) :
        "Test if the given internal name exists"
        return name in self._internals

    def has_internals(self) :
        "Test if there is any internal name"
        return len(self._internals)>0

    def get_base_url(self) :
        "Get the url of the package to use"
        return self._base_url

    def set_base_url(self,base_url) :
        "Set the url of the package to use"
        self._base_url = base_url

    def get_keys(self) :
        "Return keys that really identifies two packages as being the same. For now, it's only idproj and version"
        return (self._idproj,self._version)

    def __eq__(self,package) :
        "Test if another package is the same as this package (currently defined by the fact that idproj and version are the same)"
        try :
            return self.get_keys() == package.get_keys()
        except AttributeError :
            pass
        return False
