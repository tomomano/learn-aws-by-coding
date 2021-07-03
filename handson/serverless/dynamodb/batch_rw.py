import boto3
from boto3.dynamodb.conditions import Key, Attr
import argparse, random
from uuid import uuid4

import boto3
ddb = boto3.resource('dynamodb')

def batch_write(table_name, num):
    table = ddb.Table(table_name)
    with table.batch_writer() as batch:
        for i in range(num):
            batch.put_item(
                Item={
                    'item_id': str(uuid4()),
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'age': random.randint(1,50),
                }
            )
    print(f"Finished writing {num} items to the table")

def clear_database(table_name):
    table = ddb.Table(table_name)
    scan = None

    with table.batch_writer() as batch:
        count = 0
        while scan is None or 'LastEvaluatedKey' in scan:
            if scan is not None and 'LastEvaluatedKey' in scan:
                scan = table.scan(
                    ExclusiveStartKey=scan['LastEvaluatedKey'],
                )
            else:
                scan = table.scan()

            for item in scan['Items']:
                if count % 5000 == 0:
                    print(count)
                batch.delete_item(Key={'item_id': item['item_id']})
                count = count + 1
    print("Deleted all elements in the database.")

def search_under_age(table_name, age):
    table = ddb.Table(table_name)
    response = table.scan(
        FilterExpression=Attr('age').lt(age)
    )
    print(response.get("Items"))

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("table_name", type=str)
    subparsers = parser.add_subparsers(dest="command")

    sp1 = subparsers.add_parser("write")
    sp1.add_argument("num", type=int)

    sp2 = subparsers.add_parser("clear")

    sp3 = subparsers.add_parser("search_under_age")
    sp3.add_argument("age", type=int)

    args = parser.parse_args()

    if args.command == "write":
        batch_write(args.table_name, args.num)
    elif args.command == "clear":
        clear_database(args.table_name)
    elif args.command == "search_under_age":
        search_under_age(args.table_name, args.age)
