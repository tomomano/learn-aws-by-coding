# Docker image for hands-on

This is a Docker image which contains libraries/software to run the hands-on programs.

The image is pre-installed with

- Python 3.7
- Node.js 12.0
- AWS CLI
- AWS CDK

## Launching the container in an interactive mode

```bash
docker run -it registry.gitlab.com/tomomano/intro-aws:latest
```

Once launched, you will find the hands-on source code in `~/intro-aws/handson/`.
Then, `cd` into this directory, and run the programs.

Have fun!
