# Docker image for hands-on

This is a Docker image which contains libraries/software to run the hands-on programs.

The image is pre-installed with

- Python 3.7
- Node.js 12.0
- AWS CLI
- AWS CDK

## (For developer) Building docker image locally

`cd` to the root of the repository, and run

```bash
docker build -t labc -f docker/Dockerfile .
```
