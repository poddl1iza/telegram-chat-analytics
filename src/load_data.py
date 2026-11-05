
import json
import os
from pathlib import Path
from datetime import datetime

import psycopg
from dotenv import load_dotenv


# Загружаем настройки из .env
project_path = Path(__file__).parent.parent
load_dotenv(project_path / ".env")

# Путь к JSON
file_path = project_path / "data" / "output" / "messages.json"

with open(file_path, "r", encoding="utf-8") as file:
    messages = json.load(file)

# Подключение к PostgreSQL
with psycopg.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
) as conn:

    with conn.cursor() as cur:

        for message in messages:
            cur.execute(
                """
                INSERT INTO messages (
                    message_id,
                    author,
                    message_date,
                    message_text,
                    forwarded_text,
                    media_type,
                    media_name
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (message_id) DO NOTHING
                """,
                (
                    message["message_id"],
                    message["author"],
                    datetime.strptime(
                        message["date"],
                        "%d.%m.%Y %H:%M:%S UTC%z"
                    ),
                    message["text"],
                    message["forwarded_text"],
                    message["media_type"],
                    message["media_name"]
                )
            )

print(f"Загружено сообщений: {len(messages)}")
