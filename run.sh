#!/bin/bash

# setting python executable path
PYTHON_EXECUTABLE=$(which python)

# setting python script path
SCRIPT_PATH=run.py

# setting configuration file paths
TELEGRAM_CONFIG='config/telegram.yaml'
AUTO_CHAT_CONFIG='config/autolove.yaml'
YANDEX_CLOUD_CONFIG='config/yandex_cloud.yaml'
YANDEX_GPT_KEY='keys/yandex_authorization_key.json'

# running python script
$PYTHON_EXECUTABLE $SCRIPT_PATH \
    --telegram-config $TELEGRAM_CONFIG \
    --auto-chat-config $AUTO_CHAT_CONFIG \
    --yandex-cloud-config $YANDEX_CLOUD_CONFIG \
    --yandex-gpt-key $YANDEX_GPT_KEY
