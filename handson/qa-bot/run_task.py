import argparse, time, uuid, json
import boto3
from colorama import init, Fore, Back, Style
init(autoreset=True)

class Params:
    def __init__(self):
        # get parameters from SSM
        ssm_client = boto3.client("ssm")
        self.ECS_CLUSTER_NAME = ssm_client.get_parameter(Name="ECS_CLUSTER_NAME")["Parameter"]["Value"]
        self.ECS_TASK_DEFINITION_ARN = ssm_client.get_parameter(Name="ECS_TASK_DEFINITION_ARN")["Parameter"]["Value"]
        self.CONTAINER_NAME = ssm_client.get_parameter(Name="CONTAINER_NAME")["Parameter"]["Value"]
        self.ECS_TASK_VPC_SUBNET_1 = ssm_client.get_parameter(Name="ECS_TASK_VPC_SUBNET_1")["Parameter"]["Value"]
        self.TABLE_NAME = ssm_client.get_parameter(Name="TABLE_NAME")["Parameter"]["Value"]

def ask(context, question, timeout=240):
    """
    Given 'context' and 'question', this function asks a single question.
    """
    P = Params()

    print("Submitting task...")
    item_id = str(uuid.uuid4()) # ID of the dynamoDB entry
    client = boto3.client("ecs")
    resp = client.run_task(
        cluster=P.ECS_CLUSTER_NAME,
        taskDefinition=P.ECS_TASK_DEFINITION_ARN,
        count=1,
        launchType="FARGATE",
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [P.ECS_TASK_VPC_SUBNET_1],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
            'containerOverrides': [
                {
                    'name': P.CONTAINER_NAME,
                    'command': [
                        context, question, item_id
                    ],
                }
            ]
        }
    )

    task_arn = resp["tasks"][0]["taskArn"]
    print("Task ARN:", task_arn)

    print("Waiting for the task to finish...")
    for i in range(timeout):
        time.sleep(1)
        print("", end=".", flush=True)
        resp = client.describe_tasks(
            cluster=P.ECS_CLUSTER_NAME,
            tasks=[task_arn],
        )
        if resp["tasks"][0]["lastStatus"] == "STOPPED":
            break

    # get the answer from DynamoDB
    print() # new line
    if i >= timeout - 1:
        print("Sorry, task did not finish until timeout!")
        return

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(P.TABLE_NAME)
    resp = table.get_item(
        Key={"item_id": item_id}
    ).get("Item")
    print(Back.GREEN + "Context:", resp["context"])
    print(Back.BLUE + "Question:", resp["question"])
    print(Back.MAGENTA + "Answer:", resp["answer"])
    print(Back.YELLOW + "Score:", resp["score"])

def ask_many():
    """
    Ask many questions at once. The questions are defined in "problems.json".
    """
    P = Params()

    with open("problems.json", "r") as f:
        problems = json.load(f)
    
    print("Submitting task...")
    client = boto3.client("ecs")
    for prob in problems:
        print("", end=".", flush=True)
        item_id = str(uuid.uuid4()) # ID of the dynamoDB entry
        resp = client.run_task(
            cluster=P.ECS_CLUSTER_NAME,
            taskDefinition=P.ECS_TASK_DEFINITION_ARN,
            count=1,
            launchType="FARGATE",
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [P.ECS_TASK_VPC_SUBNET_1],
                    'assignPublicIp': 'ENABLED'
                }
            },
            overrides={
                'containerOverrides': [
                    {
                        'name': P.CONTAINER_NAME,
                        'command': [
                            prob["context"], prob["question"], item_id
                        ],
                    }
                ]
            }
        )
    print() # new line

def list_answers(limit):
    """
    List the answers to the questions that have been submitted previously
    """
    P = Params()

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(P.TABLE_NAME)
    resp = table.scan().get("Items")

    for (i, r) in enumerate(resp):
        print(i)
        print(Back.GREEN + "Context:", r["context"])
        print(Back.BLUE + "Question:", r["question"])
        print(Back.MAGENTA + "Answer:", r["answer"])
        print(Back.YELLOW + "Score:", r["score"])

def clear():
    """
    Clear all answers in the database
    """

    P = Params()

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(P.TABLE_NAME)
    resp = table.scan().get("Items")

    for (i, r) in enumerate(resp):
        table.delete_item(
            Key={"item_id": r["item_id"]}
        )
    print("Deleted all answers in the DynamoDB!")

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Run question-answering task in ECS"
    )
    subparsers = parser.add_subparsers(dest="command")

    ask_p = subparsers.add_parser("ask")
    ask_p.add_argument("context", type=str)
    ask_p.add_argument("question", type=str)

    ask_many_p = subparsers.add_parser("ask_many")

    list_p = subparsers.add_parser("list_answers")
    list_p.add_argument("--limit", type=int, default=50)

    clear_p = subparsers.add_parser("clear")

    args = parser.parse_args()

    if args.command == "ask":
        ask(args.context, args.question)
    elif args.command == "ask_many":
        ask_many()
    elif args.command == "list_answers":
        list_answers(args.limit)
    elif args.command == "clear":
        clear()
