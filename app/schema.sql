
DROP TABLE IF EXISTS models_history;


CREATE TABLE models_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  model_name TEXT NOT NULL,
  model_description TEXT NOT NULL,
  metrics TEXT NOT NULL,
  model_pickle_path TEXT NOT NULL,
  model_version INTEGER NOT NULL,
  training_dataset TEXT NOT NULL
);
