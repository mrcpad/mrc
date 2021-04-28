#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@version: v0.1
@author: xxf
@site: 
@software: PyCharm
@file: 使用springpython框架，实现Ioc控制翻转，DI依赖注入
@time: 2019-7-26
"""

import os
import sys
from module.mrc_core.gloalConfig import GloalConfig
from springpython.context import ApplicationContext
from springpython.config import *
from logs.log import logger
import traceback


def import_class(import_str):
    """Returns a class from a string including module and class.
    .. versionadded:: 0.3
    """
    mod_str, _sep, class_str = import_str.rpartition('.')
    logger.info("__import__")
    __import__(mod_str)
    logger.info("__import__   end")
    try:
        cls =getattr(sys.modules[mod_str], class_str)
        return cls()
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))


def import_object(import_str, *args, **kwargs):
    """Import a class and return an instance of it.
    .. versionadded:: 0.3
    """
    return import_class(import_str)(*args, **kwargs)


def import_object_ns(name_space, import_str, *args, **kwargs):
    """Tries to import object from default namespace.
    Imports a class and return an instance of it, first by trying
    to find the class in a default namespace, then failing back to
    a full path if not found in the default namespace.
    .. versionadded:: 0.3
    .. versionchanged:: 2.6
       Don't capture :exc:`ImportError` when instanciating the object, only
       when importing the object class.
    """
    import_value = "%s.%s" % (name_space, import_str)
    try:
        cls = import_class(import_value)
    except ImportError:
        cls = import_class(import_str)
    return cls(*args, **kwargs)


def import_module(import_str):
    """Import a module.
    .. versionadded:: 0.3
    """
    __import__(import_str)
    return sys.modules[import_str]


def import_versioned_module(module, version, submodule=None):
    """Import a versioned module in format {module}.v{version][.{submodule}].
    :param module: the module name.
    :param version: the version number.
    :param submodule: the submodule name.
    :raises ValueError: For any invalid input.
    .. versionadded:: 0.3
    .. versionchanged:: 3.17
       Added *module* parameter.
    """

    # NOTE(gcb) Disallow parameter version include character '.'
    if '.' in '%s' % version:
        raise ValueError("Parameter version shouldn't include character '.'.")
    module_str = '%s.v%s' % (module, version)
    if submodule:
        module_str = '.'.join((module_str, submodule))
    return import_module(module_str)


def try_import(import_str, default=None):
    """Try to import a module and if it fails return default."""
    try:
        return import_module(import_str)
    except ImportError:
        return default


def import_any(module, *modules):
    """Try to import a module from a list of modules.
    :param modules: A list of modules to try and import
    :returns: The first module found that can be imported
    :raises ImportError: If no modules can be imported from list
    .. versionadded:: 3.8
    """
    for module_name in (module,) + modules:
        imported_module = try_import(module_name)
        if imported_module:
            return imported_module

    raise ImportError('Unable to import any modules from the list %s' %
                      str(modules))


class AppContext(object):

    @staticmethod
    def GetObject(id,**kwargs):
        try:
            config_path = os.path.join(GloalConfig().config, 'config.xml')
            context=ApplicationContext(XMLConfig(config_path))
            obj=context.get_object(id)
            logger.info(obj)

            return obj
        except:
            logger.error("",exc_info=1)
            return None



