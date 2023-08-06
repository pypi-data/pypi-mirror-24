#-- smash.sys.plugins

"""
load plugins
"""


import logging
log = logging.getLogger( name="smash.sys.plugins" )
logging.basicConfig( level=logging.DEBUG )
log.debug = print
# log.debug = lambda *a, **b : None


#----------------------------------------------------------------------#

__all__ = []

def export( obj ) :
    try :
        __all__.append( obj.__name__ )
    except AttributeError :
        __all__.append( obj.__main__.__name__ )
    return obj

#----------------------------------------------------------------------#


#----------------------------------------------------------------------#
