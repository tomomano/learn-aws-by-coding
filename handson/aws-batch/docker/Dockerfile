FROM nvidia/cuda:11.0.3-devel-ubuntu20.04

ENV HOME /root

# Install python
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3 \
    python3-pip

# Install pytorch
RUN pip3 install -f https://download.pytorch.org/whl/torch_stable.html \
    torch==1.7.1+cu110 \
    torchvision==0.8.2+cu110

# Install other python libraries
RUN pip3 install \
    matplotlib \
    boto3 \
    pandas

# Download MNIST dataset and save in /${HOME}
RUN echo "from torchvision import datasets; datasets.MNIST(root='/mnist', download=True)" >> tmp.py && \
    python3 tmp.py

COPY main.py simple_mnist.py ${HOME}/

WORKDIR ${HOME}
ENTRYPOINT ["python3", "main.py"]
