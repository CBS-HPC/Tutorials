#!/bin/bash

cat > ~/.pgpass << 'EOL'
wrds-pgdata.wharton.upenn.edu:9737:wrds:username:password
EOL

chmod 600 ~/.pgpass

ls -l ~/.pgpass

R -e "install.packages('RPostgres')" 