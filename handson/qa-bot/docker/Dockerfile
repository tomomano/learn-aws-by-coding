FROM ubuntu:18.04
LABEL maintainer="Tomoyuki Mano"

RUN apt update \
    && apt install -y \
        git \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists

RUN python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir \
        torch \
        boto3

WORKDIR /workspace
RUN git clone https://github.com/huggingface/transformers \
    && cd transformers/ \
    && git checkout v4.8.1 \
    && python3 -m pip install --no-cache-dir .

# Download the pre-trained model
RUN echo "from transformers import pipeline; nlp = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')" >> tmp.py \
    && python3 tmp.py \
    && rm tmp.py

# Fix encoding errors
RUN apt update \
    && apt install -y locales \
    && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY main.py /workspace
ENTRYPOINT ["python3", "main.py"]
