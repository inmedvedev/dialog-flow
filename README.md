## Dvmn-dialog-flow
[Телеграм](https://t.me/dialogflowdvmn_bot) и [VK](https://vk.com/club212750271) бот для ответа на часто задаваемые вопросы на основе AI инструмента [Dialogflow](https://dialogflow.cloud.google.com/)

### Как установить
1. Скопируйте проект
```
$ git clone <url репозитория>
```
2. Создайте и активируйте виртуальное окружение
```
$ python3 -m venv venv
$ source venv/bin/activate
```
3. Установите зависимости:
```
$ pip install -r requirements.txt
```
4. Задайте переменные окружения в файле .env
- `GOOGLE_APPLICATION_CREDENTIALS`=путь до json файла для работы с Dialogflow
- `PROJECT_ID`=id проекта в Google Cloud Platform
- `BOT_LANGUAGE`=язык распрознования текста
- `VK_BOT_TOKEN`=токен для работы с API Vkontakte.
- `TELEGRAM_BOT_TOKEN`=токен вашего телеграм бота. [Как получить токен бота](https://tlgrm.ru/docs/bots)
- `LOGGER_TELEGRAM_TOKEN`=токен телграм бота-логгера
- `TG_CHAT_ID`=Ваш чат ID в телеграм. Чтобы его узнать, отправьте сообщение @userinfobot

5. Запуск ботов
```
$ python tgbot.py
$ python vkbot.py
```
### Пример работы

[![VkweBke6FG.gif](https://s7.gifyu.com/images/VkweBke6FG.gif)](https://gifyu.com/image/SLgBx)

[![Q0n16iKjbG.gif](https://s7.gifyu.com/images/Q0n16iKjbG.gif)](https://gifyu.com/image/SLgBK)