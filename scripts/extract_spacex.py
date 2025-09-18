#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тянем SpaceX /v4/launches и сохраняем поштучно в raw.launches (jsonb).
- Идемпотентно: ON CONFLICT (id) DO UPDATE — не дублируем записи.
- Подключение к Postgres берём из .env (локальный хост и порт).
"""

import os, sys, json, time
from typing import List, Dict

import requests
import psycopg2
from psycopg2.extras import execute_batch

SPACEX_URL = "https://api.spacexdata.com/v4/launches"   # публичное API

def get_pg_conn():
    host = os.getenv("POSTGRES_DATA_HOST", "127.0.0.1")         # для хоста скрипт запускаем с Mac
    port = int(os.getenv("POSTGRES_DATA_PORT", "5432"))         # из твоего .env
    user = os.getenv("POSTGRES_DATA_USER", "de")
    password = os.getenv("POSTGRES_DATA_PASSWORD", "de_password")
    db = os.getenv("POSTGRES_DATA_DB", "de_raw")

    dsn = f"host={host} port={port} user={user} password={password} dbname={db}"
    return psycopg2.connect(dsn)

def fetch_launches() -> List[Dict]:
    # Простой GET. В дальнейшем можно сделать инкремент по дате/id.
    r = requests.get(SPACEX_URL, timeout=60)
    r.raise_for_status()
    return r.json()

def upsert_launches(conn, items: List[Dict]):
    # Пишем поштучно: id + весь json в payload
    sql = """
        INSERT INTO raw.launches (id, payload)
        VALUES (%s, %s::jsonb)
        ON CONFLICT (id) DO UPDATE
        SET payload = EXCLUDED.payload,
            ingested_at = now();
    """
    rows = [(item.get("id"), json.dumps(item)) for item in items if item.get("id")]
    with conn.cursor() as cur:
        # execute_batch ускоряет вставку группой
        execute_batch(cur, sql, rows, page_size=500)
    conn.commit()

def main():
    try:
        print("→ Запрашиваю SpaceX /v4/launches ...", flush=True)
        launches = fetch_launches()
        print(f"← Получил записей: {len(launches)}", flush=True)

        with get_pg_conn() as conn:
            upsert_launches(conn, launches)
        print("✓ Готово: данные в raw.launches", flush=True)
    except Exception as e:
        print(f"✗ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()