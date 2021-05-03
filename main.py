# Inspired by
# https://cloud.google.com/sql/docs/postgres/quickstart-connect-run?hl=de
# https://cloud.google.com/sql/docs/postgres/samples/cloud-sql-postgres-sqlalchemy-create-socket?hl=de

import os
import sqlalchemy
import time
import json
from flask import Flask

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


@app.route("/")
def ping():
    print(json.dumps({
        'text': 'Pong'
    }))
    return "Pong"

@app.route("/dbping")
def dbpong():
    start_time = time.time()
    # Set the following variables depending on your specific
    # connection name and root password from the earlier steps:
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"] # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
    
    db = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_sock": f"/cloudsql/{cloud_sql_connection_name}/.s.PGSQL.5432"
            }
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )
    
    stmt = sqlalchemy.text('SELECT 1;')
    try:
        with db.connect() as conn:
            for i in range(5): # we execute the "SELECT 1;" 5 times to see latency issues better
                conn.execute(stmt)
    except Exception as e:
        print(json.dumps({
            'text': f'Error: {str(e)}'
        }))
        return f'Error: {str(e)}'
    
    elapsed = time.time() - start_time
    print(json.dumps({
        'text': f"DBPong: {elapsed}",
        'time': elapsed
    }))
    return f"DBPong: {elapsed}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))