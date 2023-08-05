#    Copyright (c) 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import collections

SessionState = collections.namedtuple('SessionState', [
    'OPENED', 'DEPLOYING', 'DEPLOYED', 'DEPLOY_FAILURE', 'DELETING',
    'DELETE_FAILURE'
])(
    OPENED='opened',
    DEPLOYING='deploying',
    DEPLOYED='deployed',
    DEPLOY_FAILURE='deploy failure',
    DELETING='deleting',
    DELETE_FAILURE='delete failure'
)

EnvironmentStatus = collections.namedtuple('EnvironmentStatus', [
    'READY', 'PENDING', 'DEPLOYING', 'DEPLOY_FAILURE', 'DELETING',
    'DELETE_FAILURE'
])(
    READY='ready',
    PENDING='pending',
    DEPLOYING='deploying',
    DEPLOY_FAILURE='deploy failure',
    DELETING='deleting',
    DELETE_FAILURE='delete failure'

)
