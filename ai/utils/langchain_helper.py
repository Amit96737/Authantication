from langchain_openai import ChatOpenAI

def ask_ai(question):
    llm = ChatOpenAI(
        temperature=0.7,
        model="gpt-4o-mini"
    )

    response = llm.invoke(question)
    return response.content