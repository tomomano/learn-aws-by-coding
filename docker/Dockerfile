FROM node:20
LABEL maintainer="Tomoyuki Mano"

RUN apt-get update \
    && apt-get install nano less

RUN cd /opt \
    && curl -q "https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz" -o Python-3.12.0.tgz \
    && tar -xzf Python-3.12.0.tgz \
    && cd Python-3.12.0 \
    && ./configure --enable-optimizations \
    && make install

RUN cd /opt \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

RUN npm install -g aws-cdk

# clean up unnecessary files
RUN rm -rf /opt/*

# copy hands-on source code in /root/
COPY handson/ /root/handson

# Make command line prettier...
RUN echo "alias ls='ls --color=auto'" >> /root/.bashrc
RUN echo "PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@aws-handson\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> /root/.bashrc

RUN mkdir -p /root/.ssh
WORKDIR /root
CMD ["/bin/bash"]
