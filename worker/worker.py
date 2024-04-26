import os
import pymongo
import psycopg2

MONGO_USERNAME=os.environ['MONGO_USERNAME']
MONGO_PASSWORD=os.environ['MONGO_PASSWORD']
MONGO_PORT=os.environ['MONGO_PORT']
MONGO_DB=os.environ['MONGO_DB']
USER_COLLECTION=os.environ['USER_COLLECTION']
DATA_COLLECTION=os.environ['DATA_COLLECTION']
MONGO_HOST=os.environ['MONGO_HOST']

POSTGRES_PASSWORD=os.environ['POSTGRES_PASSWORD']

mongo_uri=f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
mongo_client = pymongo.MongoClient(mongo_uri)
mongo_db = mongo_client.user_login_system
mongo_collection = mongo_db['data']

# PostgreSQL connection
pg_uri = os.environ.get('POSTGRES_URI')
pg_conn = psycopg2.connect(pg_uri)
pg_cur = pg_conn.cursor()

# MongoDB change stream
with mongo_collection.watch() as stream:
    for change in stream:
        if change['operationType'] == 'insert':
            # Extract new data from the change event
            new_data = change['fullDocument']
            
            # Transform data if needed
            data = {
                'field1': new_data['field1'],
                'field2': new_data['field2']
            }
            
            # Insert into PostgreSQL
            pg_cur.execute("INSERT INTO your_table (field1, field2) VALUES (%s, %s)", (data['field1'], data['field2']))
            pg_conn.commit()

pg_conn.close()
