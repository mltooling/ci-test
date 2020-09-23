# BUILD Definition
FROM ubuntu:20.04

RUN \
    apt-get update && apt-get install -y python3 python3-pip openssh-client && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip

RUN \
    pip install docker

COPY "/resources/test.py" "/resources/test.py"
COPY "/resources/run.py" "/resources/run.py"
COPY "/resources/config.py" "/resources/config.py"

# RUN Definition:
ENTRYPOINT [ "python" ]
CMD [ "/resources/run.py" ]
