# Copyright 2016 marcoimmel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
#
# this aws lambda functions locates ec2 instances and stops them
# the function can be invoked by a cloudwatch scheduled event
#

import logging
import boto3

logger = logging.getLogger('auto-admin-logger')
logger.setLevel(logging.INFO)

def event_handler(event, context):
    ec2 = boto3.resource('ec2')
    logger.info('{} ec2 instances requested'.format(event['action']))
    
    start = True if event['action'] == 'start' else False
    
    filters = [
        {
            'Name':  'tag:AutoOn' if start else 'tag:AutoOff',
            'Values': ['true']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['stopped' if start else 'running']
        }
    ]

    instances = ec2.instances.filter(Filters=filters)
    instance_ids = [instance.id for instance in instances]
    
    if len(instance_ids) > 0:
        instances.start() if start else instances.stop()
        logger.info('Processing instances: {}'.format(instance_ids))
    else:
        logger.info('Nothing to process')
