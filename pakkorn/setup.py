"""
NAME:
    setup.py

SYNOPSIS:
    python setup.py [options] [command]

DESCRIPTION:
    Using distutils "setup", build, install, or make tarball of the package.

OPTIONS:
    See Distutils documentation for details on options and commands.
    Common commands:
    build               build the package, in preparation for install
    install             install module(s)/package(s) [runs build if needed]
    install_data        install datafiles (e.g., in a share dir)
    install_scripts     install executable scripts (e.g., in a bin dir)
    sdist               make a source distribution
    bdist               make a binary distribution
    clean               remove build temporaries

EXAMPLES:
    cd mydir
    (cp myfile-0.1.tar.gz here)
    gzip -cd myfile-0.1.tar.gz | tar xvf -
    cd myfile-0.1
    python setup.py build
    python setup.py install
    python setup.py sdist
"""

#===imports=============
import os
import sys
#import re
import string
import getopt
#import shutil
#import commands
#===setuptools======
import ez_setup # From http://peak.telecommunity.com/DevCenter/setuptools
ez_setup.use_setuptools()

from setuptools import setup, find_packages, Extension

#===patch2.2.3======
# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

#===globals======
modname='setup'
debug_p=0

#===configuration======
pkgname='pakkorn'
version=string.strip(open("VERSION").readline())
exec_prefix=sys.exec_prefix
description = "Package manager for windows. Download/Install from internet."
long_description = """pakkorn is package manager that download/install/upgrade various 
packages from internet. pakkorn aims to provide on windows what linux
distributions provide threw their builtins package manager (apt/pdkg, rpm, etc.).
While sharing some concepts with linux package managers, pakkorn doesn't follow
the exact same principles, and so doesn't share code."""
author = "Arthibus Gissehel"
author_email = "public-pakkorn-setup@giss.ath.cx"
url="http://test.giss.mine.nu/pakkorn/"
classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Environment :: Win32 (MS Windows)',
    'Environment :: X11 Applications :: Qt',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: System :: Software Distribution',
    'Topic :: System :: Systems Administration',
    ]
#download_url='http://developer.berlios.de/project/showfiles.php?group_id=3108'

scripts=[
    'src/kk.py',
    'src/kkqt.py',
    ]
py_modules=[]
packages=[
    'pakkorn',
    'pakkorn.engine',
    'pakkorn.data',
    'pakkorn.database',
    'pakkorn.dataxml',
    'pakkorn.gui',
    'pakkorn.gui.qt',
    'pakkorn.config',
    ]
package_dir = {'': 'src'}
package_data = {
    '': 'src',
    }
ext_modules=[]
#   [Extension('my_ext', ['my_ext.c', 'file1.c', 'file2.c'],
#           include_dirs=[''],
#           library_dirs=[''],
#           libraries=[''],)
#    ]
zip_safe = False
options={}
extra_parameters = {}
#===py2exe==========================
try :
    import py2exe
    extra_parameters['console'] = [
        {
            'icon_resources':[(0,'ressources/pakkorn.ico')],
            'script':'src/kk.py',
            },
        {
            'icon_resources':[(0,'ressources/pakkorn.ico')],
            'script':'src/kkqt.py',
            },
        ]
    options["py2exe"] = {
        "includes" : [
            'encodings',
            'encodings.latin_1',
            'web',
            'sip', 
            'PyQt4._qt',
            ],
        "excludes": [],
        }
except ImportError :
    pass
#===utilities==========================
def debug(ftn,txt):
    if debug_p:
        sys.stdout.write("%s.%s:%s\n" % (modname,ftn,txt))
        sys.stdout.flush()

def fatal(ftn,txt):
    msg="%s.%s:FATAL:%s\n" % (modname,ftn,txt)
    raise SystemExit, msg

def usage():
    print __doc__

#=============================
def main():
    setup (#---meta-data---
           name = pkgname,
           version = version,
           description = description,
           long_description = long_description,
           author = author,
           author_email = author_email,
           url=url,
           classifiers = classifiers,
           #download_url=download_url,

           #---scripts,modules and packages---
           scripts=scripts,
           py_modules = py_modules,
           package_dir = package_dir,
           packages = packages,
           ext_modules = ext_modules,

           #---egg params---
           zip_safe = zip_safe,

           #---other---
           options = options,
           **extra_parameters
           )
#==============================
if __name__ == '__main__':
    opts,pargs=getopt.getopt(sys.argv[1:],'hv',
                 ['help','version','exec-prefix'])
    for opt in opts:
        if opt[0]=='-h' or opt[0]=='--help':
            usage()
            sys.exit(0)
        elif opt[0]=='-v' or opt[0]=='--version':
            print modname+": version="+version
        elif opt[0]=='--exec-prefix':
            exec_prefix=opt[1]

    for arg in pargs:
        if arg=='test':
            do_test()
            sys.exit(0)
        elif arg=='doc':
            do_doc()
            sys.exit(0)
        else:
            pass

    main()
