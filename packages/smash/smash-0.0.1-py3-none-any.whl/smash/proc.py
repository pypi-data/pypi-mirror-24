#-- smash.process

"""
subprocess utilities
"""


import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import psutil

from .config import Config

from collections import OrderedDict

from .profile.default import extension_handler

#----------------------------------------------------------------------#

__all__ = []

def export( obj ) :
    __all__.append( obj.__name__ )
    return obj


#----------------------------------------------------------------------#

SUBPROCESS_DELAY = 0.01
@export
def execute( command_string: str, env=None ) -> (int, list) :
    # command = shlex.split(command_string)
    proc = subprocess.Popen( command_string, env=env, shell=True )
    pid_shell = proc.pid

    # collect child pids so they can be stored for later termination
    pids_children = [process.pid for process in psutil.Process( pid_shell ).children( recursive=True )]

    time.sleep( SUBPROCESS_DELAY )
    proc.terminate( ) #terminate exterior shell
    proc.wait( )
    return pid_shell, pids_children


@export
def service( command_string: str, env=None ) -> (int, list) :
    return None, None


@export
def kill_all( pids: list ) :
    for pid in pids :
        os.kill( pid, signal.SIGTERM )


#----------------------------------------------------------------------#

@export
def build_configs( path_root:Path ):

    print("BUILD CONFIG -----------")
    try:
        config = Config.from_yaml( path_root )
    except FileNotFoundError as e:
        if 'ONE_TICK_CONFIG' not in os.environ:
            raise e
        else:
            return Config()

    print("config", config)
    path_config = path_root / '.omd'
    try :
        path_config.mkdir( )
    except FileExistsError as e :
        pass


    config.write( filepath_config )
    config.write( filepath_config_raw, raw=True )


    ### CONFIG -- Locator file
    # ToDo

    ### CONFIG -- Access Control
    # ToDo:


    return config


@export
def build_subenv( path_root:Path, config:Config, pure_mode=False ):
    if not pure_mode:
        subenv = os.environ.copy( )
    else:
        subenv = OrderedDict()

    try:
        for (key, value) in config.data['shell'].items():
            subenv[key] = value
    except KeyError as e:
        pass

    # ToDo: construct pythonpath
    # ToDo: construct pythonhome
    # ToDo: construct path


    return subenv


#----------------------------------------------------------------------#

# ToDo: pooling of service ports
# How do I synchronize knowledge of the ports that processes distributed across hosts need?
# Need a cluster-level config layer

@export
def run_service_yaml( cwd: Path, verbose=False ) -> list :
    children = None

    return children


#----------------------------------------------------------------------#

@export
def run_cmd( working_dir:Path, command:str, *, verbose=False, pure_mode=False ) -> list :
    command_string = command # ToDo: clean up the args dict

    # ToDo: merge config files -- locator, acl
    ### figure out working directory, and add it to path

    sys.path.append( str( working_dir ) )
    os.chdir( str( working_dir ) )

    config  = build_configs( working_dir )
    subenv  = build_subenv( working_dir, config, pure_mode=pure_mode )

    print( "WORKDIR:", working_dir )
    print( "COMMAND:", command )

    if verbose:
        print( "SUBENV: " )
        for item in sorted(subenv.items()):
            print(str(item))

    _, children = execute( command_string, env=subenv )
    return children


#----------------------------------------------------------------------#

@export
def run_open( filename, verbose=False, pure_mode=False ) -> list :

    path_file = Path(filename).resolve().parents[0]

    print("File:", filename)
    extension=str(filename).split('.', maxsplit=1)[-1]
    print("EXTENSION", extension)

    # Select command by extension
    command = ""
    children = None

    if extension == "yaml" :
        run_service_yaml( path_file, verbose=verbose)
        # Todo: keep service loop running
    else:
        command = extension_handler(extension, filename)

        children = run_cmd( path_file, command, verbose=verbose, pure_mode=pure_mode )
    return children


#----------------------------------------------------------------------#
