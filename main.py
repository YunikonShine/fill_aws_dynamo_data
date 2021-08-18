import json
from decimal import Decimal
import simplejson
import boto3 as boto3

dynamo = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url='http://localhost:4566',
                        aws_access_key_id="XXX", aws_secret_access_key="XXX")


def save_file(table: object, file_name: str):
    result = []
    temp_file = open(file_name + '.json', 'w')
    for i in table.scan()['Items']:
        result.append(i)
    temp_file.write(str(simplejson.loads(simplejson.dumps(result)))
                    .replace("\'", "\"")
                    .replace("False", "false")
                    .replace("True", "true"))


def save_data(table: object, file_name: str):
    temp_file = open(file_name + '.json', 'r', encoding="utf8")
    for k in json.loads(temp_file.read(), parse_float=Decimal):
        table.put_item(Item=k)


if __name__ == '__main__':
    for i in dynamo.tables.all():
        # save_file(i, i.table_name)
        save_data(i, i.table_name)
