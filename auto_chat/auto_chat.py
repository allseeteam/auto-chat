from telegram.client import AsyncResult
from telegram_text.bases import Element
from telegram.client import Telegram
from typing import List, Union
import datetime
import pytz
import os

from routines.read_file import read_yaml
from routines.yaml_to_datetime_time import yaml_to_datetime_time
from yandex_gpt.yandex_gpt import YandexGPT


class AutoChat(Telegram, YandexGPT):
    def __init__(
            self,
            target_username: str = None,
            sending_time: List[datetime.time] = None,
            chat_system_prompt: List[str] = None,
            chat_mode: bool = None,
            timezone: pytz.timezone = None,
            telegram_config_file_path: str = None,
            auto_chat_config_file_path: str = None,
            *args,
            **kwargs,
    ) -> None:
        # initializing telegram
        # checking if api_id, api_hash, phone, database_encryption_key, files_directory and login in **kwargs
        if all(
                key
                in kwargs
                for key
                in [
                    'api_id',
                    'api_hash',
                    'phone',
                    'database_encryption_key',
                    'files_directory',
                    'login'
                ]
        ):
            Telegram.__init__(
                *args,
                **kwargs,
            )
        # if there is no then calling custom telegram init method
        else:
            self._init_telegram(telegram_config_file_path)
        # initializing yandex gpt
        # checking if iam_token and catalog_id in **kwargs
        if all(
                key
                in kwargs
                for key
                in [
                    'iam_token',
                    'catalog_id'
                ]
        ):
            YandexGPT.__init__(
                *args,
                **kwargs
            )
        # if there is no then calling custom yandex gpt init method
        else:
            self._init_yandex_gpt(
                *args,
                **kwargs
            )
        # initializing auto chat
        # checking if target_username, sending_time, chat_system_prompt, chat_mode, timezone is set
        if all([
            target_username,
            sending_time,
            chat_system_prompt,
            chat_mode,
            timezone
        ]):
            self._target_user_id = self._get_target_user_id(target_username)
            self._sending_time = yaml_to_datetime_time(sending_time)
            self._chat_system_prompt = chat_system_prompt
            self._chat_mode = chat_mode
            self._timezone = timezone
        # if there is no then calling custom auto chat init method
        else:
            self._init_autochat(auto_chat_config_file_path)

    def _init_yandex_gpt(
            self,
            *args,
            **kwargs
    ) -> None:
        # checking if yandex_cloud_config_file_path and yandex_gpt_key_file_path in **kwargs
        if not all(
                key
                in kwargs
                for key
                in [
                    'yandex_cloud_config_file_path',
                    'yandex_gpt_key_file_path'
                ]
        ):
            raise ValueError(
                "AutoChat args must contain either"
                " 'yandex_cloud_config_file_path' and "
                "'yandex_gpt_key_file_path' or "
                "'iam_token' and 'catalog_id'"
            )
        # if they are than calling custom yandex gpt init method
        else:
            YandexGPT.__init__(
                self,
                *args,
                **kwargs
            )

    def _init_telegram(
            self,
            telegram_config_file_path: str = None,
    ) -> None:
        # checking if telegram_config_file_path is set
        if not telegram_config_file_path:
            raise ValueError(
                "AutoChat args must contain either"
                " 'telegram_config_file_path' or "
                "'api_id', 'api_hash', 'phone', "
                "'database_encryption_key', "
                "'files_directory' and 'login'"
            )
        # if it is than calling custom telegram init method
        else:
            # reading config file
            telegram_config = read_yaml(telegram_config_file_path)
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
                login=telegram_config['Login'],
            )

    def _init_autochat(
            self,
            auto_chat_config_file_path: str = None
    ) -> None:
        # checking if auto_chat_config_file_path is set
        if not auto_chat_config_file_path:
            raise ValueError(
                "AutoChat args must contain ether 'auto_chat_config_file_path'"
                " or 'target_username', 'sending_time', 'chat_system_prompt',"
                " 'chat_mode' and 'timezone'"
            )
        # if it is than calling custom auto chat init method
        # reading config file
        auto_chat_config = read_yaml(auto_chat_config_file_path)
        # setting autochat
        self._target_user_id = self._get_target_user_id(auto_chat_config['TargetUsername'])
        self._sending_time = yaml_to_datetime_time(auto_chat_config['SendingTime'])
        self._chat_system_prompt = auto_chat_config['ChatSystemPrompt']
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
        # checking if current time is in sending time list and returning its index or -1 if it is not
        for index, sending_time_unit in enumerate(self._sending_time):
            if current_time == sending_time_unit:
                return index
        return -1

    def check_time_and_send(self):
        # checking if current time is in sending time list
        which_sending_time = self.which_sending_time()
        # if it is than sending message
        if which_sending_time > -1:
            prompt = self._chat_system_prompt[which_sending_time]
            text = self.send_completion_request(
                messages=[
                    {
                        "role": "system",
                        "text": prompt
                    }
                ]
            )['result']['alternatives'][0]['message']['text']
            self.send_message_to_target_username(text=text)
