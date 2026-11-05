import psycopg

with psycopg.connect(
    dbname="chat_analysis",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
) as conn:
    print("Подключение к PostgreSQL успешно!")