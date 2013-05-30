from distutils.core import setup, Extension
import distutils.sysconfig
import shutil
import os.path
import re
import sys

CLASSIFIERS = filter(None, map(str.strip,
"""
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: C
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
""".splitlines()))

try:
    shutil.rmtree("./build")
except(OSError):
    pass

def _is_debug_build():
    import imp
    for ext, _, _ in imp.get_suffixes():
        if ext == "_d.pyd":
            return True
    return False

if _is_debug_build():
    macros = [("PYTHONDLL", '\\"PYTHON%d%d_d.DLL\\"' % sys.version_info[:2]),
              ("PYTHONCOM", '\\"pythoncom%d%d_d.dll\\"' % sys.version_info[:2])]
else:
    macros = [("PYTHONDLL", '\\"PYTHON%d%d.DLL\\"' % sys.version_info[:2]),
              ("PYTHONCOM", '\\"pythoncom%d%d.dll\\"' % sys.version_info[:2])]

module1 = Extension("_ssl",
                         ["./python/_ssl.c"],
                         libraries=['ws2_32', 'libeay32', 'ssleay32'],
                         depends=['socketmodule.h'],
                         define_macros=macros,
                         )

README = ''
with open('README.rst', 'rb') as fp:
    README = fp.read()

setup (name = 'ssl',
       version = '1.0',
       description = "backport ssl SNI feature to python2",
       long_description = README,
       ext_modules = [module1],
       py_modules = ['ssl'],
       author="phuslu",
       author_email="phus.lu@gmail.com",
       download_url="https://github.com/phus/backport_ssl",
       license="MIT/X11, MPL 1.1",
       platforms='Windows',
       url="https://github.com/phus/backport_ssl",
       classifiers=CLASSIFIERS,
       )
