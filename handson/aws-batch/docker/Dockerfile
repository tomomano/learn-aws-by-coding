FROM nvidia/cuda:11.0.3-devel-ubuntu20.04

ENV HOME /root

RUN apt update && \
    apt install --no-install-recommends -y \
    python3 \
    python3-pip

RUN pip3 install -f https://download.pytorch.org/whl/torch_stable.html \
    torch==1.7.1+cu110 \
    torchvision==0.8.2+cu110

RUN pip3 install \
    matplotlib \
    boto3

COPY main.py simple_mnist.py /root/

WORKDIR ${HOME}
