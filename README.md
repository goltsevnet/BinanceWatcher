# Инструкция
1. Установите зависимости `poetry install`.
2. Запустите `pytest`.
3. Запустите `main.py`.
4. Остановить программу `ctr+c`

## Улучшение кода:
1. Горячее добавления и удаление mini_ticker. 
2. Обработка ошибок, если стрим unsubscribe или по какой-то причине падает Websocket.
3. Попытка переподключения.
4. Pydantic для обработки Websocket message.
5. Добавление logging on/off и уровня логирования.
6. Покрытие всего тестами