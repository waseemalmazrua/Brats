import asyncio

from openai import OpenAI

from app.core.config import settings


def get_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY)


async def explain_prediction(prediction: dict) -> str:
    client = get_client()

    prompt = f"""
    You are a medical AI assistant.

    Given the following prediction:
    {prediction}

    Explain the result in a simple, safe, and non-diagnostic way.
    Do NOT provide diagnosis.
    Do NOT give treatment advice.
    Suggest consulting a healthcare professional.
    """

    def call_llm():
        return client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a safe medical assistant."},
                {"role": "user", "content": prompt}
            ]
        )

    response = await asyncio.to_thread(call_llm)

    text = response.choices[0].message.content.strip()

    return text.strip()