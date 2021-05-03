# Test Flask Application

The application is a small flask demo application for Cloud Run. It takes 4 environment variables:


- DB_USER: The postgres user 
- DB_PASS: The password for the postgres user
- DB_NAME: The database name
- CLOUD_SQL_CONNECTION_NAME: The Cloudrun SQL connection name, e.g. "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"

The service will expose 2 endpoints

- "/" This will just return "Pong". It won't do anything else
- "/dbping" This will run 5 times "Select 1;" and then return "DBPong" together with the time it took to run these 5 queries

