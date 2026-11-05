
-- 1. Общее количество сообщений
SELECT COUNT(*) AS total_messages
FROM messages;


-- 2. Количество сообщений по участникам
SELECT
    author,
    COUNT(*) AS message_count
FROM messages
GROUP BY author
ORDER BY message_count DESC;


-- 3. Количество употреблений слов с выбранным корнем
SELECT
    word,
    COUNT(*) AS occurrences
FROM word_statistics
WHERE word ILIKE '%хуй%'
GROUP BY word
ORDER BY occurrences DESC;


-- 4. Количество употреблений по участникам
SELECT
    author,
    COUNT(*) AS occurrences
FROM word_statistics
WHERE word ILIKE '%хуй%'
GROUP BY author
ORDER BY occurrences DESC;


-- 5. Динамика употребления по дням
SELECT
    DATE(message_date) AS day,
    COUNT(*) AS occurrences
FROM word_statistics
WHERE word ILIKE '%хуй%'
GROUP BY day
ORDER BY day;
