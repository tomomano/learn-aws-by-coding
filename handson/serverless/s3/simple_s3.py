import boto3
import argparse
import os

s3 = boto3.resource('s3')

def upload_file(bucket_name, filename, key=None):
    bucket = s3.Bucket(bucket_name)

    if key is None:
        key = os.path.basename(filename)

    bucket.upload_file(filename, key)
    print("Upload completed.")
    print("Original file:", filename)
    print("Key in bucket:", key)

def download_file(bucket_name, key, filename=None):
    bucket = s3.Bucket(bucket_name)

    if filename is None:
        filename = os.path.basename(key)

    bucket.download_file(key, filename)
    print("Download completed.")

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket_name", type=str)
    subparsers = parser.add_subparsers(dest="command")
    p1 = subparsers.add_parser("upload")
    p1.add_argument("filename", type=str)
    p1.add_argument("--key", type=str, required=False)
    p2 = subparsers.add_parser("download")
    p2.add_argument("key", type=str)
    args = parser.parse_args()

    if args.command == "upload":
        if args.key:
            upload_file(args.bucket_name, args.filename, args.key)
        else:
            upload_file(args.bucket_name, args.filename)
    elif args.command == "download":
        download_file(args.bucket_name, args.key)
