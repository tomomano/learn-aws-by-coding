import boto3
import argparse
from uuid import uuid4

ddb = boto3.resource('dynamodb')

def write_item(table_name):
    table = ddb.Table(table_name)
    table.put_item(
    Item={
        'item_id': str(uuid4()),
        'first_name': 'John',
        'last_name': 'Doe',
        'age': 25,
        }
    )

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("table_name", type=str)
    args = parser.parse_args()

    write_item(args.table_name)
