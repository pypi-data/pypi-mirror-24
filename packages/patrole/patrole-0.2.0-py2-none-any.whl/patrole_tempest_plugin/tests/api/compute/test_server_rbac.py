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

from oslo_log import log

from tempest.common import waiters
from tempest import config
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators
from tempest.lib import exceptions
from tempest import test

from patrole_tempest_plugin import rbac_exceptions
from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.compute import rbac_base as base

CONF = config.CONF
LOG = log.getLogger(__name__)


class ComputeServersRbacTest(base.BaseV2ComputeRbacTest):

    credentials = ['primary', 'admin']

    @classmethod
    def setup_clients(cls):
        super(ComputeServersRbacTest, cls).setup_clients()
        cls.networks_client = cls.os_primary.networks_client
        cls.ports_client = cls.os_primary.ports_client
        cls.subnets_client = cls.os_primary.subnets_client
        cls.admin_servers_client = cls.os_admin.servers_client

    @classmethod
    def resource_setup(cls):
        super(ComputeServersRbacTest, cls).resource_setup()
        cls.server = cls.create_test_server(wait_until='ACTIVE')

    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:servers:create")
    @decorators.idempotent_id('4f34c73a-6ddc-4677-976f-71320fa855bd')
    def test_create_server(self):
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.create_test_server(wait_until='ACTIVE')

    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:servers:create:forced_host")
    @decorators.idempotent_id('0ae3c401-52ab-41bc-ab96-c598a65d9ae5')
    def test_create_server_forced_host(self):
        # Retrieve 'nova' zone host information from availiability_zone_list
        zones = self.availability_zone_client.list_availability_zones(
            detail=True)['availabilityZoneInfo']
        hosts = [zone['hosts'] for zone in zones if zone['zoneName'] == 'nova']

        # We just need any host out of the hosts list to build the
        # availability_zone attribute. So, picking the first one is fine.
        # The first key of the dictionary specifies the host name.
        host = list(hosts[0].keys())[0]
        availability_zone = 'nova:' + host

        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.create_test_server(wait_until='ACTIVE',
                                availability_zone=availability_zone)

    @test.services('volume')
    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:servers:create:attach_volume")
    @decorators.idempotent_id('eeddac5e-15aa-454f-838d-db608aae4dd8')
    def test_create_server_attach_volume(self):
        # To create a bootable volume, the UUID of the image from which
        # to create the volume must be included as the imageRef attribute in
        # the request body.
        volume_id = self.create_volume(
            imageRef=CONF.compute.image_ref,
            size=CONF.volume.volume_size)['id']

        server_name = data_utils.rand_name(self.__class__.__name__ + "-server")
        bd_map_v2 = [{'uuid': volume_id,
                      'source_type': 'volume',
                      'destination_type': 'volume',
                      'boot_index': 0,
                      'delete_on_termination': True}]
        device_mapping = {'block_device_mapping_v2': bd_map_v2}

        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        # Use image_id='' to avoid using the default image in tempest.conf.
        self.create_test_server(name=server_name, image_id='',
                                **device_mapping)

    @test.services('network')
    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:servers:create:attach_network")
    @decorators.idempotent_id('b44cd4ff-50a4-42ce-ada3-724e213cd540')
    def test_create_server_attach_network(self):
        def _create_network_resources():
            # Create network
            network_name = data_utils.rand_name(
                self.__class__.__name__ + '-network')

            network = self.networks_client.create_network(
                name=network_name, port_security_enabled=True)['network']
            self.addCleanup(self.networks_client.delete_network, network['id'])

            # Create subnet for the network
            subnet_name = data_utils.rand_name(
                self.__class__.__name__ + '-subnet')
            subnet = self.subnets_client.create_subnet(
                name=subnet_name,
                network_id=network['id'],
                cidr=CONF.network.project_network_cidr,
                ip_version=4)['subnet']
            self.addCleanup(self.subnets_client.delete_subnet, subnet['id'])

            return network

        network = _create_network_resources()
        network_id = {'uuid': network['id']}

        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        server = self.create_test_server(wait_until='ACTIVE',
                                         networks=[network_id])
        self.addCleanup(waiters.wait_for_server_termination,
                        self.servers_client, server['id'])
        self.addCleanup(self.servers_client.delete_server, server['id'])

    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:servers:delete")
    @decorators.idempotent_id('062e3440-e873-4b41-9317-bf6d8be50c12')
    def test_delete_server(self):
        server = self.create_test_server(wait_until='ACTIVE')

        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        self.servers_client.delete_server(server['id'])
        waiters.wait_for_server_termination(
            self.admin_servers_client, server['id'])

    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:servers:update")
    @decorators.idempotent_id('077b17cb-5621-43b9-8adf-5725f0d7a863')
    def test_update_server(self):
        new_name = data_utils.rand_name(self.__class__.__name__ + '-server')
        self.rbac_utils.switch_role(self, toggle_rbac_role=True)
        try:
            self.servers_client.update_server(self.server['id'], name=new_name)
            waiters.wait_for_server_status(self.admin_servers_client,
                                           self.server['id'], 'ACTIVE')
        except exceptions.ServerFault as e:
            # Some other policy may have blocked it.
            LOG.info("ServerFault exception caught. Some other policy "
                     "blocked updating of server")
            raise rbac_exceptions.RbacConflictingPolicies(e)
