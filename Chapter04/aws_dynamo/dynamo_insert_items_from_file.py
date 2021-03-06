"""
Copyright (c) 2017-2019 Starwolf Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

Created on 20 Jan 2018

@author: Richard Freeman

This packages inserts records from a file into specified DynamoDB table

"""
import csv

from boto3 import resource
import json


class DynamoRepository:
    def __init__(self, target_dynamo_table, region='us-west-1'):
        self.dynamodb = resource(service_name='dynamodb', region_name=region)
        self.target_dynamo_table = target_dynamo_table
        try:
            response = self.dynamodb.create_table(
                AttributeDefinitions = [
                    {
                        'AttributeName': 'EventId',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'EventDay',
                        'AttributeType': 'N'
                    },
                ],
                KeySchema=[
                    {
                        'AttributeName': 'EventId',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'EventDay',
                        'KeyType': 'RANGE'
                    }
                ],
                ProvisionedThroughput = {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                },
                TableName=target_dynamo_table
            )
        except Exception as ex:
            print(f'{ex}')
        finally:
            self.table = self.dynamodb.Table(self.target_dynamo_table)


    def update_dynamo_event_counter(self, event_name, event_datetime, event_count=1):
        try:
            response = self.table.update_item(
                Key={
                    'EventId': str(event_name),
                    'EventDay': int(event_datetime)
                },
                ExpressionAttributeValues={":eventCount": int(event_count)},
                UpdateExpression="ADD EventCount :eventCount")
        except Exception as ex:
            print(f'Exception occurred of type {ex} occured when writing data record {event_name}, '
                  f'{event_datetime}, {event_count}')
            return None
        else:
            return response


def main():
    # For manual deployment
    # table_name = 'user-visits'

    # For SAM:
    table_name = 'user-visits-sam'
    input_data_path = '../sample_data/dynamodb-sample-data.txt'
    dynamo_repo = DynamoRepository(table_name)
    with open(input_data_path, 'r') as sample_file:
        csv_reader = csv.DictReader(sample_file)
        for row in csv_reader:
            response = dynamo_repo.update_dynamo_event_counter(row['EventId'],
                                                               row['EventDay'],
                                                               row['EventCount'])
            # tip from: https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries
            print(json.dumps(response, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
