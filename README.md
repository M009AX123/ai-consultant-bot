# 🤖 AI Consultant Bot — Личный ИИ-консультант в Telegram

> Интеллектуальный Telegram-бот на базе **RAG** (Retrieval-Augmented Generation) для ответов на вопросы об искусственном интеллекте и промпт-инжиниринге.

---

## ✨ Основные возможности

- 🧠 **RAG-система** с локальными векторными эмбеддингами (без внешних API)
- ⚡ **FAISS** — быстрый векторный поиск по базе знаний
- 🤖 **GPT-4o-mini** через **OpenRouter** (работает из России 🇷🇺)
- 📚 **База знаний** по ИИ и промпт-инжинирингу в формате JSON
- 🐳 **Docker** — простой деплой на любой VPS за 5 минут
- 🔒 **Никаких внешних API** для эмбеддингов — модель работает локально

---

## 🏗️ Архитектура

```
┌─────────────────┐
│  Telegram User  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Telegram Bot   │ ◄─── python-telegram-bot
│   (handlers)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RAG Pipeline   │
│  ┌───────────┐  │
│  │ Embedding │  │ ◄─── fastembed / BAAI/bge-small-en-v1.5 (локально)
│  └───────────┘  │
│  ┌───────────┐  │
│  │   FAISS   │  │ ◄─── Векторный поиск по базе знаний
│  └───────────┘  │
│  ┌───────────┐  │
│  │  GPT-4o   │  │ ◄─── OpenRouter API (Chat Completion)
│  └───────────┘  │
└─────────────────┘
```

---

## 📁 Структура проекта

```
ai-consultant-bot/
├── .env.example          # Шаблон переменных окружения
├── .gitignore            # Git-исключения (секреты не попадают в репо)
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Docker Compose для деплоя
├── requirements.txt      # Python зависимости
├── README.md             # Документация
│
├── bot/                  # Основной модуль бота
│   ├── __init__.py
│   ├── main.py           # Точка входа, регистрация хендлеров
│   ├── handlers.py       # Обработчики команд и сообщений
│   ├── rag.py            # RAG pipeline (поиск + генерация)
│   └── config.py         # Конфигурация из .env
│
├── data/
│   └── faqs.json         # База знаний (вопрос-ответ)
│
├── index/                # FAISS индекс (генерируется скриптом)
│   ├── faqs.index
│   └── faqs_metadata.json
│
└── scripts/
    └── build_index.py    # Скрипт построения векторного индекса
```

---

## 🚀 Установка и запуск

### Требования

- Python 3.10+
- Docker + Docker Compose (для деплоя на VPS)
- Telegram Bot Token (от [@BotFather](https://t.me/BotFather))
- OpenRouter API ключ ([openrouter.ai](https://openrouter.ai))

### Локальный запуск

**1. Клонируйте репозиторий**
```bash
git clone https://github.com/M009AX123/ai-consultant-bot.git
cd ai-consultant-bot
```

**2. Создайте виртуальное окружение**
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# или
venv\Scripts\activate      # Windows
```

**3. Установите зависимости**
```bash
pip install -r requirements.txt
```

**4. Настройте переменные окружения**
```bash
cp .env.example .env
# Откройте .env и заполните значения
```

**5. Постройте индекс**
```bash
python scripts/build_index.py
```

**6. Запустите бота**
```bash
python -m bot.main
```

---

### 🐳 Деплой на VPS через Docker

```bash
# Клонируйте репозиторий на сервере
git clone https://github.com/M009AX123/ai-consultant-bot.git
cd ai-consultant-bot

# Заполните .env
cp .env.example .env
nano .env

# Запустите
docker compose up -d --build
```

Бот будет работать в фоне и автоматически перезапускаться при перезагрузке сервера.

---

## ⚙️ Конфигурация

Переменные окружения (`.env`):

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# OpenRouter (chat completion)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# RAG настройки
TOP_K=3
CHAT_MODEL=openai/gpt-4o-mini
```

### Получение токенов

**Telegram Bot Token:**
1. Напишите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot` и следуйте инструкциям
3. Скопируйте полученный токен

**OpenRouter API Key:**
1. Зарегистрируйтесь на [openrouter.ai](https://openrouter.ai)
2. Перейдите в **Keys** → **Create Key**
3. Пополните баланс (от $1) для использования моделей

---

## 🎮 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и краткая инструкция |
| `/help` | Примеры вопросов, которые умеет обрабатывать бот |

**Примеры вопросов:**
```
Пользователь: Что такое RAG?
Бот: RAG (Retrieval-Augmented Generation) — это подход, при котором...

Пользователь: Как работает промпт-инжиниринг?
Бот: Промпт-инжиниринг — это процесс разработки и оптимизации...

Пользователь: Что такое эмбеддинги?
Бот: Эмбеддинги — это векторные представления текста...
```

---

## 🔧 Компоненты системы

### 1. RAG Pipeline (`bot/rag.py`)
Основной компонент системы:
- **`build_index()`** — читает `data/faqs.json`, создаёт эмбеддинги и сохраняет FAISS индекс
- **`load_index()`** — загружает индекс при старте бота
- **`search(query)`** — находит top-K релевантных FAQ по векторному сходству
- **`generate_answer(query)`** — формирует контекст и генерирует ответ через GPT-4o-mini

### 2. Модель эмбеддингов
Используется **`BAAI/bge-small-en-v1.5`** через библиотеку `fastembed`:
- ✅ Работает полностью локально — не нужен никакой API
- ✅ Загружается автоматически при первом запуске
- ✅ Быстрая и компактная (~130 МБ)

### 3. Векторное хранилище (FAISS)
- Индекс типа `IndexFlatL2` (точный поиск по L2-расстоянию)
- Строится один раз скриптом `scripts/build_index.py`
- Сохраняется в папке `index/`

### 4. Chat Completion (OpenRouter)
- Модель: `openai/gpt-4o-mini`
- Temperature: `0.3` (стабильные, фактические ответы)
- Max tokens: `1000`
- Системный промпт настроен на ответы на русском языке

---

## 📊 Как расширить базу знаний

Откройте `data/faqs.json` и добавьте новые записи:

```json
[
  {
    "question": "Что такое RAG?",
    "answer": "RAG (Retrieval-Augmented Generation) — это архитектура..."
  },
  {
    "question": "Ваш новый вопрос",
    "answer": "Ваш ответ"
  }
]
```

После добавления пересоберите индекс:
```bash
python scripts/build_index.py
# или на сервере:
docker compose restart
```

---

## 🛠️ Troubleshooting

**Бот не отвечает на вопросы:**
- Проверьте, что `TELEGRAM_BOT_TOKEN` указан корректно
- Убедитесь, что индекс был создан: папка `index/` должна содержать файлы

**Ошибка OpenRouter 403:**
- Убедитесь, что `OPENROUTER_API_KEY` корректен
- Проверьте баланс на [openrouter.ai](https://openrouter.ai)

**Контейнер не стартует:**
```bash
docker compose logs -f   # посмотреть логи
```

---

## 📝 Лицензия

MIT License

---

## 👥 Авторы

Разработано как персональный ИИ-консультант по теме искусственного интеллекта и промпт-инжиниринга.

---

## 🙏 Благодарности

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — Telegram Bot Framework
- [fastembed](https://github.com/qdrant/fastembed) — Локальные эмбеддинги
- [FAISS](https://github.com/facebookresearch/faiss) — Векторный поиск
- [OpenRouter](https://openrouter.ai) — LLM API (работает из России)
- [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) — Модель эмбеддингов
