# Транскрибация аудио через OpenAI Whisper + Flask

## Описание
Веб-приложение для загрузки аудио/видео и получения текста.
Работает через модели Whisper (small) и поддерживает запуск в Docker.

---

## Структура проекта
```bash
transcriB/
├── app.py               # Основной сервер Flask
├── templates/
│   └── index.html       # Веб-интерфейс
├── uploads/             # Временные хранилище файлов (монтируемо)
├── requirements.txt     # Python-зависимости
├── Dockerfile           # Сборка контейнера
├── docker-compose.yml   # Упрощенный запуск через compose
└── README.md            # Как пользоваться
```

---

## Требования
- Docker (https://www.docker.com/get-started)
- ПОРТ 5003 должен быть свободен
- Для работы без Docker: Python 3.9+, ffmpeg (см. инструкцию в коде)

---

## Быстрый старт через Docker Compose

1. Скачать проект локально:
   ```bash
   git clone ...  # ссылка на ваш репозиторий
   cd transcriB
   ```

2. Построить и запустить контейнер:
   ```bash
   docker-compose up --build
   ```
   > Первый запуск скачает модель Whisper (~500Мб)

3. Перейти в браузере на http://localhost:5003

---

## Ручная сборка через Docker

```bash
docker build -t transcrib-app .
docker run -p 5003:5003 transcrib-app
```

---

## Использование
- Перетащите или выберите аудиофайл в браузере, нажмите "Распознать"
- Дождитесь результата и скачайте итоговый текст файла

---

## Дополнительные параметры
- Для ускорения используйте GPU-контейнеры и модели Whisper `medium`/`large` (при наличии видеокарты и поддержки Docker CUDA)
- Все временные файлы в папке uploads, её можно подключить как volume

## Использование GPU (ускорение на видеокарте NVIDIA)
Если у вас установлен драйвер NVIDIA, Docker и NVIDIA Container Toolkit, можно использовать ускорение на GPU:

1. Установите драйвер NVIDIA и NVIDIA Container Toolkit (https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
2. В файле `docker-compose.yml` раскомментируйте секцию:
   ```yaml
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
   # runtime: nvidia
   ```
3. Запустите с помощью docker compose как обычно:
   ```bash
   docker compose up --build
   ```

На GPU обработка файлов будет в ~10-50 раз быстрее (зависит от вашей модели видеокарты).

---

## Вопросы? Ошибки?
Пишите мне или откройте issue!
