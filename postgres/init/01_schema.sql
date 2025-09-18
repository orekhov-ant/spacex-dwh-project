-- создаём схемы для пайплайна SpaceX
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;

-- проверочная таблица, чтобы увидеть, что init прошёл
CREATE TABLE IF NOT EXISTS raw._init_ok (
  created_at timestamptz DEFAULT now()
);