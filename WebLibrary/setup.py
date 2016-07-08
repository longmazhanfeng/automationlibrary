#!/usr/bin/env python

import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'src'))
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

execfile(join(dirname(__file__), 'src', 'Selenium2Library', 'version.py'))

setup(name         = 'robotframework-weblibrary',
      version      = VERSION,
      description  = 'Web testing library for Robot Framework Extended with Selenium2Library',
      long_description = open(join(dirname(__file__), 'README.rst')).read(),
      author       = 'Dong Hao',
      author_email = '<longmazhanfeng@gmail.com>',
      url          = 'https://g.hz.netease.com/yixinplusQA/RFUI_Framework/tree/master/Third-Party-Module/WebLibrary',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation selenium selenium2 webdriver web',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Testing"
                     ],
      install_requires = [
                   'images2gif-Pillow >= 0.0.2',
				   'decorator >= 3.3.2',
				   'selenium >= 2.32.0',
				   'robotframework >= 2.9.1, <=2.9.2',
				   'docutils >= 0.8.1'
				 ],
      py_modules=['ez_setup'],
      package_dir  = {'' : 'src'},
      packages     = ['Selenium2Library','Selenium2Library.keywords','Selenium2Library.locators',
                      'Selenium2Library.utils','Selenium2Library.utils.events'],
      include_package_data = True,
      )
