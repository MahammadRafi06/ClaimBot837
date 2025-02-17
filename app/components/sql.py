from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from components.llms import llm_openai
import time
from dotenv import load_dotenv
import os
import pymysql  # for error handling

load_dotenv()

user = os.getenv("user")
pwd = os.getenv("pwd")
database = os.getenv("database")  # Fixed typo

# Print for debugging
print(user, pwd, database)

def wait_for_db():
    while True:
        try:
            db = SQLDatabase.from_uri(f"mysql+pymysql://{user}:{pwd}@127.0.0.1:3306/{database}")
            if db.get_table_info():  # Ensure db is connected and tables exist
                print("Database is ready!")
                return db
        except pymysql.MySQLError as e:
            print(f"Waiting for database... Error: {e}")
            time.sleep(5)

db = wait_for_db()



toolkit = SQLDatabaseToolkit(db=db, llm=llm_openai)
tools = toolkit.get_tools()
list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")