import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

FAQS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "faqs.json")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "index")

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "openai/gpt-4o-mini"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
TOP_K = 3
