# AWS Batch Tutorial: Running a ML training in parallel

## Deploy
Create a new python virtual environment and install dependencies:

```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Set AWS credentials:

```bash
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=ABCDEFGHIJK
export AWS_DEFAULT_REGION=ap-northeast-1
```

Run deploy:

```bash
cdk deploy
```

## Build and upload docker image

Once the deployment is complete, go to the AWS console through your browser.
Then, navigate to `ECR` > `Repositories`.
There you will find a repository named `simplebatch-repositoryXXXX` (where XXXX is a random string generated for you).
Open this repository, and on the top right corner hit the button saying `View push commands`.
Simply execute each command displayed in the window (see picture).
Now your docker image is ready in AWS!

<img src="screenshot_ecr.png" width=400 />

## Submiting a single task

## 

## Destroy

```
cdk destroy
```

## Submitting job
