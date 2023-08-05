#    Copyright (c) 2016 Mirantis, Inc.
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

import os

from tempest import config
from tempest.lib import decorators
from tempest.lib import exceptions

from murano_tempest_tests.tests.api.application_catalog import base
from murano_tempest_tests import utils

CONF = config.CONF


class TestStaticActionsNegative(base.BaseApplicationCatalogTest):

    @classmethod
    def resource_setup(cls):
        super(TestStaticActionsNegative, cls).resource_setup()

        application_name = utils.generate_name('test_repository_class')
        cls.abs_archive_path, dir_with_archive, archive_name = \
            utils.prepare_package(application_name, add_class_name=True)

        if CONF.application_catalog.glare_backend:
            client = cls.artifacts_client
        else:
            client = cls.application_catalog_client

        cls.package = client.upload_package(
            application_name, archive_name, dir_with_archive,
            {"categories": [], "tags": [], 'is_public': False})

    @classmethod
    def resource_cleanup(cls):
        os.remove(cls.abs_archive_path)
        if CONF.application_catalog.glare_backend:
            client = cls.artifacts_client
        else:
            client = cls.application_catalog_client
        client.delete_package(cls.package['id'])
        super(TestStaticActionsNegative, cls).resource_cleanup()

    @decorators.attr(type='negative')
    @decorators.idempotent_id('c6d05273-b6fe-4a33-8a87-c7110c171bc2')
    def test_call_static_action_no_args(self):
        self.assertRaises(exceptions.BadRequest,
                          self.application_catalog_client.call_static_action)

    @decorators.attr(type='negative')
    @decorators.idempotent_id('35440618-6649-40cb-b878-b5cddd4ea0dd')
    def test_call_static_action_wrong_class(self):
        self.assertRaises(exceptions.NotFound,
                          self.application_catalog_client.call_static_action,
                          'wrong.class', 'staticAction',
                          args={'myName': 'John'})

    @decorators.attr(type='negative')
    @decorators.idempotent_id('75c6cc5e-0804-45d9-beb2-10c7ab409b70')
    def test_call_static_action_wrong_method(self):
        self.assertRaises(exceptions.NotFound,
                          self.application_catalog_client.call_static_action,
                          class_name=self.package['class_definitions'][0],
                          method_name='wrongMethod',
                          args={'myName': 'John'})

    @decorators.attr(type='negative')
    @decorators.idempotent_id('334c828b-3f49-49e0-97a2-534f57596bfb')
    def test_call_static_action_session_method(self):
        self.assertRaises(exceptions.NotFound,
                          self.application_catalog_client.call_static_action,
                          class_name=self.package['class_definitions'][0],
                          method_name='staticNotAction',
                          args={'myName': 'John'})

    @decorators.attr(type='negative')
    @decorators.idempotent_id('3ebb5009-2f61-4200-a34c-2bc506d94aed')
    def test_call_static_action_wrong_args(self):
        self.assertRaises(exceptions.BadRequest,
                          self.application_catalog_client.call_static_action,
                          class_name=self.package['class_definitions'][0],
                          method_name='staticAction',
                          args={'myEmail': 'John'})

    @decorators.attr(type='negative')
    @decorators.idempotent_id('5f4f6edc-2d66-4426-bb81-48e7570d93ef')
    def test_call_static_action_wrong_package(self):
        self.assertRaises(exceptions.NotFound,
                          self.application_catalog_client.call_static_action,
                          class_name=self.package['class_definitions'][0],
                          method_name='staticAction',
                          package_name='wrong.package',
                          args={'myName': 'John'})

    @decorators.attr(type='negative')
    @decorators.idempotent_id('c0854170-700f-4924-9cfe-3bff876b9e63')
    def test_call_static_action_wrong_version_format(self):
        self.assertRaises(exceptions.BadRequest,
                          self.application_catalog_client.call_static_action,
                          class_name=self.package['class_definitions'][0],
                          method_name='staticAction',
                          class_version='aaa',
                          args={'myName': 'John'})
