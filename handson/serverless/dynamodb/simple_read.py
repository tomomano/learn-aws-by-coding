import boto3
import argparse

ddb = boto3.resource('dynamodb')

def scan_table(table_name):
    table = ddb.Table(table_name)
    items = table.scan().get("Items")
    print(items)

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("table_name", type=str)
    args = parser.parse_args()

    scan_table(args.table_name)
