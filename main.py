from retrieve import querier
from google import genai
from dotenv import load_dotenv
load_dotenv(".llmenv")


client = genai.Client()  



def build_prompt(question, context):
   
    return f"""You are answering questions using ONLY the passages below.

Some passages may be more relevant than others, and the most relevant one is
not always listed first -- read all of them before deciding.

Rules:
1. If any passage actually answers the question, answer using it and cite the
   file and section it came from in the end like this  
   Citation: file and section
2. If none of the passages actually answer the question, say clearly that the
   documents don't cover this. Do not guess, and do not use outside knowledge.

Passages:
{context}

Question: {question}"""

def ask_llm(prompt):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text
 
def answer_question(question):
    results = querier(question)
    if results=='':
        return "I don't have this in the provided documents.", results
    prompt = build_prompt(question, results)
    answer = ask_llm(prompt)
    return answer, results

if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or 'quit'): ")
        if question.lower() == "quit":
            break
        answer, results = answer_question(question)
        print(f"\n\nAnswer: {answer}")
