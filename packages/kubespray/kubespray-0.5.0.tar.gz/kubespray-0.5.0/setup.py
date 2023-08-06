#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

requirements = [
    'cffi>=1.6.0',
    'setuptools>=11.3',
    'cryptography>=1.3.2',
    'requests>=2.4.3',
    'netaddr>=0.7.18',
    'markupsafe>=0.23',
    'pyasn1>=0.1.8',
    'boto>=2.40.0',
    'apache-libcloud>=0.20.1'
]

test_requirements = [
    # TODO: put package test requirements here
]

my_homedir = os.path.expanduser("~")

setup(
    name='kubespray',
    version='0.5.0',
    description="Kubespray kubernetes cluster deployment",
    author="Smaine Kahlouch",
    author_email='smainklh@gmail.com',
    url='https://github.com/kubespray/kubespray-cli',
    data_files=[
        (my_homedir, ['src/kubespray/files/.kubespray.yml'])
    ],
    packages=find_packages('src'),
    scripts=[
        'bin/kubespray'
    ],
    package_dir={'': 'src'},
    package_data={'kubespray': ['files/*.yml'], },
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords='kubespray',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
