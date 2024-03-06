# telegram-bot-video-downloader

## About

Change TOKEN with your token 

Usage:
  - Send link of video (@vid inline is comfortable)
  - The bot will download the video and send it
      - If the video is larger than 50MB, it is split into smaller parts, 
        which then need to be concatenated (in linux: cat vid.mp4* > vid.mp4)

## How to install
This script require:
  - Python3 interpreter
  - Telegram python api https://github.com/python-telegram-bot/python-telegram-bot
  - yt-dlp https://github.com/yt-dlp/yt-dlp (installed on the machine)

```
apt install -y python3-pip python3 yt-dlp
pip3 install -r requirements.txt
```

## How to start

```
screen
TELEGRAM_TOKEN="telegram_token" python3 main.py
```