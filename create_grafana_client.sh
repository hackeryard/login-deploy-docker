./hydra clients create \
--endpoint http://10.10.26.30:4445 \
--id test-client-grafana \
--secret test-secret-grafana \
--response-types code,id_token \
--grant-types refresh_token,authorization_code \
--scope openid,offline \
--callbacks http://10.10.26.24:3000/login/generic_oauth
