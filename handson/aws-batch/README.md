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

Execute deploy:

```bash
cdk deploy
```

## Destroy

```
cdk destroy
```

## Submitting job
