### Данный репозиторий содержит исходный код для автоапдейтов в tg на базе YaGPT.

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