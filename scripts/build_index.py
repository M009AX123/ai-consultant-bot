#!/usr/bin/env python3
"""Скрипт для создания FAISS-индекса из базы FAQ."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bot.rag import build_index

if __name__ == "__main__":
    print("Создание FAISS-индекса...")
    build_index()
    print("Готово!")
