#!/usr/bin/env jython

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import sys
try:
    from setuptools import setup, Extension
except:
    from distutils.core import setup, Extension

setup(
    name='jyboss',
    version='0.2.2',
    url='https://github.com/fareliner/jyboss-cli',
    author='Niels Bertram',
    author_email='nielsbne@gmail.com',
    description='A Jython CLI for JBoss Application Server',
    license='Apache License 2.0',
    requires=['simplejson', 'PyYAML'],
    py_modules=['jyboss.context', 'jyboss.cli', 'jyboss.exceptions', 'jyboss.logging', 'jyboss.command.core',
                'jyboss.command.undertow', 'jyboss.command.extension', 'jyboss.command.security',
                'jyboss.command.keycloak', 'jyboss.command.ee', 'jyboss.command.datasources', 'jyboss.command.module',
                'jyboss.command.deployment', 'jyboss.command.jgroups', 'jyboss.command.infinispan',
                'jyboss.command.interface', 'jyboss.command.binding', 'jyboss.ansible']
)
