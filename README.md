Telegram Bot
=============================

This bot can detect faces on uploading images, convert voice/audio messages to wav format with preselected samplerate.

Guide
------------

First, you need to create and configure the environment settings through the env.yaml file on the root:

      START_MESSAGE: "Hello, send me a voice message or some pictures."
      TELEGRAM_API_TOKEN: 'your_telegram_bot_token'
      TELEGRAM_FILE_URL: "https://api.telegram.org/bot{0}/getFile?file_id={1}"
      TELEGRAM_IMAGE_URL: "https://api.telegram.org/file/bot{0}/{1}"
      POSTGRES_DB_NAME: 'your_db_name'
      POSTGRES_DB_USER: 'your_db_user'
      POSTGRES_DB_PASSWORD: 'your_password'
      POSTGRES_DB_HOST: 'your_host'
      SAMPLERATE: '16000'
      
Then run migration command from migrations/init.py
This will create all necessary tables.

Run
------------
Run telegram/test_work.py and the bot will start working.
