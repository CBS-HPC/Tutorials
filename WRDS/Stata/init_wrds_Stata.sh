#!/bin/bash

mkdir ~/odbc

cat > ~/odbc/odbc.ini << 'EOL'
[ODBC Data Sources]
wrds-postgres = PostgreSQL

[wrds-postgres]
Driver           = PostgreSQL
Description      = Connect to WRDS on the WRDS Cloud
Database         = wrds
Username         = username
Password         = password
Servername       = wrds-pgdata.wharton.upenn.edu
Port             = 9737
SSLmode          = require
EOL

chmod 600 ~/odbc/odbc.ini

cat > ~/odbc/odbc.sh  << 'EOL'
ODBCINST="/etc/odbcinst.ini"; export ODBCINST
ODBCINI="$HOME/odbc/odbc.ini"; export ODBCINI
EOL

ls -l ~/odbc/  