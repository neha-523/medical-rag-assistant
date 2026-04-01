import ollama


MODEL_NAME = "llama3.1"


def generate_answer(prompt: str) -> str:
    """
    Send prompt to LLaMA 3.1 via Ollama and return the response text.
    Uses streaming=False for simple request/response.
    """
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are DataPilot, a precise data engineering assistant. Answer only from the provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.1,   # low temp = factual, grounded answers
            "num_predict": 512,   # max tokens in response
        }
    )
    return response["message"]["content"]


def generate_answer_streaming(prompt: str):
    """
    Generator version — yields text chunks as they stream in.
    Used later by the Streamlit UI for live typing effect.
    """
    stream = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are DataPilot, a precise data engineering assistant. Answer only from the provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.1,
            "num_predict": 512,
        },
        stream=True
    )
    for chunk in stream:
        yield chunk["message"]["content"]