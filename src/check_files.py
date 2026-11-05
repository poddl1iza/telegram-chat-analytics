import json
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup


data_folder = Path("data/raw")
html_files = sorted(data_folder.glob("*.html"))

print("Найдено файлов:", len(html_files))

all_messages = []



for file_path in html_files:

    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    messages = soup.select("div.message.default")
    last_author = None

    for message in messages:

        message_id = message.get("id")

        body = message.find(
            "div", class_="body", recursive=False
        )

        # автор сообщения
        author_element = body.find(
            "div", class_="from_name", recursive=False
        ) if body else None

        if author_element:
            author = author_element.get_text(" ", strip=True)
            last_author = author
        else:
            author = last_author

        # дата сообщения
        date_element = body.select_one(
            ".pull_right.date.details"
        ) if body else None

        date = date_element.get("title") if date_element else None

        # о
        # бычный текст
        text_element = body.find(
            "div", class_="text", recursive=False
        ) if body else None

        text = (
            text_element.get_text(" ", strip=True)
            if text_element else None
        )

        # пересланный текст
        forwarded_element = body.select_one(
            ".forwarded .text"
        ) if body else None

        forwarded_text = (
            forwarded_element.get_text(" ", strip=True)
            if forwarded_element else None
        )

        # тип и название вложения
        media_title = message.select_one(
            ".media_wrap .title"
        )

        media_type = None
        media_name = None

        if media_title:
            title = media_title.get_text(strip=True).lower()

            if title in ["sticker", "photo", "animation"]:
                media_type = title

            elif title in [
                "video file",
                "video message",
                "voice message"
            ]:
                media_type = title

            else:
                media_type = "document"
                media_name = title

        # собираем данные сообщения
        message_data = {
            "message_id": message_id,
            "author": author,
            "date": date,
            "text": text,
            "forwarded_text": forwarded_text,
            "media_type": media_type,
            "media_name": media_name
        }

        all_messages.append(message_data)


# сохранение данных в JSON
output_file = Path("data/output/messages.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(
        all_messages,
        file,
        ensure_ascii=False,
        indent=4
    )

print("JSON успешно сохранён!")
print("Всего собрано сообщений:", len(all_messages))


# повторно открываем JSON для проверки
with open(output_file, "r", encoding="utf-8") as file:
    loaded_messages = json.load(file)


# проверка количества сообщений
print("\nПроверка JSON:")
print("Всего записей:", len(loaded_messages))

print(
    "Без обычного текста:",
    sum(1 for m in loaded_messages if not m["text"])
)

print(
    "С пересланным текстом:",
    sum(1 for m in loaded_messages if m["forwarded_text"])
)


# считаем типы вложений
media_stats = Counter(
    m["media_type"]
    for m in loaded_messages
    if m["media_type"]
)

print("\nТипы вложений:")

for media_type, count in media_stats.items():
    print(media_type, "-", count)


# проверяем пример со стикером
sticker = next(
    (
        m for m in loaded_messages
        if m["message_id"] == "message787962"
    ),
    None
)

print("\nПроверка сообщения со стикером:")
print(sticker)
print("\nПроверка качества данных:")

print(
    "Без автора:",
    sum(1 for m in loaded_messages if not m["author"])
)

print(
    "Без даты:",
    sum(1 for m in loaded_messages if not m["date"])
)

message_ids = [
    m["message_id"]
    for m in loaded_messages
]

print(
    "Повторяющиеся ID:",
    len(message_ids) - len(set(message_ids))
)