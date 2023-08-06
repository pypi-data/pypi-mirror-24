# Copyright 2017 AT&T Corporation.
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


class SnapshotsActionsRbacTest(rbac_base.BaseVolumeRbacTest):

    @classmethod
    def skip_checks(cls):
        super(SnapshotsActionsRbacTest, cls).skip_checks()
        if not CONF.volume_feature_enabled.snapshot:
            raise cls.skipException("Cinder snapshot feature disabled")

    @classmethod
    def resource_setup(cls):
        super(SnapshotsActionsRbacTest, cls).resource_setup()
        cls.volume = cls.create_volume()
        cls.snapshot = cls.create_snapshot(volume_id=cls.volume['id'])
        cls.snapshot_id = cls.snapshot['id']

    @rbac_rule_validation.action(
        service="cinder",
        rule="volume_extension:snapshot_admin_actions:reset_status")
    @decorators.idempotent_id('ea430145-34ef-408d-b678-95d5ae5f46eb')
    def test_reset_snapshot_status(self):
        status = 'error'
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.snapshots_client.reset_snapshot_status(self.snapshot['id'],
                                                    status)

    @rbac_rule_validation.action(
        service="cinder",
        rule="volume_extension:snapshot_admin_actions:force_delete")
    @decorators.idempotent_id('a8b0f7d8-4c00-4645-b8d5-33ab4eecc6cb')
    def test_snapshot_force_delete(self):
        temp_snapshot = self.create_snapshot(self.volume['id'])

        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.snapshots_client.force_delete_snapshot(temp_snapshot['id'])
        self.snapshots_client.wait_for_resource_deletion(temp_snapshot['id'])


class SnapshotsActionsV3RbacTest(SnapshotsActionsRbacTest):
    _api_version = 3
