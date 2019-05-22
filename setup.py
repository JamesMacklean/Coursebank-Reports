# -*- coding: utf-8 -*-
#
# Imports ###########################################################

import os
from setuptools import setup

# Main ##############################################################

setup(
    name='coursebank-reports',
    version='1.0',
    description='Cousrebank Reports',
    packages=['coursebank_reports'],
    install_requires=[
        'Django',
    ],
)
