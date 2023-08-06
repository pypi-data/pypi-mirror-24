""" Logs calls to the AMaaS APIs """

from datetime import datetime

import boto3

class APICallLogger(object):
    """ The current implementation of the API Call Logger uses Cloudwatch metrics """

    def __init__(self):
        self.client = boto3.client('cloudwatch')

    def record_api_call(self, asset_manager_id, api_call_type, api_call_subtype, client_id=None, token_asset_manager_id=None, username=None, environment='dev'):
        """ Record the API call """
        asset_manager_id = str(asset_manager_id)  # In case it gets sent in as an integer
        token_asset_manager_id = str(token_asset_manager_id) if token_asset_manager_id is not None else ""
        username = str(username) if username is not None else ""
        client_id = str(client_id) if client_id is not None else ""
        self.client.put_metric_data(
            Namespace='amaas',
            MetricData=[
                {
                    'MetricName': 'AMaaSAPICalls',
                    'Dimensions': [
                        {'Name': 'api_call_type', 'Value': api_call_type},
                        {'Name': 'api_call_subtype', 'Value': api_call_subtype},
                        {'Name': 'asset_manager_id', 'Value': asset_manager_id},
                        {'Name': 'environment', 'Value': environment},
                        {'Name': 'client_id', 'Value': client_id},
                        {'Name': 'token_asset_manager_id', 'Value': token_asset_manager_id},
                        {'Name': 'username', 'Value': username}
                    ],
                    'Timestamp': datetime.utcnow(),
                    'Value': 1,
                    'Unit': 'Count'
                },
            ]
        )
