# using python parent image
FROM python:3-slim

# defining workdir
WORKDIR /auto_chat

# copying the current directory contents into the container
COPY ./ /auto_chat

# installing any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# installing openssl 1.1 using the package manager
RUN apt-get update
RUN apt-get install -y wget
RUN wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb

# running start script (ENTRYPOINT instead of CMD to be sure that our run.py would catch stop signal)
ENTRYPOINT [ \
    "python", \
    "run.py", \
    "--telegram-config", \
    "config/telegram.yaml", \
    "--auto-chat-config", \
    "config/autolove.yaml", \
    "--yandex-cloud-config", \
    "config/yandex_cloud.yaml", \
    "--yandex-gpt-key", \
    "keys/yandex_authorization_key.json" \
]
