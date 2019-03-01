FROM ubuntu:16.04

# set maintainer
LABEL maintainer="spalani2@jhu.edu"

# update
RUN apt-get update && apt-get -y upgrade

# install packages
RUN apt-get install -y \
    cmake \
    cpio \
    gfortran \
    libpng-dev \
    freetype* \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    software-properties-common\
    git \
    man \
    wget

# install python3
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y \
  python3.6 \
  python3.6-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py

RUN ln -s /usr/bin/python3.6 /usr/local/bin/python

# add vim in docker
RUN apt-get install -y vim

# make a directory for mounting local files into docker
RUN mkdir /root/workspace/
WORKDIR /root/workspace/

# copy the file-indexer code into the container
COPY . /root/workspace/

# install python requirements
RUN pip install -r requirements.txt

# setup pep8 guidelines (restricts push when pep8 is violated)
RUN rm -f ./.git/hooks/pre-commit
RUN chmod 777 install-hooks.sh
RUN ./install-hooks.sh

# add code to PYTHONPATH for dev purposes
RUN echo "export PYTHONPATH='${PYTHONPATH}:/root/workspace'" >> ~/.bashrc

# clean dir
RUN py3clean .

# launch terminal
CMD ["/bin/bash"]
