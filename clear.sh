#!/bin/bash

su - postgres -c "psql << EOF
UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'hydra';

SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'hydra';

DROP DATABASE hydra;

CREATE DATABASE hydra OWNER hydra;
GRANT ALL PRIVILEGES ON DATABASE hydra TO hydra;
EOF"


