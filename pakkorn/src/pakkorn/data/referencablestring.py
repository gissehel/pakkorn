class ReferencableString(object) :
    """This class store every aspects of a 'ReferencableString'.
       A ReferencableString is either a string, or a reference to a string.
       A reference to a string consist of an url to a web page, and a pattern (regexp)
       that extract the string.

       Referencable strings are used for Item, Version, Fullname, Description, etc."""

    def __init__(self,string=None,url=None,pattern=None,reference_container=None) :
        self._string = None
        self._pattern = None
        self._url = None
        self._reference_container = None
    
        if string is not None and (url is not None or pattern is not None) :
            raise ValueError('You must define either string, or url and pattern, not both')
        if string is None and (url is None or pattern is None) :
            raise ValueError('You must define either string, or url and pattern')
        if string is not None :
            self.set_string(string)
        else :
            self.set_reference(url,pattern)
            self.set_reference_container(reference_container)
    
    def is_string(self) :
        return self._string is not None
    
    def is_reference(self) :
        return self._url is not None
    
    def set_string(self,string) :
        if isinstance(string,ReferencableString) :
            if string.is_string() :
                self.set_string(string.get_string())
            elif string.is_reference() :
                (url,pattern) = string.get_reference()
                self.set_reference(url=url,pattern=pattern)
                if string.get_reference_container() is not None :
                    self.set_reference_container(string.get_reference_container())
            else :
                raise ValueError('argument is a ReferencableString but neither a string or a reference to a string')
        else :
            self._string = str(string)
            self._pattern = None
            self._url = None
    
    def set_reference(self,url,pattern) :
        self._string = None
        self._pattern = pattern
        self._url = url

    def set_reference_container(self,reference_container) :
        self._reference_container = reference_container

    def get_string(self) :
        return self._string
    
    def get_reference(self) :
        return (self._url,self._pattern)

    def get_reference_container(self) :
        return (self._reference_container)

    def __hash__(self) :
        if (self._string,self._url,self._pattern,self._reference_container) == (None,None,None,None) :
            return hash(None)
        elif self.is_string() :
            return hash(self._string)
        else :
            return hash((self._url,self._pattern,self._reference_container))

    def __eq__(self,element) :
        if element is None :
            return (self._string,self._url,self._pattern,self._reference_container) == (None,None,None,None)
        elif isinstance(element,ReferencableString) :
            return element._string == self._string and element._url == self._url and element._pattern == self._pattern and self._reference_container == element._reference_container
        elif isinstance(element,tuple) :
            return self.is_reference() and (((self._url,self._pattern) == element) or ((self._url,self._pattern,self._reference_container) == element))
        elif self.is_string() :
            return self._string == element

        return False
            
    def __str__(self) :
        return self._string

    def __repr__(self) :
        if self.is_string() :
            return 'ReferencableString(string=%r)' % (self._string,)
        elif self.is_reference() :
            return 'ReferencableString(url=%r,pattern=%r)' % (self._url,self._pattern)
        return 'ReferencableString()'
