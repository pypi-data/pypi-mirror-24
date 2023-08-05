# @(#) $Id$
"""
Installation script for the GSI module
"""
#import ez_setup
#ez_setup.use_setuptools()

import os
import ConfigParser

from setuptools import setup, find_packages, Extension

here = os.path.realpath(os.path.dirname(__file__))
srcDir = os.path.join(here, "src")

config = ConfigParser.SafeConfigParser()
config.read(os.path.join(here, "setup.cfg"))

def findFiles(baseDir, validFileExts):
    files = []
    for t in os.walk(baseDir):
        for fileInDir in t[2]:
            for fext in validFileExts:
                fPos = len(fileInDir) - len(fext)
                if fileInDir.find(fext, fPos) == fPos:
                    files.append(os.path.join(baseDir, fileInDir))
    return files

def createExtension(extName):
    extDir = os.path.join(srcDir, extName.lower())
    cFiles = [os.path.join(srcDir, "util.c")] + findFiles(extDir, ".c")
    hFiles = [os.path.join(srcDir, "util.h")] + findFiles(extDir, ".h")
    extraArgs = {}
    if 'Extensions' in config.sections():
        for k in config.options('Extensions'):
            extraArgs[k] = [v.strip() for v in config.get('Extensions', k).split(" ") if v.strip()]
            for i in range(len(extraArgs[k])):
                if os.path.isfile(extraArgs[k][i]):
                    extraArgs[k][i] = os.path.realpath(extraArgs[k][i])
    return Extension("GSI.%s" % extName,
                     cFiles,
                     depends=hFiles,
                     libraries=['ssl', 'crypto'],
                     extra_compile_args=["-Wno-deprecated-declarations", "-std=c99"],
                     ** extraArgs
                    )

# Get the long description from the README file
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name="GSI",
    version='0.6.5',
    description="Python wrapper module around the OpenSSL library",
    long_description=long_description,
    url='https://github.com/DIRACGrid/pyGSI',
    author="Adrian Casajus",
    author_email="adria@ecm.ub.es",
    license="GPLv3",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        #'Topic :: GSI to python :: Grid proxy certificates', #only for non-sdst packages

        # Pick your license as you wish (should match "license" above)
        #'License :: OSI Approved :: GPLv3 License',#only for non-sdst packages

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    zip_safe=False,
    #install_requires = ["distribute>0.6", "pip"],
    python_requires='>=2.7',
    py_modules=['GSI.__init__', 'GSI.tsafe', 'GSI.version'],
    ext_modules=[createExtension(extName) for extName in ("crypto", "rand", "SSL")]
)
