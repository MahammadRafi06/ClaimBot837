from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm_openai = ChatOpenAI(model="gpt-4o",temperature=0)

