from groq import Groq


def ask_llm(context, question, api_key, model):
    client = Groq(api_key=api_key)

    prompt = f"""
Answer only using the context below.
If the answer is not present, respond with: "Not enough information in the provided context."

Context:
{context}

Question: {question}

Answer:
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()
