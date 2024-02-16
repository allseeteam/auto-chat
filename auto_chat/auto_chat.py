from typing import List, Union
import datetime
import os

from telegram.client import Telegram
from telegram.client import AsyncResult
from telegram_text.bases import Element
import pytz

from routines.read_file import read_yaml
from routines.yaml_to_datetime_time import yaml_to_datetime_time
from yandex_gpt.yandex_gpt import YandexGPT


class AutoChat(Telegram, YandexGPT):
    def __init__(
            self,
            telegram_config_file_path: str,
            auto_chat_config_file_path: str,
            yandex_cloud_config_file_path: str,
            yandex_gpt_key_file_path: str
    ) -> None:
        # reading config files
        telegram_config = read_yaml(telegram_config_file_path)
        auto_chat_config = read_yaml(auto_chat_config_file_path)
        # initializing Telegram class
        Telegram.__init__(
            self,
            api_id=int(telegram_config['ApiId']),
            api_hash=telegram_config['ApiHash'],
            phone=telegram_config['PhoneNumber'],
            database_encryption_key=telegram_config['DatabaseEncryptionKey'],
            files_directory=os.path.join(
                os.getcwd(),
                telegram_config['FilesDirectory']
            ),
            login=True,
        )
        # initializing YaGPT class
        YandexGPT.__init__(
            self,
            yandex_cloud_config_file_path=yandex_cloud_config_file_path,
            yandex_gpt_key_file_path=yandex_gpt_key_file_path,
        )
        # setting autochat
        self._target_user_id = self._get_target_user_id(auto_chat_config['TargetUsername'])
        self._sending_time = yaml_to_datetime_time(auto_chat_config['SendingTime'])
        self._message_prompt = auto_chat_config['MessagePrompt']
        self._chat_mode = auto_chat_config['ChatMode']
        self._timezone = pytz.timezone(auto_chat_config['TimeZone'])

    def _get_target_user_id(
            self,
            target_username: str
    ) -> int:
        # getting target user id
        return int(self._get_contact_by_username(target_username)['id'])

    def _get_client_contacts(self) -> List[dict]:
        # getting client chats
        chats = self.get_chats()
        chats.wait()
        # getting contacts from private chats
        contacts = []
        for chat_id in chats.update['chat_ids']:
            chat = self.get_chat(chat_id)
            chat.wait()
            if chat.update['type']['@type'] == 'chatTypePrivate':
                contact = self.get_user(chat_id)
                contact.wait()
                contacts.append(contact.update)
        # returning contacts
        return contacts

    def _get_contact_by_username(
            self,
            target_username: str
    ) -> dict:
        # getting list of all contacts
        contacts = self._get_client_contacts()
        # finding target contact by username
        for contact in contacts:
            if contact['username'] == target_username:
                return contact
        # raise ValueError if there is no such contact
        raise ValueError(f"Contact with username {target_username} not found")

    def send_message_to_target_username(
            self,
            text: Union[str, Element],
            entities: Union[List[dict], None] = None,
    ) -> Union[AsyncResult, None]:
        # sending message to target contact
        return self.send_message(
            chat_id=self._target_user_id,
            text=text,
            entities=entities
        )

    def which_sending_time(self) -> int:
        # getting current time without seconds and microseconds
        current_time = (
            datetime.datetime
            .now(self._timezone)
            .replace(second=0, microsecond=0)
            .time()
        )
        # checking if current time is in sending time list and returning its index
        for index, sending_time_unit in enumerate(self._sending_time):
            if current_time == sending_time_unit:
                return index
        return -1

    def check_time_and_send(self):
        which_sending_time = self.which_sending_time()
        if which_sending_time > -1:
            prompt = self._message_prompt[which_sending_time]
            text = self.send_completion_request(
                message={
                    "role": "system",
                    "text": prompt
                }
            )['result']['alternatives'][0]['message']['text']
            self.send_message_to_target_username(text=text)
