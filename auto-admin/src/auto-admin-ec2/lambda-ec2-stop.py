# this aws lambda functions locates running ec2 instances and stops them
# the function can be invoked by a cloudwatch scheduled event
import logging
import boto3

logger = logging.getLogger('auto-admin-logger')
logger.setLevel(logging.INFO)

def event_handler(event, context):
    ec2 = boto3.resource('ec2')

    filters = [
        {
            'Name': 'tag:AutoOff',
            'Values': ['true']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    instances = ec2.instances.filter(Filters=filters)

    if len(instances) > 0:
        instances.stop()
        logger.info('Instances shutting down: {}'.format([instance.id for instance in instances]))
    else:
        logger.info('Nothing to shut down')
