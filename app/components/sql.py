from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from components.llms import llm_openai
import time

def wait_for_db():
    while True:
        try:
            db = SQLDatabase.from_uri("mysql+pymysql://mrafi:Tasneem1996@db:3306/medical")
            if db.get_table_info():
                print("Database is ready!")
                return db
        except :
            print("Waiting for database...")
            time.sleep(5)

db = wait_for_db()

toolkit = SQLDatabaseToolkit(db=db, llm=llm_openai)
tools = toolkit.get_tools()
list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")