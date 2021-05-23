import boto3
from datetime import datetime

def main():
    session = boto3.Session()
    client = session.client("batch")

    resp = client.submit_job(
        jobName="test",
        jobQueue="SimpleBatchjob-queue",
        jobDefinition="SimpleBatchjob-definition",
        containerOverrides={
            "command": ["echo", "Hello World"]
        }
    )
    print("Job submitted!")
    print("job name", resp["jobName"], "job ID", resp["jobId"])

if __name__ == "__main__":
    main()
