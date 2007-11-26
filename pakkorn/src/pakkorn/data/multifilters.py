class MultiFilters(object) :
    """This class can contains several filters to check a collection of instances with each time the same filters.
    
    A multifilters is a list of contraints ordered by "set"s.
    
    When you 'check_filters' of a multifilters, you need to have at least one set that verify all constraints for the check to be valid.
    
    For exemple , let's suppose you call :
        multifilters = MultiFilters()
        multifilters.add_filter(firstvalueis=8)
        multifilters.add_filter(secondvalueisatleast=5)
        multifilters.define_new_set()
        multifilters.add_filter(firstvalueis=7)
        multifilters.add_filter(thirdvalueisnot=23)
        
    You can read it as "You need to have firstvalueis valid with 8 and secondvalueisatleast valid with 5, or firstvalueis valid with 7 and thirdvalueisnot valid with 23".
    You can read it as "You need to have first value 8 and second value at least 5, or first value 7 and third value not 23".
    
    You need a constraints dictionnary to be able to check an object, for example :
        constaints = {
            # firstvalueis is "first element of the object is equal to value"
            'firstvalueis' : lambda object,value : object[0]==value,
            # secondvalueisatleast is "second element of the object is equal to value"
            'secondvalueisatleast' : lambda object,value : object[1]>=value,
            # thirdvalueisnot is "third element of the object is equal to value"
            'thirdvalueisnot' : lambda object,value : object[2]!=value,
            }

    Then, you can check several values :
        test1 = (8,6,12)
        test2 = (7,4,24)
        test3 = (7,4,23)
        test4 = (8,5,23)
        test3 = (8,4,12)
        
        >>> print multifilters.check_filters(test1,constaints)
        True

        >>> print multifilters.check_filters(test2,constaints)
        True

        >>> print multifilters.check_filters(test3,constaints)
        False

        >>> print multifilters.check_filters(test4,constaints)
        True

        >>> print multifilters.check_filters(test5,constaints)
        False

    You can replace :
        multifilters = MultiFilters()
        multifilters.add_filter(firstvalueis=8)
        multifilters.add_filter(secondvalueisatleast=5)
    by :
        multifilters = MultiFilters()
        multifilters.add_filter(firstvalueis=8,secondvalueisatleast=5)
    and even by :
        multifilters = MultiFilters(firstvalueis=8,secondvalueisatleast=5)

    """
    def __init__(self,**filter_struct) :
        self._filters = []
        self._filters_set = [self._filters]
        self._empty = True

        if len(filter_struct)>0 :
            self.add_filter(**filter_struct)

    def add_filter(self,**filter_struct) :
        if len(filter_struct) != 0 :
            self._empty = False
            self._filters.append(filter_struct)

    def define_new_set(self,**filter_struct) :
        if len(self._filters) > 0 :
            self._filters = []
            self._filters_set.append(self._filters)

        if len(filter_struct)>0 :
            self.add_filter(**filter_struct)

    def iter_filters_set(self) :
        # TODO : Change this to not access directly to attributes
        return iter(self._filters_set)

    def check_filters(self,element,constraints) :
        for filters in self._filters_set :
            result = True

            for filter_struct in filters :
                for key in filter_struct :
                    if key[:1] in '-_' :
                        result = result and not constraints[key[1:]](element,filter_struct[key])
                    else :                        
                        result = result and constraints[key](element,filter_struct[key])

            if result :
                # I'm stopping iterations here for performances reasons
                return True

        return False

    def is_empty(self) :
        return self._empty
