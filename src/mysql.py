from dotenv import load_dotenv
import os
from langchain_community.utilities import SQLDatabase

load_dotenv(override=True)

db_uri = os.getenv("db_uri")
db = SQLDatabase.from_uri(db_uri)

def get_schema(_):
    schema = db.get_table_info()
    return schema

def run_query(query):
    results = db.run(query)
    return results

#print(run_query("SELECT * FROM apmtanalytics LIMIT 1"))