-- Сырые запуски SpaceX в jsonb
CREATE TABLE IF NOT EXISTS raw.launches (
  id          text PRIMARY KEY,        -- id из SpaceX /v4/launches
  payload     jsonb NOT NULL,          -- весь ответ по одному запуску
  ingested_at timestamptz DEFAULT now()
);

-- На будущее: быстрые фильтры по дате/статусу
CREATE INDEX IF NOT EXISTS idx_launches_ingested_at ON raw.launches(ingested_at);