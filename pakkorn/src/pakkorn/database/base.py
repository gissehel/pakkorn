from pakkorn.data import MultiFilters

class Database(object) :
    """Base class for all pakkorn databases"""
    def __init__(self,path) :
        pass
        
    def update(self,catalog) :
        """Update database with the given catalog"""
        pass

    def search(self,multifilters=None,**kwargs) :
        """Search the database with several parameters (see Package.constraints for a full list)"""

        if multifilters is None :
            multifilters = MultiFilters(**kwargs)

        # _search only takes a multifilters
        return self._search(multifilters)
        
    def change(self,package) :
        """Change the status of a given package"""
        pass
        
    def get_categories(self) :
        """Get all the categories"""
        return []

