import boto3, argparse, base64

def main(function_name):
    client = boto3.client("lambda")
    response = client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
    )
    print(response['Payload'].read().decode("utf-8"))

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("function_name", type=str)
    args = parser.parse_args()

    main(args.function_name)
