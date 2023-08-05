# Copyright 2017 AT&T Corporation.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import itertools

from murano.common.policies import action
from murano.common.policies import base
from murano.common.policies import category
from murano.common.policies import deployment
from murano.common.policies import env_template
from murano.common.policies import environment
from murano.common.policies import package


def list_rules():
    return itertools.chain(
        base.list_rules(),
        action.list_rules(),
        category.list_rules(),
        deployment.list_rules(),
        environment.list_rules(),
        env_template.list_rules(),
        package.list_rules()
    )
