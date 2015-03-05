#!/usr/bin/env python
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""entity, a simple object-document mapper which wraps the mongodb driver - motor for python tornado applications."""
try:
    import tornado
except:
    raise ImportError(
        "Tornado is not installed. Install tornado using pip install "
        "or version >= 4.0.2 https://github.com/tornadoweb/tornado")

try:
    import motor
except:
    raise ImportError("Tornado is not installed. Install motor using pip install "
                      "preferably https://github.com/mongodb/motor/")

version = "0.1.4"
version_info = (0, 1, 4)

from pyenty.entitymanager import EntityManager, EntityConnection
from pyenty import types



