#!/bin/bash

# migrate loginserver-mysql
./login_migrate.sh

# migrate hydra-postgresql database
./hydra_migrate.sh

# start first time
./deploy.sh
#./restart.sh
