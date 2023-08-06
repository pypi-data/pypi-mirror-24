# Copyright 2016 AT&T Corp
# All Rights Reserved.
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

from tempest import config
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.volume import rbac_base

CONF = config.CONF


class SnapshotMetadataRbacTest(rbac_base.BaseVolumeRbacTest):

    @classmethod
    def skip_checks(cls):
        super(SnapshotMetadataRbacTest, cls).skip_checks()
        if not CONF.volume_feature_enabled.snapshot:
            raise cls.skipException("Cinder snapshot feature disabled")

    @classmethod
    def resource_setup(cls):
        super(SnapshotMetadataRbacTest, cls).resource_setup()
        cls.volume = cls.create_volume()
        # Create a snapshot
        cls.snapshot = cls.create_snapshot(volume_id=cls.volume['id'])
        cls.snapshot_id = cls.snapshot['id']

    @classmethod
    def _create_test_snapshot_metadata(self):
        # Create test snapshot metadata
        metadata = {"key1": "value1",
                    "key2": "value2",
                    "key3": "value3"}
        self.snapshots_client.create_snapshot_metadata(
            self.snapshot_id, metadata)['metadata']

    @rbac_rule_validation.action(
        service="cinder",
        rule="volume_extension:extended_snapshot_attributes")
    @decorators.idempotent_id('c9cbec1c-edfe-46b8-825b-7b6ac0a58c25')
    def test_create_snapshot_metadata(self):
        # Create metadata for the snapshot
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self._create_test_snapshot_metadata()

    @rbac_rule_validation.action(service="cinder",
                                 rule="volume:get_snapshot_metadata")
    @decorators.idempotent_id('f6912bb1-62e6-483d-bcd0-e98c1641f4c3')
    def test_get_snapshot_metadata(self):
        # Create volume and snapshot metadata
        self._create_test_snapshot_metadata()
        # Get metadata for the snapshot
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.snapshots_client.show_snapshot_metadata(
            self.snapshot_id)

    @rbac_rule_validation.action(
        service="cinder",
        rule="volume_extension:volume_tenant_attribute")
    @decorators.idempotent_id('e2c73b00-0c19-4bb7-8c61-d84b1a223ed1')
    def test_get_snapshot_metadata_for_volume_tenant(self):
        # Create volume and snapshot metadata
        self._create_test_snapshot_metadata()
        # Get metadata for the snapshot
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        # Get the metadata of the snapshot
        self.snapshots_client.show_snapshot_metadata(
            self.snapshot_id)['metadata']


class SnapshotMetadataV3RbacTest(SnapshotMetadataRbacTest):
    _api_version = 3
