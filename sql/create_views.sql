CREATE OR REPLACE VIEW word_statistics AS
SELECT
    m.message_id,
    m.author,
    m.message_date,
    rm.word[1] AS word
FROM messages AS m
CROSS JOIN LATERAL regexp_matches(
    m.message_text,
    '[А-Яа-яЁё]+',
    'gi'
) AS rm(word);