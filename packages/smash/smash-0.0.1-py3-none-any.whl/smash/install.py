#-- smash.install

"""
installation procedures
"""


import logging

log = logging.getLogger( name="smash.install" )
logging.basicConfig( level=logging.DEBUG )
log.debug = print
# log.debug = lambda *a, **b : None


#----------------------------------------------------------------------#

def register_script_to_context_menu( ) :
    # http://support.microsoft.com/kb/310516
    cmd_line = 'regedit.exe registerOne.reg'
    import os
    os.system( cmd_line )

#----------------------------------------------------------------------#



#----------------------------------------------------------------------#
