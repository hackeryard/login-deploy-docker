export OAUTH2_CONSENT_URL=http://10.10.26.30:3001/consent
export OAUTH2_LOGIN_URL=http://10.10.26.30:3001/login
export OAUTH2_ISSUER_URL=http://10.10.26.30:4443
export OAUTH2_SHARE_ERROR_DEBUG=1
export LOG_LEVEL=debug
export DATABASE_URL=postgres://hydra:secret@localhost:5432/hydra?sslmode=disable
export SYSTEM_SECRET=fdfdsearas92jj3x
export PUBLIC_PORT=4443

./hydra serve all --dangerous-force-http

