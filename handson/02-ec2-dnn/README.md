# Hands-on #1: Creating a EC2 instance

**For the full step-by-step tutorial, see https://tomomano.gitlab.io/intro-aws**

## Installation

Create a new python `virtual environment`:

```bash
python3 -m venv .env
```

This will create a directory named `.env/`. Activate the environment and install dependencies:

```bash
source .env/bin/activate
pip install -r requirements.txt
```

### Set AWS credentials

```bash
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=ABCDEFGHIJK
export AWS_DEFAULT_REGION=ap-northeast-1
```

### Generate a SSH key pair

First, run the following command to createa a SSH key pair:
```bash
export KEY_NAME="HirakeGoma"
aws ec2 create-key-pair --key-name ${KEY_NAME} --query 'KeyMaterial' --output text > ${KEY_NAME}.pem
```

This will create a SSH secret key named `HirakeGoma.pem`. Move this secret key to a place where your computer stores SSH secret keys, such as `.ssh/`. After moving the file, be sure to set the correct access permission.

```bash
mv HirakeGoma.pem ~/.ssh/
chmod 400 ~/.ssh/HirakeGoma.pem 
```

### Deploy

To deploy the stack, run

```bash
cdk deploy -c key_name=$KEY_NAME
```

### Accessing the EC2 server

1. `cdk deploy` command will print the IP address of the instance. Find a line that says `MyfirstEc2.InstancePublicIp = XXXXX`
1. Using the command copied above, connect to the server. e.g.

    ```
    ssh -i ~/.ssh/HirakeGoma.pem ec2-user@<IP address>
    ```

### Destroy

To destroy the stack, run
```bash
cdk destroy
```

**NOTE**: You can do the same operation from AWS console. Go to `CloudFormation` -> `Stacks`. Find the stack, and delete it.

You should also delete the SSH key pair, which is no longer used.
1. `rm ~/.ssh/HirakeGoma.pem`
2. From the AWS console, go to `EC2` -> `Key pair`. Find the key pair, and delete it.
