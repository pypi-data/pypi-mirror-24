# Copyright 2015
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


import os

# noinspection PyPackageRequirements
from tempest.test_discover import plugins

from vitrage_tempest_tests import config as config_rca_service


class VitrageTempestPlugin(plugins.TempestPlugin):
    def load_tests(self):
        base_path = os.path.split(os.path.dirname(
            os.path.abspath(__file__)))[0]
        test_dir = "vitrage_tempest_tests/tests"
        full_test_dir = os.path.join(base_path, test_dir)
        return full_test_dir, base_path

    def register_opts(self, conf):
        conf.register_opt(config_rca_service.service_option,
                          group='service_available')
        conf.register_group(config_rca_service.rca_service_group)
        conf.register_opts(config_rca_service.RcaServiceGroup,
                           group='root_cause_analysis_service')

    def get_opt_lists(self):
        return [(config_rca_service.rca_service_group.name,
                 config_rca_service.RcaServiceGroup),
                ('service_available', [config_rca_service.service_option])]
