import boto3, argparse, base64
from multiprocessing import Pool, cpu_count
client = boto3.client("lambda")

def invoke(p):
    function_name = p[0]
    print("", end=".", flush=True)
    client.invoke(
        FunctionName=function_name,
        InvocationType="Event",
    )

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("function_name", type=str)
    parser.add_argument("num_tasks", type=int)
    args = parser.parse_args()

    # submit tasks
    with Pool(cpu_count()) as p:
        params = [(args.function_name, i) for i in range(args.num_tasks)]
        p.map(invoke, params)

    print(f"\nSubmitted {args.num_tasks} tasks to Lambda!")
