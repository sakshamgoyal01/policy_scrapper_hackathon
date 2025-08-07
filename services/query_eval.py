import os, re, json
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "deepseek-r1-distill-llama-70b"

async def generate_answer_response(question, clauses):
    excerpts = "\n\n".join(f"{c['number']}: {c['text']}" for c in clauses)
    prompt = f"""
You are a legal document assistant AI. You are provided with a list of policy clauses from an insurance document.
You must answer the user's question using only the content from those clauses. Return a valid JSON object with the following fields:

- answer: a direct answer to the question based on the clause content.
- clause_numbers: list of clause numbers (e.g., ["2.1", "4.3"]) that were used to derive the answer.
- confidence_score: a float between 0 and 1 indicating how confident you are.
- reasoning: explain how you derived the answer based on the referenced clauses.

Always respond in JSON format.
Question:
{question}

Policy Clauses:
{excerpts}

Return answer in this JSON format:
{{
  "answer": "..."
  
}}
Only respond with JSON. Do not include explanations before or after.
"""

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=700,
        )
        content = response.choices[0].message.content.strip()

        # Try parsing JSON from content
        match = re.search(r"\{[\s\S]*\}", content)
        json_str = match.group(0) if match else content

        # Validate and return JSON
        return json.loads(json_str)

    except json.JSONDecodeError as e:
        return {
            "question": question,
            "answer": "Unable to generate answer.",
            "clause_numbers": [],
            "confidence_score": 0.0,
            "reasoning": f"JSON decoding failed: {str(e)}. Raw response: {content}"
        }
    except Exception as e:
        return {
            "question": question,
            "answer": "Unable to generate answer.",
            "clause_numbers": [],
            "confidence_score": 0.0,
            "reasoning": str(e)
        }
