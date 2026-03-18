import json
import os

import faiss
import numpy as np
from openai import OpenAI
from fastembed import TextEmbedding

from bot.config import (
    OPENROUTER_API_KEY, CHAT_MODEL,
    INDEX_DIR, FAQS_PATH, TOP_K, OPENROUTER_BASE_URL,
)

LOCAL_EMBED_MODEL = "BAAI/bge-small-en-v1.5"

# Локальная модель для эмбеддингов (не требует API)
_embed_model = None

# Чат через OpenRouter
router_client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

_index = None
_faqs = None


def _get_embed_model():
    global _embed_model
    if _embed_model is None:
        _embed_model = TextEmbedding(model_name=LOCAL_EMBED_MODEL)
    return _embed_model


def _get_embedding(text: str) -> np.ndarray:
    model = _get_embed_model()
    return list(model.embed([text]))[0]


def build_index():
    """Создаёт FAISS-индекс из faqs.json и сохраняет в index/."""
    with open(FAQS_PATH, encoding="utf-8") as f:
        faqs = json.load(f)

    texts = [f"Вопрос: {faq['question']}\nОтвет: {faq['answer']}" for faq in faqs]

    model = _get_embed_model()
    embeddings = np.array(list(model.embed(texts)), dtype="float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, os.path.join(INDEX_DIR, "faqs.index"))
    with open(os.path.join(INDEX_DIR, "faqs_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(faqs, f, ensure_ascii=False, indent=2)

    print(f"Индекс создан: {index.ntotal} записей, размерность {dimension}")


def load_index():
    """Загружает FAISS-индекс и метаданные."""
    global _index, _faqs
    _index = faiss.read_index(os.path.join(INDEX_DIR, "faqs.index"))
    with open(os.path.join(INDEX_DIR, "faqs_metadata.json"), encoding="utf-8") as f:
        _faqs = json.load(f)
    _get_embed_model()
    print(f"Индекс загружен: {_index.ntotal} записей")


def search(query: str, top_k: int = TOP_K) -> list[dict]:
    """Ищет top_k наиболее релевантных FAQ."""
    embedding = np.array([_get_embedding(query)], dtype="float32")
    distances, indices = _index.search(embedding, top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(_faqs):
            results.append({
                "question": _faqs[idx]["question"],
                "answer": _faqs[idx]["answer"],
                "distance": float(distances[0][i]),
            })
    return results


def generate_answer(query: str) -> str:
    """Ищет контекст в базе знаний и генерирует ответ."""
    results = search(query)

    context = "\n\n".join(
        f"Q: {r['question']}\nA: {r['answer']}" for r in results
    )

    response = router_client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты — ИИ-консультант по теме искусственного интеллекта и промпт-инжиниринга. "
                    "Отвечай на русском языке. Используй предоставленный контекст из базы знаний "
                    "для формирования ответа. Если в контексте нет релевантной информации, "
                    "честно скажи об этом. Будь дружелюбным и полезным."
                ),
            },
            {
                "role": "user",
                "content": f"Контекст из базы знаний:\n{context}\n\nВопрос пользователя: {query}",
            },
        ],
        temperature=0.3,
        max_tokens=1000,
    )

    return response.choices[0].message.content
