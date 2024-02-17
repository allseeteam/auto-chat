### Данный репозиторий содержит исходный код для автоапдейтов в tg на базе YaGPT.

<br>

#### Перед использованием необходимо будет задать конфигурационные файлы с параметрами из примеров в папке config, а также создать ключ авторизации Yandex Cloud. Как это сделать — смотрите по следующим ссылкам:
- [Yandex Cloud IAM](https://cloud.yandex.ru/ru/docs/iam/operations/iam-token/create-for-sa#via-jwt)
- [Yandex Cloud Key](https://cloud.yandex.ru/ru/docs/iam/operations/authorized-key/create#console_1)
- [Yandex Cloud SA ID](https://cloud.yandex.ru/ru/docs/iam/operations/sa/get-id)
- [Telegram API](https://core.telegram.org/api/obtaining_api_id)
- [Python-Telegram](https://python-telegram.readthedocs.io/en/latest/tutorial.html)

<br>

#### Как использовать локально:
- Установка зависимостей
```bash
git clone https://github.com/PE51K/auto-chat
сd auto-chat
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- Установка openssl

Arch Linux
```bash
sudo pacman -S yay
yay -S openssl-1.1
```
Ubuntu или Debian
```bash
apt-get update
apt-get install -y wget
wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
```
- Запуск скрипта
```bash
chmod -x ./run.sh
./ run.sh
```

<br>

#### Как использовать с docker:
```bash
git clone https://github.com/PE51K/auto-chat
сd auto-chat
docker build -t auto_chat .
docker run -d --name auto_chat-container auto_chat
```