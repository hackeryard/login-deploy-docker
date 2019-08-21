./hydra clients create \
--endpoint http://10.10.26.30:4445 \
--id test-client \
--secret test-secret \
--response-types code,id_token \
--grant-types refresh_token,authorization_code \
--scope openid,offline \
--token-endpoint-auth-method client_secret_post \
--callbacks http://10.10.26.30:8003/

