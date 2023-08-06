# Copyright 2012 OpenStack Foundation
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

from tempest.api.compute import base
from tempest.common import utils
from tempest import config
from tempest.lib import decorators

CONF = config.CONF


class FloatingIPDetailsTestJSON(base.BaseV2ComputeTest):

    @classmethod
    def skip_checks(cls):
        super(FloatingIPDetailsTestJSON, cls).skip_checks()
        if not utils.get_service_list()['network']:
            raise cls.skipException("network service not enabled.")
        if not CONF.network_feature_enabled.floating_ips:
            raise cls.skipException("Floating ips are not available")

    @classmethod
    def setup_clients(cls):
        super(FloatingIPDetailsTestJSON, cls).setup_clients()
        cls.client = cls.floating_ips_client
        cls.pools_client = cls.floating_ip_pools_client

    @classmethod
    def resource_setup(cls):
        super(FloatingIPDetailsTestJSON, cls).resource_setup()
        cls.floating_ip = []
        cls.floating_ip_id = []
        for _ in range(3):
            body = cls.client.create_floating_ip(
                pool=CONF.network.floating_network_name)['floating_ip']
            cls.floating_ip.append(body)
            cls.floating_ip_id.append(body['id'])

    @classmethod
    def resource_cleanup(cls):
        for f_id in cls.floating_ip_id:
            cls.client.delete_floating_ip(f_id)
        super(FloatingIPDetailsTestJSON, cls).resource_cleanup()

    @decorators.idempotent_id('16db31c3-fb85-40c9-bbe2-8cf7b67ff99f')
    def test_list_floating_ips(self):
        # Positive test:Should return the list of floating IPs
        body = self.client.list_floating_ips()['floating_ips']
        floating_ips = body
        self.assertNotEmpty(floating_ips,
                            "Expected floating IPs. Got zero.")
        for i in range(3):
            self.assertIn(self.floating_ip[i], floating_ips)

    @decorators.idempotent_id('eef497e0-8ff7-43c8-85ef-558440574f84')
    def test_get_floating_ip_details(self):
        # Positive test:Should be able to GET the details of floatingIP
        # Creating a floating IP for which details are to be checked
        body = self.client.create_floating_ip(
            pool=CONF.network.floating_network_name)['floating_ip']
        floating_ip_id = body['id']
        self.addCleanup(self.client.delete_floating_ip,
                        floating_ip_id)
        floating_ip_instance_id = body['instance_id']
        floating_ip_ip = body['ip']
        floating_ip_fixed_ip = body['fixed_ip']
        body = self.client.show_floating_ip(floating_ip_id)['floating_ip']
        # Comparing the details of floating IP
        self.assertEqual(floating_ip_instance_id,
                         body['instance_id'])
        self.assertEqual(floating_ip_ip, body['ip'])
        self.assertEqual(floating_ip_fixed_ip,
                         body['fixed_ip'])
        self.assertEqual(floating_ip_id, body['id'])

    @decorators.idempotent_id('df389fc8-56f5-43cc-b290-20eda39854d3')
    def test_list_floating_ip_pools(self):
        # Positive test:Should return the list of floating IP Pools
        floating_ip_pools = self.pools_client.list_floating_ip_pools()
        self.assertNotEmpty(floating_ip_pools['floating_ip_pools'],
                            "Expected floating IP Pools. Got zero.")
