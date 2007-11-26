from pakkorn.config.config import ConfigClass
from pakkorn.config.register import register_type
from pakkorn.config.register import register_key
from pakkorn.config.register import ConversionException

config = ConfigClass()

register_key('binpath',str,doc='The binary path of the software', default=None, internal=True, advanced=True, never_save=True )
register_key('respath',str,doc='The ressource path of the software', default=None, internal=True, advanced=True )
register_key('userdatapath',str,doc='The path where userdata is stored', default=None, internal=True, advanced=True )
register_key('binname',str,doc='The binary name of the software', default=None, internal=True, advanced=True, never_save=True )

