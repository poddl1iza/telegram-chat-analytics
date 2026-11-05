CREATE TABLE messages (
    message_id TEXT PRIMARY KEY,
    author TEXT NOT NULL,
    message_date TIMESTAMPTZ,
    message_text TEXT,
    forwarded_text TEXT,
    media_type TEXT,
    media_name TEXT
);