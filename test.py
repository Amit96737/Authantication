from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.invoke(
    model="gpt-5.5",
    input="Who is the prime minister of india ?"
)

print(response)