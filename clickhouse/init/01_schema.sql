-- ClickHouse: создаём БД под витрины/факты
CREATE DATABASE IF NOT EXISTS dwh;

-- проверочная таблица
CREATE TABLE IF NOT EXISTS dwh._init_ok
(
  created_at DateTime DEFAULT now()
)
ENGINE = MergeTree
-- базовый и самый универсальный движок таблиц в ClickHouse.
ORDER BY created_at;
-- В MergeTree поле ORDER BY — обязательно. Это ключ сортировки. Сортировка обеспечивается внутри каждого парта, влияет на эффективность сжатия и мержей.
-- Хороший выбор для append-only временных рядов.