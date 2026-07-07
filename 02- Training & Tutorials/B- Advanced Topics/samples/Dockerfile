#----------------------------------------------------------------------------------------------------------------------#
# AnyLog Dockerifle using an python:3.10-alpine, the image is roughly 600MB
#
# :process:
#   1. env params
#   2. install packages
#   3. Copy for packeging files
#   4. install python packages and build anylog
#   5. remove unneed files that were used for step 4
#   6. start AnyLog based on `INIT_TYPE` env param
#       -> bash starts a bash interface
#       -> raw starts AnyLog without any thing
#       -> if not set uses deployment scripts
# :overwrite entrrypoint:
# if a user would like to overwrite the default entrry point  they can do something like this:
#   docker run -it --rm your_image_name python3.10 $ANYLOG_HOME/source/anylog.py process !local_scirpts/personalized_file.al
#----------------------------------------------------------------------------------------------------------------------#
FROM python:3.10-alpine AS base

# declare params
ENV ANYLOG_PATH=/app \
    ANYLOG_LIB=/app/AnyLog-Network \
    ANYLOG_HOME=/app/AnyLog-Network \
    BLOCKCHAIN_DIR=/app/AnyLog-Network/blockchain \
    DATA_DIR=/app/AnyLog-Network/data \
    LOCAL_SCRIPTS=/app/deployment-scripts/scripts \
    TEST_DIR=/app/deployment-scripts/tests \
    DEBIAN_FRONTEND=noninteractive \
    NODE_NAME=anylog-node \
    NODE_TYPE=rest \
    NODE_NAME=anylog-node
#ENV USERNAME=anylog
#ENV ANYLOG_SERVER_PORT=32548
#ENV ANYLOG_REST_PORT=32549
#ENV ANYLOG_BROKER_PORT=2150

# Expose TCP and REST ports
EXPOSE $ANYLOG_SERVER_PORT \
       $ANYLOG_REST_PORT \
       $ANYLOG_BROKER_PORT

# update & install packages 
RUN apk update && \
    apk add --no-cache \
  bash \
  git \
  build-base \
  libpq-dev \
  libffi-dev \
  py3-jwt \
  gcc \
  musl-dev \
  cmake \
  jpeg-dev \ 
  zlib-dev \
  libjpeg-turbo-dev && \
  python3.10 -m pip install --upgrade pip

# move to WORKDIR + COPY codebsae
WORKDIR $ANYLOG_PATH
RUN mkdir -p $ANYLOG_HOME/source $ANYLOG_HOME/docker_files && \
    git clone -b os-dev https://github.com/AnyLog-co/deployment-scripts && \
    rm -rf $ANYLOG_PATH/deployment-scripts/.idea \
           $ANYLOG_PATH/deployment-scripts/archive 

COPY source/* $ANYLOG_HOME/source
COPY docker_files/setup.py $ANYLOG_HOME/docker_files/setup.py 
COPY docker_files/requirements-alpine.txt $ANYLOG_HOME/docker_files/requirements-alpine.txt 
COPY docker_files/deploy_anylog.sh $ANYLOG_HOME/deploy_anylog.sh

# Set permissions dirs

RUN chmod 777 $ANYLOG_PATH && \
    chmod -R 755 $ANYLOG_HOME $ANYLOG_PATH/deployment-scripts 

RUN  python3.10 -m pip install --upgrade -r $ANYLOG_HOME/docker_files/requirements-alpine.txt --no-cache-dir || true && \
    python3.10 $ANYLOG_HOME/docker_files/setup.py build && \
    python3.10 $ANYLOG_HOME/docker_files/setup.py install


ENV DIRECTORIES_TO_REMOVE="README.md api blockchain cmd dbms generic job json_to_sql members tcpip build anylog_node.spec"
RUN for DIR in $DIRECTORIES_TO_REMOVE; do rm -rf "${ANYLOG_HOME}/source/${DIR}"; done && \
    rm -rf $ANYLOG_HOME/build \
       $ANYLOG_HOME/dist \
       $ANYLOG_HOME/anylog_node.egg-info \
       $ANYLOG_HOME/docker_files

FROM base AS start_node
ENTRYPOINT bash $ANYLOG_HOME/deploy_anylog.sh

