import os
import datetime
import threading
import time

from telegram_client.telegram_client import TelegramClient
from routines.read_file import read_yaml


# loading environment variables
telegram_config = read_yaml('config/telegram.yaml')

# initializing auto sender
auto_sender = TelegramClient(
    api_id=int(telegram_config['ApiId']),
    api_hash=telegram_config['ApiHash'],
    phone='+79181034711',
    database_encryption_key=telegram_config['DatabaseEncryptionKey'],
    files_directory=os.path.join(
        os.getcwd(),
        telegram_config['FilesDirectory']
    ),
    login=True,
    target_username='gregory1m',
    message_text='Hello!',
    sending_time=[
        datetime.time(17, 5),
        datetime.time(0, 29),
        datetime.time(0, 30),
    ],
    timezone='Europe/Moscow'
)


def check_time_and_send():
    while not exit_flag.is_set():
        if auto_sender.is_sending_time():
            auto_sender.send_message_by_username(
                target_username=auto_sender.target_username,
                text=auto_sender.message_text
            )
        time.sleep(60)


exit_flag = threading.Event()
thread = threading.Thread(target=check_time_and_send)
thread.start()

time.sleep(160)
exit_flag.set()
thread.join()
auto_sender.stop()
