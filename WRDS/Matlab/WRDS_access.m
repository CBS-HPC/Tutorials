%% Connect to
driver = eval('org.postgresql.Driver');
dbURL = 'jdbc:postgresql://wrds-pgdata.wharton.upenn.edu:9737/wrds?ssl=require&sslfactory=org.postgresql.ssl.NonValidatingFactory';
username = 'wrds_username';
password = 'wrds_password';
WRDS = java.sql.DriverManager.getConnection(dbURL, username, password);

%% 
q = WRDS.prepareStatement("select * from DJONES.DJDAILY");
rs = q.executeQuery();


%% 
% Prepare SQL statement and execute:
q = WRDS.prepareStatement("select * from library.dataset");
rs = q.executeQuery();

% Loop through result set:
while (rs.next())
    table_schema = char(rs.getString(1));
    matlabData(rs.getRow,:) = {table_schema};
end
disp(matlabData)

% Clean up
rs.close();
WRDS.close();