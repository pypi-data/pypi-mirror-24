# Copyright 2014 Mirantis, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
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
#

import mock

from mistralclient.api.v2 import cron_triggers
from mistralclient.commands.v2 import cron_triggers as cron_triggers_cmd
from mistralclient.tests.unit import base


TRIGGER_DICT = {
    'name': 'my_trigger',
    'workflow_name': 'flow1',
    'workflow_input': {},
    'workflow_params': {},
    'pattern': '* * * * *',
    'next_execution_time': '4242-12-20 13:37',
    'remaining_executions': 5,
    'created_at': '1',
    'updated_at': '1'
}

TRIGGER = cron_triggers.CronTrigger(mock, TRIGGER_DICT)


class TestCLITriggersV2(base.BaseCommandTest):
    @mock.patch('argparse.open', create=True)
    def test_create(self, mock_open):
        self.client.cron_triggers.create.return_value = TRIGGER
        mock_open.return_value = mock.MagicMock(spec=open)

        result = self.call(
            cron_triggers_cmd.Create,
            app_args=['my_trigger', 'flow1', '--pattern', '* * * * *',
                      '--params', '{}', '--count', '5', '--first-time',
                      '4242-12-20 13:37']
        )

        self.assertEqual(
            (
                'my_trigger', 'flow1', {}, '* * * * *',
                '4242-12-20 13:37', 5, '1', '1'
            ),
            result[1]
        )

    def test_list(self):
        self.client.cron_triggers.list.return_value = [TRIGGER]

        result = self.call(cron_triggers_cmd.List)

        self.assertEqual(
            [(
                'my_trigger', 'flow1', {}, '* * * * *',
                '4242-12-20 13:37', 5, '1', '1'
            )],
            result[1]
        )

    def test_get(self):
        self.client.cron_triggers.get.return_value = TRIGGER

        result = self.call(cron_triggers_cmd.Get, app_args=['name'])

        self.assertEqual(
            (
                'my_trigger', 'flow1', {}, '* * * * *',
                '4242-12-20 13:37', 5, '1', '1'
            ),
            result[1]
        )

    def test_delete(self):
        self.call(cron_triggers_cmd.Delete, app_args=['name'])

        self.client.cron_triggers.delete.assert_called_once_with('name')

    def test_delete_with_multi_names(self):
        self.call(cron_triggers_cmd.Delete, app_args=['name1', 'name2'])

        self.assertEqual(2, self.client.cron_triggers.delete.call_count)
        self.assertEqual(
            [mock.call('name1'), mock.call('name2')],
            self.client.cron_triggers.delete.call_args_list
        )
