#!/usr/bin/env python
# http://docs.python.org/distutils/setupscript.html
# http://docs.python.org/2/distutils/examples.html

from setuptools import setup, find_packages
import re
import os


name = "" # TODO give me a name
###############################################################################
# REMOVE WHEN FLESHED OUT
#name = os.path.splitext(os.path.basename(os.path.dirname(__file__)))[0].lstrip("_").lower()
name = os.path.splitext(os.path.basename(os.getcwd()))[0].lstrip("_").lower()
#import subprocess
filepath = "{}.py".format(name)
if not os.path.isfile(filepath):
    with open(filepath, 'w') as f:
        f.write("\n__version__ = '0.0.1'\n")

#subprocess.check_call("touch {}.py".format(name), shell=True)
###############################################################################
with open("{}.py".format(name), 'rU') as f:
    version = re.search("^__version__\s*=\s*[\'\"]([^\'\"]+)", f.read(), flags=re.I | re.M).group(1)


setup(
    name=name,
    version=version,
    description='PLACEHOLDER',
    author='Jay Marcyes',
    author_email='jay@marcyes.com',
    url='http://github.com/Jaymon/{}'.format(name),
    py_modules=[name], # files
    # packages=find_packages(), # folders
    license="MIT",
#     install_requires=[''],
    classifiers=[ # https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
#     entry_points = {
#         'console_scripts': [
#             '{} = {}:console'.format(name, name),
#         ],
#     }
)
