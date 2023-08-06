
"""
manipulate configuration files
"""

import colorama
from termcolor import colored
colorama.init( )

import colored_traceback
colored_traceback.add_hook( )

import logging
log = logging.getLogger( name='smash.config' )
log.debug = lambda *a, **b : None
log.debug = print

################################

import re

from collections import OrderedDict

from pathlib import Path

from .yaml import load as load_yaml
from .path import stack_of_files

#----------------------------------------------------------------------#

parameter_expression_regex = re.compile(
r"""    \${                             # ${
        ((?P<namespace>[^{}]+?)::)?     #   namespace::         [optional]
        ((?P<section>[^:{}]+?):)?       #   section:            [optional]
        (?P<key>[^:{}]+?)               #   key                 -required-
        }                               #  }
""", re.VERBOSE)

####################

#----------------------------------------------------------------------#


class ConfigTree:
    """Immutable iterator over a network of configuration files with cross-tree references."""

    #----------------------------------------------------------------#
    #----------------------------------------------------------------#

    ####################
    def __init__( self, *
                  , root_file:     Path = None
                  , child_file:    Path = None
                  ) :

        self.nodes      = list()
        self.root       = None

        self.root_file  = root_file
        self.child_file = child_file

        if root_file is not None:
            self.__add_root(root_file)


    @classmethod
    def from_path( cls, target_path: Path ) :
        """Find the root file for a target path, load it and its children"""
        root_file = stack_of_files( target_path, '__root__.yml' )[0]
        self = cls( root=root_file )
        return self

    @classmethod
    def from_root( cls, root_file: Path ) :
        self = cls( root=root_file )
        return self

    @classmethod
    def from_child( cls, target_file: Path ) :

        self = cls( target=target_file )
        return self


    def  add_root(self, root_file):
        pass
    __add_root = add_root

    def add_child(self, child_file):
        pass
    __add_child = add_child

    #----------------------------------------------------------------#
    #----------------------------------------------------------------#


#----------------------------------------------------------------------#


class Config:
    """A single immutable configuration structure"""
    section_names       = ['pkg', 'path', 'shell', 'main']
    export_sections     = ['pkg', 'path', 'shell']
    write_sections      = ['shell', 'main']

    #----------------------------------------------------------------#
    #----------------------------------------------------------------#


    ####################
    def __init__( self ) :

        self.name       = None
        self.path       = None
        self.filepath   = None

        self.yaml_data  = None
        self.eval_data  = OrderedDict()
        self.flat_data  = OrderedDict()

        self.tree       = None
        self.parents    = OrderedDict()
        self.children   = OrderedDict()


    #----------------------------------------------------------------#
    #----------------------------------------------------------------#


    ####################
    def load( self, target: Path ) :

        self.filepath   = target
        self.path       = target.parents[0]
        self.name       = target.name

        log.debug(
            colored( '*'*80, 'green', attrs=['bold'] ),
            self.path
        )

        self.yaml_data = load_yaml( target )

        # for section_name in self.section_names :
        #     try :
        #         data = self.load_parameters( struct, section_name, path_target )
        #     except KeyError :
        #         data = OrderedDict( )

            # self.data_raw[section_name] = data
            # self.data[section_name] = data


    @classmethod
    def from_yaml( cls, target_file: Path ) :
        self = cls()
        self.load( target_file )
        return self


    @classmethod
    def from_root( cls, target_path: Path ):
        pass

    @classmethod
    def Tree( cls ) :
        pass

#----------------------------------------------------------------------#
