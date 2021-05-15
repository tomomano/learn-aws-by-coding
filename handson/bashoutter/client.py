import boto3, argparse, base64
from multiprocessing import Pool, cpu_count
import requests

def post_haiku(p):
    endpoint_url = p[0]
    print("", end=".", flush=True)
    resp = requests.post(
        endpoint_url + "/haiku",
        json={
            "username": "松尾芭蕉",
            "first": "閑さや",
            "second": "岩にしみ入る",
            "third": "蝉の声"
        }
    )

def delete_haiku(p):
    endpoint_url = p[0]
    item_id = p[1]
    print("", end=".", flush=True)
    resp = requests.delete(
        endpoint_url + "/haiku/" + item_id
    )

def post_many_haiku(endpoint_url, num):
    with Pool(cpu_count()) as pool:
        params = [(endpoint_url, i) for i in range(num)]
        pool.map(post_haiku, params)
    print(f"\nSent POST /haiku requests {num} times.")

def clear_database(endpoint_url):
    haikus = requests.get(
        endpoint_url + "/haiku"
    ).json()

    if not haikus:
        return

    with Pool(cpu_count()) as pool:
        params = [(endpoint_url, h["item_id"]) for h in haikus]
        pool.map(delete_haiku, params)
    print(f"\nDeleted all haiku in the database.")

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint_url", type=str)
    subparsers = parser.add_subparsers(dest="command")

    sp1 = subparsers.add_parser("post_many")
    sp1.add_argument("num", type=int)

    sp2 = subparsers.add_parser("clear_database")

    args = parser.parse_args()

    if args.command == "post_many":
        post_many_haiku(args.endpoint_url, int(args.num))
    elif args.command == "clear_database":
        clear_database(args.endpoint_url)
